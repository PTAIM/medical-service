from fastapi import FastAPI, UploadFile
from typing import Dict
from dotenv import load_dotenv

from gemini_api import analyze_image

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

    result = analyze_image(image_path)
    return {"result": result}


@app.get("/health")
def health_check() -> Dict[str, str]:
    """
    Health check endpoint.
    """
    return {"status": "healthy"}
