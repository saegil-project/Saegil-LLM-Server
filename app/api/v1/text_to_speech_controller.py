"""
텍스트-음성 변환 기능을 위한 API 라우트.
"""
from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse

from app.core.config import settings
from app.dependencies import get_text_to_speech_service
from app.models.text_to_speech import TextQuery
from app.services.text_to_speech_service import TextToSpeechService

# 라우터 경로에서 API_V1_STR 중복 제거하고 하위 경로만 지정
router = APIRouter(prefix="/text-to-speech", tags=["text-to-speech"])


@router.post("/", summary="텍스트를 음성으로 변환")
async def convert_text_to_speech(
        query: TextQuery,
        provider: Literal["elevenlabs", "openai"] = Query(default="openai", description="사용할 음성 제공자(요청 본문 provider 값 대체)"),
        tts_service: TextToSpeechService = Depends(get_text_to_speech_service)
):
    """
    텍스트를 음성으로 변환하고 오디오 스트림을 반환합니다.

    Args:
        query: 음성으로 변환할 텍스트 쿼리
        provider: 사용할 음성 제공자 ("elevenlabs" 또는 "openai"), 제공되면 query의 provider보다 우선함
        tts_service: 텍스트-음성 변환 서비스 (주입됨)

    Returns:
        오디오 데이터가 포함된 스트리밍 응답

    Raises:
        HTTPException: 텍스트를 음성으로 변환하는 중 오류가 발생한 경우
    """
    try:
        # 쿼리 파라미터로 전달된 provider가 있으면 그것을 사용하고, 그렇지 않으면 요청 본문의 provider를 사용
        active_provider = provider or query.provider
        
        # 서비스를 사용하여 텍스트를 음성으로 변환
        audio_stream = tts_service.text_to_speech_stream(query.text, provider=active_provider)

        # 오디오를 스트리밍 응답으로 반환
        return StreamingResponse(
            audio_stream,
            media_type="audio/mpeg",
            headers={
                "Content-Disposition": "attachment; filename=speech.mp3"
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"텍스트를 음성으로 변환하는 중 오류 발생: {str(e)}"
        )
