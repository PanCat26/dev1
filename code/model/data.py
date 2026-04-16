from __future__ import annotations

import logging
from typing import Optional

from datasets import Dataset, load_dataset

from config import SFT_DATASET


logger = logging.getLogger(__name__)


def _format_opencode_instruct(example: dict) -> dict:
    """Convert an OpenCodeInstruct sample to a chat-template messages list.
    """
    instruction = example.get("input", "")
    response = example.get("output", "")

    messages = [
        {"role": "user", "content": instruction},
        {"role": "assistant", "content": response},
    ]
    return {"messages": messages}


def load_sft_dataset(
    *,
    max_samples: Optional[int] = None,
    streaming: bool = False,
) -> Dataset:
    """Load and format the SFT training dataset.

    Parameters
    ----------
    max_samples:
        Cap the total number of training rows. ``None`` means use the
        full dataset.
    streaming:
        If ``True``, the dataset is loaded in streaming mode.
    """
    logger.info("Loading SFT dataset: %s", SFT_DATASET)
    dataset = load_dataset(SFT_DATASET, split="train", streaming=streaming)

    dataset = dataset.map(
        _format_opencode_instruct,
        remove_columns=dataset.column_names if not streaming else None,
    )

    if max_samples is not None and not streaming:
        dataset = dataset.select(range(min(max_samples, len(dataset))))

    logger.info("SFT dataset ready - %s samples", len(dataset) if not streaming else "streaming")
    return dataset
