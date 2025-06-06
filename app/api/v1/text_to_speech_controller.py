from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse

from app.core.config import settings
from app.dependencies import get_text_to_speech_service
from app.models.text_to_speech import TextQuery
from app.services.text_to_speech_service import TextToSpeechService

router = APIRouter(prefix="/text-to-speech", tags=["text-to-speech"])


@router.post("/", summary="텍스트를 음성으로 변환")
async def convert_text_to_speech(
        query: TextQuery,
        provider: Literal["elevenlabs", "openai"] = Query(default="openai", description="사용할 음성 제공자"),
        tts_service: TextToSpeechService = Depends(get_text_to_speech_service)
):
    try:
        audio_stream = tts_service.text_to_speech_stream(query.text, provider=provider)

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
