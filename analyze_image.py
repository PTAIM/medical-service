from typing import Dict
from PIL import Image
from get_logger import app_logger
from setup_model import setup_model


def analyze_image(image_path: str) -> Dict[str, float]:
    pipe = setup_model()
    app_logger.info(f"Analyzing image at {image_path}.")
    image = Image.open(image_path)

    if image is None:
        app_logger.error(f"Failed to open image at {image_path}.")
        return {}

    messages = [
        {
            "role": "system",
            "content": [{"type": "text", "text": "You are an expert radiologist."}],
        },
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Describe this X-ray"},
                {"type": "image", "image": image},
            ],
        },
    ]

    result = pipe(text=messages, max_new_tokens=200)
    return result[0]["generated_text"][-1]["content"]
