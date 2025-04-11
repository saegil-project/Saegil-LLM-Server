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
    PROJECT_NAME: str = "텍스트-음성 및 음성-텍스트 변환 API"
    PROJECT_DESCRIPTION: str = "ElevenLabs를 사용하여 텍스트 쿼리를 음성으로 변환하고, OpenAI를 사용하여 음성을 텍스트로 변환하는 API"
    VERSION: str = "1.0.0"

    # ElevenLabs settings
    ELEVENLABS_API_KEY: str = Field(default_factory=lambda: os.getenv("ELEVENLABS_API_KEY", ""))
    ELEVENLABS_VOICE_ID: str = Field(
        default_factory=lambda: os.getenv("ELEVENLABS_VOICE_ID", "uyVNoMrnUku1dZyVEXwD"))  # Adam pre-made voice
    ELEVENLABS_MODEL_ID: str = Field(default_factory=lambda: os.getenv("ELEVENLABS_MODEL_ID", "eleven_flash_v2_5"))

    # OpenAI settings
    OPENAI_API_KEY: str = Field(default_factory=lambda: os.getenv("OPENAI_API_KEY", ""))
    OPENAI_MODEL: str = Field(default_factory=lambda: os.getenv("OPENAI_MODEL", "whisper-1"))
    OPENAI_CHAT_MODEL: str = Field(default_factory=lambda: os.getenv("OPENAI_CHAT_MODEL", "gpt-4o"))

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
