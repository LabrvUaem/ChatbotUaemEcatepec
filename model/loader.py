import torch
from transformers import pipeline
from config.settings import MODEL_ID

pipe = pipeline(
    "text-generation",
    model=MODEL_ID,
    torch_dtype=torch.bfloat16,
    device_map="auto",
    return_full_text=False
)