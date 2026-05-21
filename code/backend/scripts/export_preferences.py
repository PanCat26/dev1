from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from database.session import engine
from repository_management.models.feedback import RLHFFeedback


MIN_RESPONSE_CHARS = 10


def export(out_path: Path, limit: int | None = None) -> int:
    """Export finalized rlhf_feedback rows to JSONL. Returns rows written."""
    stmt = (
        select(RLHFFeedback)
        .where(RLHFFeedback.chosen_response.is_not(None))
        .where(RLHFFeedback.rejected_response.is_not(None))
        .where(RLHFFeedback.chosen_response != RLHFFeedback.rejected_response)
        .where(func.char_length(RLHFFeedback.chosen_response) >= MIN_RESPONSE_CHARS)
        .where(func.char_length(RLHFFeedback.rejected_response) >= MIN_RESPONSE_CHARS)
        .order_by(RLHFFeedback.created_at.asc())
    )
    if limit is not None:
        stmt = stmt.limit(limit)

    out_path.parent.mkdir(parents=True, exist_ok=True)

    written = 0
    skipped = 0
    with Session(engine) as session, out_path.open("w", encoding="utf-8") as f:
        for fb in session.scalars(stmt):
            try:
                messages = json.loads(fb.prompt or "")
            except json.JSONDecodeError:
                skipped += 1
                continue
            if not isinstance(messages, list) or not messages:
                skipped += 1
                continue

            obj = {
                "id": str(fb.id),
                "repo_id": str(fb.repository_id),
                "created_at": fb.created_at.isoformat() if fb.created_at else None,
                "prompt": messages,
                "chosen": fb.chosen_response,
                "rejected": fb.rejected_response,
            }
            f.write(json.dumps(obj, ensure_ascii=False) + "\n")
            written += 1

    print(f"Wrote {written} pair(s) to {out_path} (skipped {skipped} malformed row(s))")
    return written


def main():
    parser = argparse.ArgumentParser(
        description="Export DPO preference triples (prompt, chosen, rejected) from rlhf_feedback to JSONL."
    )
    parser.add_argument(
        "--out", type=str, default=None,
        help="Output JSONL path. Default: storage/preferences/dpo_<UTC-timestamp>.jsonl",
    )
    parser.add_argument(
        "--limit", type=int, default=None,
        help="Optional cap on number of rows.",
    )
    args = parser.parse_args()

    if args.out is None:
        ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        out_path = ROOT / "storage" / "preferences" / f"dpo_{ts}.jsonl"
    else:
        out_path = Path(args.out)

    export(out_path, limit=args.limit)


if __name__ == "__main__":
    main()
