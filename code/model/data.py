from __future__ import annotations

from typing import Optional

from datasets import IterableDataset, load_dataset, load_dataset_builder

from config import SFT_DATASET


def _format_opencode_instruct(example: dict) -> dict:
    """Convert an OpenCodeInstruct sample to a chat-template messages list."""
    instruction = example.get("input", "")
    response = example.get("output", "")

    messages = [
        {"role": "user", "content": instruction},
        {"role": "assistant", "content": response},
    ]
    return {"messages": messages}


def get_train_num_examples() -> int:
    """Return the declared size of the train split."""
    builder = load_dataset_builder(SFT_DATASET)
    return builder.info.splits["train"].num_examples


def load_sft_dataset(
    *,
    max_samples: Optional[int] = None,
) -> IterableDataset:
    """Load and format the SFT dataset in streaming mode."""
    print("Loading SFT dataset in streaming mode: %s", SFT_DATASET)
    dataset = load_dataset(SFT_DATASET, split="train", streaming=True)

    dataset = dataset.map(_format_opencode_instruct)

    if max_samples is not None:
        dataset = dataset.take(max_samples)

    print(
        "SFT dataset ready - %s",
        f"streaming (capped at {max_samples} samples)"
        if max_samples is not None
        else "streaming full dataset",
    )
    return dataset
