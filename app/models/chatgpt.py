"""
ChatGPT 기능을 위한 Pydantic 모델.
"""
from pydantic import BaseModel, Field, HttpUrl


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


class ChatGPTSttQuery(BaseModel):
    """
    음성에서 변환된 텍스트를 ChatGPT에게 전달하기 위한 모델.
    """
    audio_text: str = Field(..., description="음성에서 변환된 텍스트 쿼리")

    model_config = {
        "json_schema_extra": {
            "example": {
                "audio_text": "오늘 날씨가 어떤가요?"
            }
        }
    }


class ChatGPTAudioUrlQuery(BaseModel):
    """
    오디오 URL을 ChatGPT 처리를 위해 전달하기 위한 모델.
    """
    audio_url: HttpUrl = Field(..., description="텍스트로 변환할 오디오 파일의 URL")

    model_config = {
        "json_schema_extra": {
            "example": {
                "audio_url": "https://example.com/audio/sample.mp3"
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


