"""
음성-텍스트 변환 기능을 위한 Pydantic 모델.
"""
from pydantic import BaseModel, Field, HttpUrl


class AudioQuery(BaseModel):
    """
    음성-텍스트 변환 요청을 위한 모델.
    """
    audio_url: HttpUrl = Field(..., description="텍스트로 변환할 오디오 파일의 URL")

    model_config = {
        "json_schema_extra": {
            "example": {
                "audio_url": "https://example.com/audio/sample.mp3"
            }
        }
    }


class AudioFileInfo(BaseModel):
    """
    업로드된 MP3 파일 정보를 위한 모델.
    """
    filename: str = Field(..., description="업로드된 오디오 파일의 이름")
    content_type: str = Field(..., description="파일의 MIME 타입")

    model_config = {
        "json_schema_extra": {
            "example": {
                "filename": "recording.mp3",
                "content_type": "audio/mpeg"
            }
        }
    }


class TranscriptionResult(BaseModel):
    """
    음성-텍스트 변환 결과를 위한 모델.
    """
    text: str = Field(..., description="변환된 텍스트")

    model_config = {
        "json_schema_extra": {
            "example": {
                "text": "안녕하세요, 이것은 음성에서 변환된 텍스트입니다."
            }
        }
    }
