from fastapi import APIRouter, Depends, HTTPException, UploadFile, File

from app.core.config import settings
from app.dependencies import get_speech_to_text_service
from app.models.speech_to_text import AudioQuery, TranscriptionResult
from app.services.speech_to_text_service import SpeechToTextService

router = APIRouter(prefix="/speech-to-text", tags=["speech-to-text"])


@router.post("/audio-url", response_model=TranscriptionResult, summary="오디오 URL에서 음성을 텍스트로 변환")
async def convert_speech_to_text(
        query: AudioQuery,
        stt_service: SpeechToTextService = Depends(get_speech_to_text_service)
):
    try:
        text = stt_service.speech_to_text(str(query.audio_url))
        return TranscriptionResult(text=text)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"음성을 텍스트로 변환하는 중 오류 발생: {str(e)}"
        )


@router.post("/upload", response_model=TranscriptionResult, summary="오디오 파일 업로드로 음성을 텍스트로 변환")
async def convert_speech_to_text_from_file(
        file: UploadFile = File(...),
        stt_service: SpeechToTextService = Depends(get_speech_to_text_service)
):
    try:
        if not file.content_type or not file.content_type.startswith("audio/"):
            raise HTTPException(
                status_code=400,
                detail="오디오 파일만 업로드할 수 있습니다."
            )

        text = await stt_service.speech_to_text_from_file(file)
        return TranscriptionResult(text=text)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"업로드된 오디오를 텍스트로 변환하는 중 오류 발생: {str(e)}"
        )
