from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal


@dataclass(frozen=True)
class GoldSymbolTarget:

    file_path_abs: str
    symbol_name: str
    symbol_type: Literal["function", "class", "method"]
    start_line: int
    end_line: int


@dataclass
class RetrievalEvalQuestion:

    repo_id: str
    repo_name: str
    commit_sha: str | None
    snapshot_path_abs: str
    question_text: str
    gold: GoldSymbolTarget

    file_path_display: str
    """Path relative to snapshot root for human-readable reports."""

    retrieval_used_file_only_fallback: bool = False
    notes: list[str] = field(default_factory=list)


@dataclass
class RetrievalSingleResultDebug:
    top_file_paths: list[str]
    top1_correct: bool
    recall_at_3_correct: bool
    recall_at_5_correct: bool
    matching_rules_used: dict[str, str]
    errors: list[str] = field(default_factory=list)


@dataclass
class RepoRetrievalAgg:
    repo_id: str
    repo_name: str
    num_questions: int
    top1_accuracy_pct: float
    recall_at_3_pct: float
    recall_at_5_pct: float
    per_question: list[tuple[RetrievalEvalQuestion, RetrievalSingleResultDebug]]


@dataclass
class AnswerEvalRow:
    repo_id: str
    repo_name: str
    question: str
    answer_text: str
    relevancy_score: float | None
    faithfulness_score: float | None
    relevancy_reason: str | None = None
    faithfulness_reason: str | None = None
    errors: list[str] = field(default_factory=list)


EvalReportDict = dict[str, Any]

