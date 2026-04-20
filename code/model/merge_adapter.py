from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
import torch

from config import (
    BASE_MODEL_ID,
    ADAPTER_REPO,
    DEFAULT_MERGED_OUTPUT,
)

if ADAPTER_REPO is None:
    raise ValueError("Set ADAPTER_REPO to a Hugging Face repo id or local adapter path.")

tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL_ID, trust_remote_code=True)

base_model = AutoModelForCausalLM.from_pretrained(
    BASE_MODEL_ID,
    torch_dtype=torch.float16,
    trust_remote_code=True,
)

model = PeftModel.from_pretrained(base_model, ADAPTER_REPO)
model = model.merge_and_unload()

model.save_pretrained(DEFAULT_MERGED_OUTPUT, safe_serialization=True)
tokenizer.save_pretrained(DEFAULT_MERGED_OUTPUT)
