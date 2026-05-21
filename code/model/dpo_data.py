from __future__ import annotations

import json
from typing import Optional

from datasets import Dataset
from transformers import PreTrainedTokenizerBase


def load_dpo_dataset(
    jsonl_path: str,
    tokenizer: PreTrainedTokenizerBase,
    *,
    max_samples: Optional[int] = None,
) -> Dataset:
    """Load a preference JSONL and render each prompt via the tokenizer's chat template."""
    print(f"Loading DPO dataset from {jsonl_path}")
    rows: list[dict] = []
    skipped = 0
    with open(jsonl_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
                messages = obj["prompt"]
                if not isinstance(messages, list) or not messages:
                    skipped += 1
                    continue
                prompt_str = tokenizer.apply_chat_template(
                    messages, tokenize=False, add_generation_prompt=True
                )
                rows.append({
                    "prompt": prompt_str,
                    "chosen": obj["chosen"],
                    "rejected": obj["rejected"],
                })
            except Exception:
                skipped += 1
                continue
            if max_samples is not None and len(rows) >= max_samples:
                break

    print(f"Loaded {len(rows)} DPO pair(s) (skipped {skipped})")
    return Dataset.from_list(rows)
