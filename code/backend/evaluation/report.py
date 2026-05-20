from __future__ import annotations

from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from evaluation.types import AnswerEvalRow, RepoRetrievalAgg, RetrievalEvalQuestion


def _iso_timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def _fmt_pct(value: Any) -> str:
    if isinstance(value, (int, float)):
        return f"{float(value):.3f}".rstrip("0").rstrip(".")
    return "n/a"


def retrieval_question_to_serializable(q: RetrievalEvalQuestion) -> dict[str, Any]:
    payload = asdict(q)
    payload["gold"] = asdict(q.gold)
    return payload


def build_retrieval_repo_section(agg: RepoRetrievalAgg) -> dict[str, Any]:
    per_q: list[dict[str, Any]] = []

    for q, dbg in agg.per_question:
        entry = {
            "question": q.question_text,
            "gold": asdict(q.gold),
            "display_path": q.file_path_display,
            "snapshot_path_abs": q.snapshot_path_abs,
            "top_retrieved_summaries": dbg.top_file_paths,
            "top1_correct": dbg.top1_correct,
            "recall_at_3_correct": dbg.recall_at_3_correct,
            "recall_at_5_correct": dbg.recall_at_5_correct,
            "per_rank_match_detail": dbg.matching_rules_used,
            "question_errors": dbg.errors,
            "fallback_note": (
                "Recall used file-path-only heuristic when retrieval payload lacked overlapping lines."
                if any("file_only_fallback_missing_metadata" in v for v in dbg.matching_rules_used.values())
                else None
            ),
        }
        per_q.append(entry)

    return {
        "repo_id": agg.repo_id,
        "repo_name": agg.repo_name,
        "num_questions": agg.num_questions,
        "top1_accuracy_pct": agg.top1_accuracy_pct,
        "recall_at_3_pct": agg.recall_at_3_pct,
        "recall_at_5_pct": agg.recall_at_5_pct,
        "per_question": per_q,
    }


def summarize_answer(rows: list[AnswerEvalRow]) -> dict[str, float | None]:
    rel = [row.relevancy_score for row in rows if isinstance(row.relevancy_score, (int, float))]
    fai = [
        row.faithfulness_score
        for row in rows
        if isinstance(row.faithfulness_score, (int, float))
    ]
    return {
        "avg_answer_relevancy_score": round(sum(rel) / len(rel), 4) if rel else None,
        "avg_faithfulness_score": round(sum(fai) / len(fai), 4) if fai else None,
    }


def build_report_payload(
    *,
    repos_config_path: Path,
    max_questions_per_repo: int,
    retrieval_agg: dict[str, Any] | None,
    answers: dict[str, Any] | None,
    global_errors: list[str],
) -> dict[str, Any]:
    retrieval_summary = retrieval_agg["summary"] if retrieval_agg else None
    retrieval_per_repo = retrieval_agg["repos"] if retrieval_agg else []

    summary_block = {
        "metric_definitions": {
            "top_1_accuracy": "% of queries where rank-1 chunk matches Architecture rules.",
            "recall_at_3": "% of queries where ANY of top 3 chunks match.",
            "recall_at_5": "% of queries where ANY of top 5 chunks match.",
            "matching_rules": [
                ("file_line_overlap", "Same normalized path + overlapping line spans."),
                ("file_symbol_match", "Same path + identical symbol identifiers."),
                ("file_only_fallback_missing_metadata", "Either side lacked spans needed for overlap."),
            ],
        },
        "deepeval_metrics": (
            answers.get("deepeval_description")
            if answers
            else "AnswerRelevancyMetric + FaithfulnessMetric (skipped if --skip-deepeval)."
        ),
    }

    return {
        "meta": {
            "generated_at": _iso_timestamp(),
            "repos_config_path": str(repos_config_path.resolve()),
            "max_questions_per_repo": max_questions_per_repo,
            "timezone": "UTC",
        },
        "summary": summary_block,
        "retrieval": {
            "aggregate": retrieval_summary,
            "per_repository": retrieval_per_repo,
            "skipped": retrieval_agg is None,
        },
        "answers": answers or {"skipped": True},
        "errors_and_warnings": global_errors,
    }


def write_evaluation_reports(report: dict[str, Any], destination_dir: Path) -> tuple[Path, Path]:
    destination_dir.mkdir(parents=True, exist_ok=True)
    slug = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    json_path = destination_dir / f"evaluation_report_{slug}.json"
    md_path = destination_dir / f"evaluation_report_{slug}.md"

    import json as json_std

    with json_path.open("w", encoding="utf-8") as fh:
        json_std.dump(report, fh, indent=2, ensure_ascii=False)

    markdown = render_markdown_report(report)

    md_path.write_text(markdown, encoding="utf-8")
    latest_json = destination_dir / "evaluation_report_latest.json"
    latest_md = destination_dir / "evaluation_report_latest.md"
    latest_json.write_text(json_path.read_text(encoding="utf-8"), encoding="utf-8")
    latest_md.write_text(markdown, encoding="utf-8")

    return json_path, md_path


def render_markdown_report(report: dict[str, Any]) -> str:
    meta = report.get("meta", {})
    retrieval = report.get("retrieval") or {}
    answers = report.get("answers") or {}
    defs = (
        (((report.get("summary") or {}) or {}).get("metric_definitions") or {}).get(
            "matching_rules"
        )
    )

    md_lines = [
        "# Evaluation Report",
        "",
        "## Summary",
        "",
        f"- Generated at `{meta.get('generated_at')}` UTC",
        f"- Repo config `{meta.get('repos_config_path')}`",
        f"- Retrieval questions per repo capped at `{meta.get('max_questions_per_repo')}`",
        "",
        "### Retrieval metric definitions",
        "",
        "| Metric | Meaning |",
        "| --- | --- |",
        "| Top-1 accuracy | Queries where globally ranked retrieval #1 satisfies the Architecture.md match rules |",
        "| Recall@3 | Queries where positions 1-3 contain at least one match |",
        "| Recall@5 | Queries where positions 1-5 contain at least one match |",
        "",
    ]

    if defs:
        md_lines.extend(
            [
                "Match rule priority:",
                "",
            ]
            + [f"{idx + 1}. `{hint[0]}` → {hint[1]}" for idx, hint in enumerate(defs)]
            + [""]
        )

    retrieval_summary = retrieval.get("aggregate") or {}

    md_lines.extend(
        [
            "## Retrieval metrics",
            "",
        ]
    )

    if retrieval.get("skipped"):
        md_lines.append("_Retrieval metrics were skipped (`--answers-only`)._\n")
    else:
        macro_top1 = retrieval_summary.get("macro_top1_pct")
        macro_top1_display = _fmt_pct(macro_top1)
        macro_r3 = retrieval_summary.get("macro_recall_at_3_pct")
        macro_r3_display = _fmt_pct(macro_r3)
        macro_r5 = retrieval_summary.get("macro_recall_at_5_pct")
        macro_r5_display = _fmt_pct(macro_r5)
        md_lines.extend(
            [
                f"- Total generated questions: `{retrieval_summary.get('total_questions', 0)}`",
                f"- Macro Top-1: `{macro_top1_display}%`",
                f"- Macro Recall@3: `{macro_r3_display}%`",
                f"- Macro Recall@5: `{macro_r5_display}%`",
                "",
            ]
        )
        if retrieval_summary.get("per_repo"):
            md_lines.extend(["### Macro averages", "", "| Repo | Questions | Top-1 | Recall@3 | Recall@5 |"])
            md_lines.extend(["| --- | ---:| ---:| ---:| ---:|"])
            for row in retrieval_summary["per_repo"]:
                md_lines.append(
                    "| {repo_name} | {qcount} | {t1}% | {r3}% | {r5}% |".format(
                        repo_name=row.get("repo_name"),
                        qcount=int(row.get("num_questions", 0)),
                        t1=float(row.get("top1_pct", row.get("top1_accuracy_pct", 0))),
                        r3=float(row.get("recall_at_3_pct", row.get("r3_pct", 0))),
                        r5=float(row.get("recall_at_5_pct", row.get("r5_pct", 0))),
                    )
                )

        md_lines.extend(["", "## Per-repository retrieval details", ""])

        for repo_block in retrieval.get("per_repository", []):
            md_lines.extend(
                [
                    f"### {repo_block.get('repo_name')} (`{repo_block.get('repo_id')}`)",
                    "",
                    f"- Questions evaluated: `{repo_block.get('num_questions')}`",
                    (
                        "| Top-1 | Recall@3 | Recall@5 |"
                        f"\n| {repo_block.get('top1_accuracy_pct')}% "
                        f"| {repo_block.get('recall_at_3_pct')}% "
                        f"| {repo_block.get('recall_at_5_pct')}% |"
                        "\n"
                    ),
                ]
            )

            for q_detail in repo_block.get("per_question", []):
                md_lines.extend(
                    [
                        f"<details>",
                        "",
                        "",
                    ]
                )
                md_lines.append(f"- **Question:** {q_detail.get('question')}")
                md_lines.extend(
                    [
                        f"- **Gold:** `{q_detail.get('gold', {}).get('file_path_abs')}` :: "
                        f"`{q_detail.get('gold', {}).get('symbol_name')}`",
                        "",
                    ]
                )
                md_lines.append("- **Correctness:** ")
                md_lines.extend(
                    [
                        f"- top-1 ✅" if q_detail.get("top1_correct") else "- top-1 ❌",
                        f"- Recall@3 ✅" if q_detail.get("recall_at_3_correct") else "- Recall@3 ❌",
                        f"- Recall@5 ✅" if q_detail.get("recall_at_5_correct") else "- Recall@5 ❌",
                    ]
                )
                md_lines.append("")
                tops = "\n".join(f"  -- {snippet}" for snippet in q_detail.get("top_retrieved_summaries") or [])
                md_lines.extend(["Retrieved previews:", "```", tops, "```"])
                hints = (
                    "**Fallback heuristic used:** `_file_only_fallback_missing_metadata_` surfaced in diagnostics."
                    if q_detail.get("fallback_note")
                    else ""
                )
                if hints:
                    md_lines.extend(["", hints])
                errs = "\n".join(q_detail.get("question_errors") or [])
                if errs.strip():
                    md_lines.extend(["", "Errors:", "", "```text", errs, "```"])
                md_lines.append("")  # blank line spacer

                md_lines.append("</details>")
                md_lines.extend(["", "---", ""])

        md_lines.append("")

    md_lines.extend(["## Answer quality metrics", "", answers.get("_markdown_notes", "").strip()])
    avg_rel = answers.get("avg_answer_relevancy_score")
    avg_faith = answers.get("avg_faithfulness_score")
    md_lines.extend(
        [
            "",
            f"- Average AnswerRelevancyMetric: `{avg_rel}`",
            f"- Average FaithfulnessMetric: `{avg_faith}`",
            "",
        ]
    )

    md_lines.extend(["### Manual QA rows"])

    for idx, row in enumerate(answers.get("rows_rendered", []) or [], start=1):
        md_lines.extend(
            [
                f"{idx}. **{row.get('repo_name')}**: {row['question']}  ",
                "",
                "",
            ]
            + [
                "```",
                row.get("answer_preview", ""),
                "```",
                f"- AnswerRelevancy: `{row.get('answer_relevancy')}` ({row.get('answer_relevancy_reason')})",
                f"- Faithfulness: `{row.get('faithfulness')}` ({row.get('faithfulness_reason')})",
                "",
            ]
            + ([] if not row.get("errors_rendered") else ["Errors:", "```", row["errors_rendered"], "```", ""])
        )

    errs = "\n".join(report.get("errors_and_warnings") or [])
    md_lines.extend(
        [
            "## Failed questions / global errors",
            "",
            "```text",
            errs or "none",
            "```",
            "",
            "## Notes",
            "",
            'Results come from actual `retrieve_ranked_chunks` output (embedding → Qdrant → rerank without evidence truncation). ',
            "`FaithfulnessMetric` consumes the snippets pulled from Qdrant for the reproduced query after orchestration completes.",
            "",
        ]
    )

    cleaned = []

    prev_blank = False
    for line in md_lines:
        stripped = line.strip()
        # Drop consecutive blank lines aggressively
        if not stripped:
            if prev_blank:
                continue
            prev_blank = True
            cleaned.append("")
        else:
            prev_blank = False
            cleaned.append(line.rstrip())
    while cleaned and cleaned[0] == "":
        cleaned.pop(0)
    while cleaned and cleaned[-1] == "":
        cleaned.pop()
    cleaned.append("")  # final newline terminator
    return "\n".join(cleaned)
