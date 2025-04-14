"""
STT-ChatGPT-TTS 통합 기능을 위한 Pydantic 모델.
"""
from pydantic import BaseModel, Field


class STTChatGPTTTSResponse(BaseModel):
    """
    STT-ChatGPT-TTS 통합 응답을 위한 모델.
    """
    text: str = Field(..., description="STT로 변환된 원본 텍스트")
    response: str = Field(..., description="ChatGPT의 응답 텍스트")
    audio_url: str = Field(..., description="TTS로 생성된 오디오 파일의 URL")

    model_config = {
        "json_schema_extra": {
            "example": {
                "text": "오늘 날씨가 어떤가요?",
                "response": "안녕하세요! 오늘 날씨는 지역에 따라 다를 수 있습니다. 특정 지역을 알려주시면 더 정확한 정보를 제공해 드릴 수 있습니다.",
                "audio_url": "/stt-chatgpt-tts/audio/response.mp3"
            }
        }
    }
