from fastapi import FastAPI, UploadFile
from typing import Dict
from dotenv import load_dotenv

from google_api import analyze_image
from get_logger import app_logger
# from analyze_image import analyze_image

load_dotenv()
# Create the FastAPI app instance
app = FastAPI()


@app.get("/")
def read_root() -> Dict[str, str]:
    """
    Root endpoint for the API.
    Returns a simple "Hello World" message.
    """
    return {"Hello": "World"}


@app.post("/analyze")
def analyze(image: UploadFile):
    """
    Analyze the uploaded image and return the results.
    """
    image_path = f"/tmp/{image.filename}"
    with open(image_path, "wb") as f:
        f.write(image.file.read())

    app_logger.info(f"Image saved to {image_path} for analysis.")
    result = analyze_image(image_path)
    return result


@app.get("/health")
def health_check() -> Dict[str, str]:
    """
    Health check endpoint.
    """
    return {"status": "healthy"}
