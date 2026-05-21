from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
import torch

from config import (
    DEFAULT_DPO_MERGED_OUTPUT,
    DPO_ADAPTER_REPO,
    SFT_MERGED_MODEL_PATH,
)

if DPO_ADAPTER_REPO is None:
    raise ValueError("Set DPO_ADAPTER_REPO to a Hugging Face repo id or local DPO adapter path.")

tokenizer = AutoTokenizer.from_pretrained(SFT_MERGED_MODEL_PATH, trust_remote_code=True)

base_model = AutoModelForCausalLM.from_pretrained(
    SFT_MERGED_MODEL_PATH,
    torch_dtype=torch.float16,
    trust_remote_code=True,
)

model = PeftModel.from_pretrained(base_model, DPO_ADAPTER_REPO)
model = model.merge_and_unload()

model.save_pretrained(DEFAULT_DPO_MERGED_OUTPUT, safe_serialization=True)
tokenizer.save_pretrained(DEFAULT_DPO_MERGED_OUTPUT)
