import os
from dataclasses import dataclass, field
from typing import Optional
from dotenv import load_dotenv

load_dotenv()


BASE_MODEL_ID = "Qwen/Qwen2.5-Coder-7B-Instruct"
ADAPTER_REPO = os.getenv("ADAPTER_REPO")

SFT_DATASET = "nvidia/OpenCodeInstruct"

DEFAULT_OUTPUT_DIR = "outputs"
DEFAULT_SFT_OUTPUT = os.path.join(DEFAULT_OUTPUT_DIR, "sft")
DEFAULT_MERGED_OUTPUT = os.path.join(DEFAULT_OUTPUT_DIR, "merged")
DEFAULT_DPO_OUTPUT = os.path.join(DEFAULT_OUTPUT_DIR, "dpo")
DEFAULT_DPO_MERGED_OUTPUT = os.path.join(DEFAULT_OUTPUT_DIR, "merged_dpo")

DPO_DATASET_PATH = os.getenv("DPO_DATASET_PATH")
DPO_ADAPTER_REPO = os.getenv("DPO_ADAPTER_REPO")
SFT_MERGED_MODEL_PATH = os.getenv("SFT_MERGED_MODEL_PATH", DEFAULT_MERGED_OUTPUT)


@dataclass
class QLoRAConfig:
    """QLoRA adapter hyper-parameters."""

    lora_r: int = 16
    lora_alpha: int = 16
    lora_dropout: float = 0.05
    target_modules: list[str] = field(
        default_factory=lambda: [
            "q_proj",
            "k_proj",
            "v_proj",
            "o_proj",
        ]
    )
    task_type: str = "CAUSAL_LM"
    bias: str = "none"


@dataclass
class BitsAndBytesConfig:
    """4-bit quantisation settings used by QLoRA."""

    load_in_4bit: bool = True
    bnb_4bit_quant_type: str = "nf4"
    bnb_4bit_compute_dtype: str = "bfloat16"
    bnb_4bit_use_double_quant: bool = True


@dataclass
class SFTRunConfig:
    """Training arguments for Supervised Fine-Tuning."""

    num_train_epochs: int = 1
    per_device_train_batch_size: int = 2
    gradient_accumulation_steps: int = 8
    learning_rate: float = 2e-4
    lr_scheduler_type: str = "cosine"
    warmup_ratio: float = 0.03
    max_seq_length: int = 1024
    fp16: bool = False
    bf16: bool = True
    logging_steps: int = 100
    save_steps: int = 1000
    save_total_limit: int = 3
    seed: int = 42
    output_dir: str = DEFAULT_SFT_OUTPUT
    gradient_checkpointing: bool = False
    optim: str = "paged_adamw_8bit"
    report_to: str = "none"
    max_train_samples: Optional[int] = 50000


@dataclass
class DPORunConfig:
    """Training arguments for Direct Preference Optimization."""

    num_train_epochs: int = 3
    per_device_train_batch_size: int = 1
    gradient_accumulation_steps: int = 8
    learning_rate: float = 5e-5
    lr_scheduler_type: str = "cosine"
    warmup_ratio: float = 0.1
    beta: float = 0.1
    max_length: int = 4096
    max_prompt_length: int = 3072
    fp16: bool = False
    bf16: bool = True
    logging_steps: int = 10
    save_steps: int = 200
    save_total_limit: int = 3
    seed: int = 42
    output_dir: str = DEFAULT_DPO_OUTPUT
    gradient_checkpointing: bool = True
    optim: str = "paged_adamw_8bit"
    report_to: str = "none"
    max_train_samples: Optional[int] = None
