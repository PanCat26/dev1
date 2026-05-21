from __future__ import annotations

import os
from collections.abc import Callable
from typing import Iterable

from retrieval.types import RetrievedChunk

from evaluation.types import (
    GoldSymbolTarget,
    RepoRetrievalAgg,
    RetrievalEvalQuestion,
    RetrievalSingleResultDebug,
)


def normalize_path(abs_path: str) -> str:
    return os.path.normcase(os.path.normpath(os.path.abspath(abs_path)))


def _ranges_overlap(a_start: int, a_end: int, b_start: int, b_end: int) -> bool:
    if a_start <= 0 or b_start <= 0:
        return False
    ae = a_end if a_end >= a_start else a_start
    be = b_end if b_end >= b_start else b_start
    return not (ae < b_start or a_start > be)


def retrieval_chunk_matches_gold(candidate: RetrievedChunk, gold: GoldSymbolTarget) -> tuple[bool, str]:
    """Apply Architecture-style matching rules for one retrieved chunk."""

    gold_path_n = normalize_path(gold.file_path_abs)
    ret_path_n = normalize_path(candidate.file_path)
    if gold_path_n != ret_path_n:
        return False, "path_mismatch"

    gold_lines_ok = gold.start_line > 0 and gold.end_line >= gold.start_line
    ret_lines_ok = candidate.start_line > 0 and candidate.end_line >= candidate.start_line
    gs = gold.symbol_name.strip()
    cs = candidate.symbol_name.strip()

    if gold_lines_ok and ret_lines_ok:
        if _ranges_overlap(candidate.start_line, candidate.end_line, gold.start_line, gold.end_line):
            return True, "file_line_overlap"
        return False, "same_file_disjoint_lines"

    if gs and cs and gs == cs:
        return True, "file_symbol_match"

    return True, "file_only_fallback_missing_metadata"


RankedRetriever = Callable[[str, str, str | None, int], list[RetrievedChunk]]


def _describe_chunk(chunk: RetrievedChunk) -> str:
    gs = chunk.symbol_name.strip()
    loc = ""
    if chunk.start_line > 0 and chunk.end_line > 0:
        loc = f" L{chunk.start_line}-{chunk.end_line}"
    sym = f" [{gs}]" if gs else ""
    return f"{chunk.file_path}{loc}{sym}"


def evaluate_questions_retrieval(
    questions: Iterable[RetrievalEvalQuestion],
    *,
    ranked_fetcher: RankedRetriever,
    num_candidates: int = 50,
) -> RepoRetrievalAgg | None:
    """Compute Top-1 and Recall@{3,5} using globally ranked retrieval output."""

    qs = list(questions)
    if not qs:
        return None

    first = qs[0]
    repo_name = first.repo_name
    repo_id = first.repo_id

    per_question: list[tuple[RetrievalEvalQuestion, RetrievalSingleResultDebug]] = []
    top1_hits = 0
    r3_hits = 0
    r5_hits = 0

    for q in qs:
        errors: list[str] = []
        ranked: list[RetrievedChunk] = []

        try:
            ranked = ranked_fetcher(q.question_text.strip(), q.repo_id, q.commit_sha, num_candidates)
        except Exception as exc:  # noqa: BLE001 — eval harness tolerates infra issues
            errors.append(f"retrieval_failed: {exc}")

        match_labels_top5: dict[str, str] = {}
        if ranked:
            for idx in range(min(5, len(ranked))):
                hit, lbl = retrieval_chunk_matches_gold(ranked[idx], q.gold)
                match_labels_top5[f"rank_{idx + 1}"] = (
                    f"{_describe_chunk(ranked[idx])} -> {lbl} ({'hit' if hit else 'miss'})"
                )

        top_paths = [_describe_chunk(c) for c in ranked[: min(8, len(ranked))]]

        top1_correct = False
        r3_correct = False
        r5_correct = False

        if ranked:
            if retrieval_chunk_matches_gold(ranked[0], q.gold)[0]:
                top1_correct = True
            if any(
                retrieval_chunk_matches_gold(ranked[i], q.gold)[0] for i in range(min(3, len(ranked)))
            ):
                r3_correct = True
            if any(
                retrieval_chunk_matches_gold(ranked[i], q.gold)[0] for i in range(min(5, len(ranked)))
            ):
                r5_correct = True

        if top1_correct:
            top1_hits += 1
        if r3_correct:
            r3_hits += 1
        if r5_correct:
            r5_hits += 1

        pq = RetrievalSingleResultDebug(
            top_file_paths=top_paths,
            top1_correct=top1_correct,
            recall_at_3_correct=r3_correct,
            recall_at_5_correct=r5_correct,
            matching_rules_used=match_labels_top5,
            errors=errors,
        )
        per_question.append((q, pq))

    total = len(qs)

    def pct(hits: int) -> float:
        return round(100.0 * hits / total, 3) if total else 0.0

    return RepoRetrievalAgg(
        repo_id=repo_id,
        repo_name=repo_name,
        num_questions=total,
        top1_accuracy_pct=pct(top1_hits),
        recall_at_3_pct=pct(r3_hits),
        recall_at_5_pct=pct(r5_hits),
        per_question=per_question,
    )
