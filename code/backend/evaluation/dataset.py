from __future__ import annotations

import os
from pathlib import Path

from indexing.parser import parse_python_file
from indexing.scanner import list_supported_files

from evaluation.types import GoldSymbolTarget, RetrievalEvalQuestion


def _should_skip_symbol(symbol_name: str, symbol_type: str) -> bool:
    """Skip private helpers, noisy dunder hooks, and class constructors."""

    leaf = symbol_name.split(".")[-1]
    if symbol_type == "method":
        if leaf == "__init__":
            return True
        known_magic = {
            "__repr__",
            "__str__",
            "__eq__",
            "__ne__",
            "__hash__",
            "__len__",
            "__getitem__",
            "__setitem__",
            "__delitem__",
            "__iter__",
            "__next__",
            "__enter__",
            "__exit__",
            "__call__",
            "__del__",
            "__await__",
        }
        if leaf in known_magic or (leaf.startswith("__") and leaf.endswith("__")):
            return True
        return leaf.startswith("_")

    if symbol_type in ("function", "class"):
        return leaf.startswith("_")

    return False


def _question_for(symbol_type: str, symbol_name: str) -> str:
    if symbol_type == "function":
        return f"Where is function `{symbol_name}` defined?"
    if symbol_type == "class":
        return f"In which file is class `{symbol_name}` defined?"
    if symbol_type == "method":
        return f"Where is method `{symbol_name}` implemented?"
    return f"Where is `{symbol_name}` defined?"


def generate_retrieval_questions(
    *,
    snapshot_path: str,
    repo_id: str,
    repo_name: str,
    commit_sha: str | None,
    max_questions_per_repo: int,
) -> tuple[list[RetrievalEvalQuestion], list[str]]:
    """Walk Python sources under snapshot_path and build deterministic QA items."""

    warnings: list[str] = []

    snap = Path(snapshot_path)
    resolved_root = snap.resolve()
    if not resolved_root.is_dir():
        warnings.append(f"Snapshot path is not a directory: {snapshot_path}")
        return [], warnings

    files = list_supported_files(str(resolved_root))
    py_files = [p for p in files if p.endswith(".py")]
    py_files.sort()

    candidates: list[RetrievalEvalQuestion] = []
    for fp in py_files:
        symbols = parse_python_file(fp)
        for sym in symbols:
            sym_type = sym.symbol_type
            if sym_type not in ("function", "class", "method"):
                continue
            if _should_skip_symbol(sym.symbol_name, sym_type):
                continue
            rel = os.path.relpath(sym.file_path, str(resolved_root))
            candidates.append(
                RetrievalEvalQuestion(
                    repo_id=repo_id.strip(),
                    repo_name=repo_name,
                    commit_sha=(commit_sha or "").strip() or None,
                    snapshot_path_abs=str(resolved_root),
                    question_text=_question_for(sym_type, sym.symbol_name),
                    gold=GoldSymbolTarget(
                        file_path_abs=os.path.abspath(sym.file_path),
                        symbol_name=sym.symbol_name,
                        symbol_type=sym_type,  # type: ignore[arg-type]
                        start_line=sym.start_line,
                        end_line=sym.end_line,
                    ),
                    file_path_display=rel.replace("\\", "/"),
                )
            )

    candidates.sort(
        key=lambda q: (
            q.file_path_display,
            q.gold.symbol_type,
            q.gold.symbol_name,
            q.question_text,
        )
    )

    capped = candidates[: max(0, max_questions_per_repo)]
    if not capped and py_files:
        warnings.append("No retrieval questions emitted (all symbols filtered or none parsed).")

    return capped, warnings
