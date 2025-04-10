"""
Configuration settings for the application.
"""
import os

from pydantic import Field, BaseModel


class Settings(BaseModel):
    """
    Application settings.
    """
    # API settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Text-to-Speech API"
    PROJECT_DESCRIPTION: str = "API that converts text queries to speech using ElevenLabs"
    VERSION: str = "1.0.0"

    # ElevenLabs settings
    ELEVENLABS_API_KEY: str = Field(default_factory=lambda: os.getenv("ELEVENLABS_API_KEY", ""))
    ELEVENLABS_VOICE_ID: str = Field(
        default_factory=lambda: os.getenv("ELEVENLABS_VOICE_ID", "uyVNoMrnUku1dZyVEXwD"))  # Adam pre-made voice
    ELEVENLABS_MODEL_ID: str = Field(default_factory=lambda: os.getenv("ELEVENLABS_MODEL_ID", "eleven_flash_v2_5"))

    model_config = {
        "env_file": ".env",
        "case_sensitive": True
    }


# Load environment variables from .env file
try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

# Create global settings object
settings = Settings()
