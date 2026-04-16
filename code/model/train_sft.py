from __future__ import annotations

import logging
import os

import torch
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    TrainingArguments,
)
from trl import SFTTrainer

from config import (
    BASE_MODEL_ID,
    BitsAndBytesConfig as BnBCfg,
    QLoRAConfig,
    SFTRunConfig,
)
from data import load_sft_dataset


logger = logging.getLogger(__name__)


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


def _build_training_args(cfg: SFTRunConfig) -> TrainingArguments:
    return TrainingArguments(
        output_dir=cfg.output_dir,
        num_train_epochs=cfg.num_train_epochs,
        per_device_train_batch_size=cfg.per_device_train_batch_size,
        gradient_accumulation_steps=cfg.gradient_accumulation_steps,
        learning_rate=cfg.learning_rate,
        lr_scheduler_type=cfg.lr_scheduler_type,
        warmup_ratio=cfg.warmup_ratio,
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


def train():
    """Run SFT."""
    run_cfg = SFTRunConfig()
    bnb_cfg = BnBCfg()
    qlora_cfg = QLoRAConfig()

    # tokenizer
    logger.info("Loading tokenizer for %s", BASE_MODEL_ID)
    tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL_ID, trust_remote_code=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    # quantised base model
    logger.info("Loading base model with 4-bit quantisation")
    model = AutoModelForCausalLM.from_pretrained(
        BASE_MODEL_ID,
        quantization_config=_build_bnb_config(bnb_cfg),
        device_map="auto",
        trust_remote_code=True,
    )
    model = prepare_model_for_kbit_training(model)

    # LoRA adapter
    lora_config = _build_lora_config(qlora_cfg)
    model = get_peft_model(model, lora_config)
    model.print_trainable_parameters()

    # dataset
    dataset = load_sft_dataset(
        max_samples=run_cfg.max_train_samples,
    )

    # trainer
    training_args = _build_training_args(run_cfg)
    trainer = SFTTrainer(
        model=model,
        args=training_args,
        train_dataset=dataset,
        processing_class=tokenizer,
        max_seq_length=run_cfg.max_seq_length,
    )

    logger.info("Starting SFT training")
    trainer.train()

    # save adapter
    adapter_path = os.path.join(run_cfg.output_dir, "final_adapter")
    trainer.save_model(adapter_path)
    tokenizer.save_pretrained(adapter_path)
    logger.info("Adapter saved to %s", adapter_path)


if __name__ == "__main__":
    train()
