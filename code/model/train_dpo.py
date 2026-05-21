from __future__ import annotations

import os

import torch
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
)
from trl import DPOConfig, DPOTrainer

from config import (
    BitsAndBytesConfig as BnBCfg,
    DPO_DATASET_PATH,
    DPORunConfig,
    QLoRAConfig,
    SFT_MERGED_MODEL_PATH,
)
from dpo_data import load_dpo_dataset


def _build_bnb_config(cfg: BnBCfg) -> BitsAndBytesConfig:
    compute_dtype = getattr(torch, cfg.bnb_4bit_compute_dtype)
    return BitsAndBytesConfig(
        load_in_4bit=cfg.load_in_4bit,
        bnb_4bit_quant_type=cfg.bnb_4bit_quant_type,
        bnb_4bit_compute_dtype=compute_dtype,
        bnb_4bit_use_double_quant=cfg.bnb_4bit_use_double_quant,
    )


def _build_lora_config(cfg: QLoRAConfig) -> LoraConfig:
    return LoraConfig(
        r=cfg.lora_r,
        lora_alpha=cfg.lora_alpha,
        lora_dropout=cfg.lora_dropout,
        target_modules=cfg.target_modules,
        task_type=cfg.task_type,
        bias=cfg.bias,
    )


def _build_training_args(cfg: DPORunConfig) -> DPOConfig:
    return DPOConfig(
        output_dir=cfg.output_dir,
        num_train_epochs=cfg.num_train_epochs,
        per_device_train_batch_size=cfg.per_device_train_batch_size,
        gradient_accumulation_steps=cfg.gradient_accumulation_steps,
        learning_rate=cfg.learning_rate,
        lr_scheduler_type=cfg.lr_scheduler_type,
        warmup_ratio=cfg.warmup_ratio,
        beta=cfg.beta,
        max_length=cfg.max_length,
        max_prompt_length=cfg.max_prompt_length,
        fp16=cfg.fp16,
        bf16=cfg.bf16,
        logging_steps=cfg.logging_steps,
        save_steps=cfg.save_steps,
        save_total_limit=cfg.save_total_limit,
        seed=cfg.seed,
        gradient_checkpointing=cfg.gradient_checkpointing,
        optim=cfg.optim,
        report_to=cfg.report_to,
    )


def train() -> None:
    """Run DPO on top of the SFT-merged model with a fresh LoRA adapter."""
    if not DPO_DATASET_PATH:
        raise ValueError("Set DPO_DATASET_PATH to the JSONL produced by export_preferences.py.")
    if not os.path.isdir(SFT_MERGED_MODEL_PATH):
        raise ValueError(
            f"SFT_MERGED_MODEL_PATH does not exist: {SFT_MERGED_MODEL_PATH}. "
            "Run merge_adapter.py first to produce the SFT-merged base."
        )

    run_cfg = DPORunConfig()
    bnb_cfg = BnBCfg()
    qlora_cfg = QLoRAConfig()

    print(f"Loading tokenizer from {SFT_MERGED_MODEL_PATH}")
    tokenizer = AutoTokenizer.from_pretrained(SFT_MERGED_MODEL_PATH, trust_remote_code=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    print(f"Loading SFT-merged base with 4-bit quantisation from {SFT_MERGED_MODEL_PATH}")
    model = AutoModelForCausalLM.from_pretrained(
        SFT_MERGED_MODEL_PATH,
        quantization_config=_build_bnb_config(bnb_cfg),
        device_map="auto",
        trust_remote_code=True,
    )
    model = prepare_model_for_kbit_training(model)

    lora_config = _build_lora_config(qlora_cfg)
    model = get_peft_model(model, lora_config)
    model.print_trainable_parameters()

    dataset = load_dpo_dataset(
        DPO_DATASET_PATH,
        tokenizer,
        max_samples=run_cfg.max_train_samples,
    )

    training_args = _build_training_args(run_cfg)
    trainer = DPOTrainer(
        model=model,
        ref_model=None,
        args=training_args,
        train_dataset=dataset,
        processing_class=tokenizer,
    )

    print("Starting DPO training")
    trainer.train()

    adapter_path = os.path.join(run_cfg.output_dir, "final_adapter")
    trainer.save_model(adapter_path)
    tokenizer.save_pretrained(adapter_path)
    print(f"DPO adapter saved to {adapter_path}")


if __name__ == "__main__":
    train()
