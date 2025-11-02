# Load google/medgemma-4b-it-8k model from Hugging Face
from transformers import pipeline
import torch

model_name = "google/medgemma-4b-it"
# Identify device

device = "cuda" if torch.cuda.is_available() else "cpu"
pipe = None


def setup_model():
    global pipe

    if pipe is not None:
        return pipe
    pipe = pipeline(
        "image-text-to-text",
        model=model_name,
        torch_dtype=torch.bfloat16,
        device=device,
    )
    return pipe


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()
    setup_model()
