"""
텍스트-음성 변환 기능을 위한 Pydantic 모델.
"""
from typing import Literal

from pydantic import BaseModel, Field


class TextQuery(BaseModel):
    """
    텍스트-음성 변환 요청을 위한 모델.
    """
    text: str = Field(..., description="음성으로 변환할 텍스트")
    provider: Literal["elevenlabs", "openai"] = Field(
        default="openai",
        description="사용할 음성 제공자 (elevenlabs 또는 openai)"
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "text": "안녕하세요, 이것은 음성으로 변환할 샘플 텍스트입니다.",
                "provider": "openai"
            }
        }
    }
