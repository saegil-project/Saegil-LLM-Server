"""
Pydantic models for text-to-speech functionality.
"""
from pydantic import BaseModel, Field


class TextQuery(BaseModel):
    """
    Model for text-to-speech request.
    """
    text: str = Field(..., description="Text to convert to speech")

    class Config:
        schema_extra = {
            "example": {
                "text": "Hello, this is a sample text to convert to speech."
            }
        }
