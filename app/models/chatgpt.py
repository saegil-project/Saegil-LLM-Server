"""
ChatGPT 기능을 위한 Pydantic 모델.
"""
from pydantic import BaseModel, Field


class ChatGPTQuery(BaseModel):
    """
    ChatGPT 요청을 위한 모델.
    """
    text: str = Field(..., description="ChatGPT에게 보낼 텍스트 쿼리")

    model_config = {
        "json_schema_extra": {
            "example": {
                "text": "안녕하세요, 오늘 날씨가 어떤가요?"
            }
        }
    }


class ChatGPTResponse(BaseModel):
    """
    ChatGPT 응답을 위한 모델.
    """
    response: str = Field(..., description="ChatGPT의 응답 텍스트")
    text: str = Field(None, description="STT로 변환된 원본 텍스트")

    model_config = {
        "json_schema_extra": {
            "example": {
                "response": "안녕하세요! 오늘 날씨는 지역에 따라 다를 수 있습니다. 특정 지역을 알려주시면 더 정확한 정보를 제공해 드릴 수 있습니다.",
                "text": "오늘 날씨가 어떤가요?"
            }
        }
    }


class STTChatGPTQuery(BaseModel):
    """
    STT로 변환된 텍스트를 ChatGPT에게 보내기 위한 모델.
    """
    audio_text: str = Field(..., description="STT로 변환된 텍스트")

    model_config = {
        "json_schema_extra": {
            "example": {
                "audio_text": "오늘 날씨가 어떤가요?"
            }
        }
    }
