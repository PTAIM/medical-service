from pydantic import BaseModel


class ImageAnalysisRequest(BaseModel):
    image_bytes: bytes
    mime_type: str


class ImageAnalysisResponse(BaseModel):
    analysis_text: str
