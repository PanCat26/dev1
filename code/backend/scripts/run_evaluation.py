#!/usr/bin/env python
"""Evaluate retrieval ranking and optional answer quality for held-out repos.

Run from ``code/backend`` so imports resolve similarly to other scripts."""

from __future__ import annotations

import argparse
import asyncio
import json
from pathlib import Path
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import config

from evaluation.answer_metrics import (
    deepeval_installed,
    normalize_retrieval_section,
    score_answer_quality,
)
from evaluation.dataset import generate_retrieval_questions
from evaluation.report import (
    build_report_payload,
    summarize_answer as aggregate_answer_quality,
    write_evaluation_reports,
    build_retrieval_repo_section,
)
from evaluation.retrieval_metrics import evaluate_questions_retrieval
from evaluation.types import AnswerEvalRow, RepoRetrievalAgg


def resolve_backend_path(candidate: Path) -> Path:
    if candidate.is_absolute():
        return candidate
    return (ROOT / candidate).resolve()


def load_repo_entries(primary: Path, override: Path | None) -> list[dict[str, Any]]:
    with primary.open(encoding="utf-8") as handle:
        data = json.load(handle)
    entries = [_normalize_repo_entry(raw) for raw in data]

    if not override:
        return entries

    with override.open(encoding="utf-8") as extra:
        supplemental = [_normalize_repo_entry(raw) for raw in json.load(extra)]


    manual_map = {
        item["repo_id"]: item["questions"]
        for item in supplemental
        if item.get("repo_id") and item.get("questions") is not None
    }

    supplemental_ids = {item["repo_id"] for item in supplemental}
    repo_ids_existing = {item["repo_id"] for item in entries}
    orphans = supplemental_ids - repo_ids_existing

    if orphans:
        joined = ", ".join(sorted(orphans))
        raise ValueError(f"--questions-file references unknown repo_id values: {joined}")

    if manual_map:

        for entry in entries:

            override_qs = manual_map.get(entry["repo_id"])

            if override_qs is not None:

                entry["questions"] = override_qs

    return entries


def _normalize_repo_entry(payload: dict[str, Any]) -> dict[str, Any]:
    if "repo_id" not in payload or "snapshot_path" not in payload:
        missing = []
        if "repo_id" not in payload:
            missing.append("repo_id")
        if "snapshot_path" not in payload:
            missing.append("snapshot_path")
        raise ValueError(f"Repository entry incomplete (missing {', '.join(missing)}): {payload}")
    qs = payload.get("questions") or []
    cleaned_questions = [str(q).strip() for q in qs if str(q).strip()]
    return {
        "name": payload.get("name") or payload["repo_id"],
        "repo_id": str(payload["repo_id"]).strip(),
        "commit_sha": _clean_sha(payload.get("commit_sha")),
        "snapshot_path": str(payload["snapshot_path"]).strip(),
        "questions": cleaned_questions,
    }


def _clean_sha(raw: Any) -> str | None:
    if raw is None:
        return None
    value = str(raw).strip()
    return value or None


def summarize_retrieval_across_repos(per_repo_sections: list[dict[str, Any]]) -> dict[str, Any]:
    total_questions = sum(int(block.get("num_questions") or 0) for block in per_repo_sections)
    if total_questions == 0:
        return {
            "total_questions": 0,
            "macro_top1_pct": None,
            "macro_recall_at_3_pct": None,
            "macro_recall_at_5_pct": None,
            "per_repo": [],
        }

    weighted = {
        "top1": 0.0,
        "recall_at_3": 0.0,
        "recall_at_5": 0.0,
    }
    summarized_rows: list[dict[str, Any]] = []

    for block in per_repo_sections:
        n = int(block.get("num_questions") or 0)
        wt1 = float(block.get("top1_accuracy_pct") or 0.0)
        wr3 = float(block.get("recall_at_3_pct") or 0.0)
        wr5 = float(block.get("recall_at_5_pct") or 0.0)
        summarized_rows.append(
            {
                "repo_name": block.get("repo_name"),
                "repo_id": block.get("repo_id"),
                "num_questions": n,
                "top1_pct": wt1,
                "recall_at_3_pct": wr3,
                "recall_at_5_pct": wr5,
            }
        )

        weighted["top1"] += wt1 * n
        weighted["recall_at_3"] += wr3 * n
        weighted["recall_at_5"] += wr5 * n

    denominator = float(total_questions)
    macro_top1 = weighted["top1"] / denominator
    macro_r3 = weighted["recall_at_3"] / denominator
    macro_r5 = weighted["recall_at_5"] / denominator

    return {
        "total_questions": total_questions,
        "macro_top1_pct": macro_top1,
        "macro_recall_at_3_pct": macro_r3,
        "macro_recall_at_5_pct": macro_r5,
        "per_repo": summarized_rows,
    }


async def _collect_generated_answer(repo_id: str, commit_sha: str | None, snapshot_path: str, question: str) -> str:
    from orchestration.service import answer_query

    buffer: list[str] = []

    async for raw in answer_query(
        repo_id=repo_id,
        commit_sha=commit_sha or "",
        snapshot_path=snapshot_path,
        user_query=question,
    ):
        try:
            event = json.loads(raw)
        except json.JSONDecodeError:
            continue
        evt_type = event.get("type")
        if evt_type == "content":
            buffer.append(str(event.get("delta", "")))
        elif evt_type == "error":
            raise RuntimeError(event.get("message") or str(event))

    return "".join(buffer)


def _evidence_sections(question: str, repo_id: str, commit_sha: str | None) -> tuple[list[str], list[str]]:
    from retrieval.service import retrieve_for_query

    errors: list[str] = []

    sections: list[str] = []

    commit = commit_sha or None

    try:
        package = retrieve_for_query(
            question,
            repo_id,
            commit_sha=commit,
            num_candidates=20,
            max_chunks_per_category_in_package=8,
        )
    except ValueError as exc:
        errors.append(str(exc))
        return sections, errors
    except Exception as exc:  # noqa: BLE001
        errors.append(f"Evidence rebuild failed: {exc}")
        return sections, errors

    for group in package.groups:
        for chunk in group.chunks:
            sections.append(
                normalize_retrieval_section(chunk.file_path, chunk.symbol_name, chunk.text)
            )

    if not sections:
        errors.append("Evidence package contained zero chunks.")

    return sections, errors


def run_manual_answer_eval(entry: dict[str, Any], skip_deepeval: bool) -> tuple[list[AnswerEvalRow], list[str]]:
    rows: list[AnswerEvalRow] = []
    notes: list[str] = []

    snapshot_path_abs = resolve_backend_path(Path(entry["snapshot_path"]))

    repo_id = entry["repo_id"]
    repo_name = entry["name"]
    sha = entry.get("commit_sha")
    qs = entry.get("questions") or []

    if not qs:
        notes.append(f"{repo_name} had no manual `questions`; skipping orchestration.")

    for manual_q in qs:
        errors_accum: list[str] = []

        try:
            answer_text = asyncio.run(
                _collect_generated_answer(repo_id, sha or None, str(snapshot_path_abs), manual_q)
            )
        except Exception as exc:  # noqa: BLE001 — surface runtime errors as report artifacts
            errors_accum.append(f"answer_generation_failed: {exc}")
            rows.append(
                AnswerEvalRow(
                    repo_id=repo_id,
                    repo_name=repo_name,
                    question=manual_q,
                    answer_text="",
                    relevancy_score=None,
                    faithfulness_score=None,
                    errors=list(errors_accum),
                )
            )
            continue

        evidence_sections: list[str] = []
        if answer_text.strip():
            evidence_sections, evid_err = _evidence_sections(manual_q, repo_id, sha or None)

            errors_accum.extend(evid_err)

        scores = (None, None, None, None, [])

        if skip_deepeval:

            errors_accum.append("DeepEval metrics skipped (--skip-deepeval).")

        else:

            scores = score_answer_quality(

                question=manual_q,

                answer_text=answer_text,

                retrieval_context_sections=evidence_sections,

            )


        rel, faith, rr, fr, errs = scores
        merged_errors = list(errors_accum + errs)

        rows.append(
            AnswerEvalRow(
                repo_id=repo_id,
                repo_name=repo_name,
                question=manual_q,
                answer_text=answer_text.strip(),
                relevancy_score=rel,
                faithfulness_score=faith,
                relevancy_reason=rr,
                faithfulness_reason=fr,
                errors=list(merged_errors),
            )
        )

    return rows, notes


def format_answer_sections(rows: list[AnswerEvalRow], skip_deepeval: bool) -> dict[str, Any]:
    render_rows = []
    for row in rows:
        preview_cap = 2000
        answer_preview = row.answer_text
        preview = answer_preview if len(answer_preview) <= preview_cap else answer_preview[:preview_cap] + "…"

        render_rows.append(
            {
                "repo_name": row.repo_name,
                "repo_id": row.repo_id,
                "question": row.question,
                "answer_preview": preview,
                "answer_full_length": len(row.answer_text),
                "answer_relevancy": str(row.relevancy_score) if row.relevancy_score is not None else "n/a",
                "faithfulness": str(row.faithfulness_score) if row.faithfulness_score is not None else "n/a",
                "answer_relevancy_reason": row.relevancy_reason or "",
                "faithfulness_reason": row.faithfulness_reason or "",
                "errors_rendered": "\n".join(row.errors),
            }
        )

    averages = aggregate_answer_quality(rows)

    description = (
        "DeepEval AnswerRelevancyMetric + FaithfulnessMetric were executed using the system's "
        "`answer_query` stream plus reconstructed Qdrant evidence."
        if not skip_deepeval and deepeval_installed()
        else "DeepEval metrics were disabled or unavailable for this invocation."
    )

    md_notes_parts = []

    md_notes_parts.append(description)

    if skip_deepeval:
        md_notes_parts.append(
            "**Note:** rerun without `--skip-deepeval` once judge credentials (`OPENROUTER_API_KEY` "
            "recommended, or DeepEval/OpenAI-compatible `OPENAI_API_KEY` + optional `OPENAI_BASE_URL`)."
        )

    merged = averages | {
        "_markdown_notes": "\n".join(md_notes_parts),
        "rows_rendered": render_rows,
        "deepeval_description": description,
        "skipped_metric_run": skip_deepeval,
    }

    return merged



def run_retrieval_for_entry(
    entry: dict[str, Any], max_questions: int, cand_limit: int
) -> tuple[RepoRetrievalAgg | None, list[str]]:
    snapshot_path_abs = resolve_backend_path(Path(entry["snapshot_path"]))

    if not snapshot_path_abs.is_dir():
        raise FileNotFoundError(
            f"Missing snapshot folder for `{entry['name']}` → `{snapshot_path_abs}` "
            "(populate `snapshot_path` with an existing extracted repository folder)."
        )

    questions, warns = generate_retrieval_questions(
        snapshot_path=str(snapshot_path_abs),
        repo_id=entry["repo_id"],
        repo_name=entry["name"],
        commit_sha=entry["commit_sha"],
        max_questions_per_repo=max_questions,
    )

    if not questions:
        return None, warns

    default_commit = entry.get("commit_sha") or None

    from retrieval.service import retrieve_ranked_chunks

    def ranked_fetch(question: str, repo_id_inner: str, commit_sha_override: str | None, _: int):  # noqa: ANN001
        merged_commit = commit_sha_override or default_commit or None

        try:
            return retrieve_ranked_chunks(
                query=question,
                repo_id=repo_id_inner,
                commit_sha=_clean_sha(merged_commit),
                num_candidates=max(5, cand_limit),
            )
        except Exception as exc:
            raise RuntimeError(f"{repo_id_inner} retrieval error: {exc}") from exc

    agg = evaluate_questions_retrieval(
        questions,
        ranked_fetcher=ranked_fetch,
        num_candidates=max(5, cand_limit),
    )
    return agg, warns



def build_arg_parser() -> argparse.ArgumentParser:

    parser = argparse.ArgumentParser(description="Run lightweight backend evaluation harness.")

    group = parser.add_mutually_exclusive_group()

    group.add_argument("--retrieval-only", action="store_true")

    group.add_argument("--answers-only", action="store_true")



    parser.add_argument(

        "--repos-file",

        type=Path,

        default=ROOT / "evaluation" / "eval_repos.example.json",

        help="JSON array describing repos to evaluate",

    )


    parser.add_argument(

        "--questions-file",

        type=Path,

        default=None,

        help="Optional JSON overriding manual QA questions keyed by repo_id",

    )



    parser.add_argument(

        "--output-dir",

        type=Path,

        default=ROOT / "reports" / "evaluation",

        help="Where JSON/Markdown reports are written",

    )



    parser.add_argument("--max-questions-per-repo", type=int, default=120)




    parser.add_argument("--num-candidates", type=int, default=48)



    parser.add_argument("--skip-deepeval", action="store_true")



    return parser


def main(argv: list[str] | None = None) -> int:

    argv = argv if argv is not None else sys.argv[1:]

    parser = build_arg_parser()

    args = parser.parse_args(argv)

    retrieval_only = bool(args.retrieval_only)

    answers_only = bool(args.answers_only)

    skip_metrics = bool(args.skip_deepeval)

    global_warnings: list[str] = []

    repos_path = resolve_backend_path(Path(args.repos_file))

    questions_override = resolve_backend_path(Path(args.questions_file)) if args.questions_file else None

    repos = load_repo_entries(repos_path, questions_override)

    retrieval_agg: dict[str, Any] | None = None

    if not answers_only:

        retrieval_sections = []

        for entry in repos:

            try:

                agg, warns = run_retrieval_for_entry(

                    entry,

                    args.max_questions_per_repo,

                    args.num_candidates,

                )

            except FileNotFoundError as missing:

                global_warnings.append(str(missing))

                continue

            except Exception as exc:  # noqa: BLE001

                global_warnings.append(f"{entry.get('name')}: retrieval crashed: {exc}")

                continue

            global_warnings.extend(warns or [])

            if agg is not None:

                retrieval_sections.append(build_retrieval_repo_section(agg))

        summary = summarize_retrieval_across_repos(retrieval_sections)

        retrieval_agg = {"summary": summary, "repos": retrieval_sections}

    if retrieval_only:

        answers_payload = {

            "skipped": True,

            "reason": "--retrieval-only",

            "_markdown_notes": "_Answer evaluation skipped because `--retrieval-only` was set._",

            "rows_rendered": [],

            "deepeval_description": "Not executed.",

            "avg_answer_relevancy_score": None,

            "avg_faithfulness_score": None,

        }

    else:

        answer_rows: list[AnswerEvalRow] = []

        answer_notes: list[str] = []

        for entry in repos:

            rows, notes = run_manual_answer_eval(entry, skip_metrics)

            answer_rows.extend(rows)

            answer_notes.extend(notes)

        global_warnings.extend(answer_notes)

        answers_payload = format_answer_sections(answer_rows, skip_metrics)

    report = build_report_payload(

        repos_config_path=repos_path,

        max_questions_per_repo=args.max_questions_per_repo,

        retrieval_agg=None if answers_only else retrieval_agg,

        answers=answers_payload,

        global_errors=global_warnings,

    )

    output_root = resolve_backend_path(Path(args.output_dir))

    json_path, md_path = write_evaluation_reports(report, output_root)

    print(f"[evaluation] wrote JSON report → {json_path}")

    print(f"[evaluation] wrote Markdown report → {md_path}")

    return 0


if __name__ == "__main__":

    raise SystemExit(main())
