"""
음성-텍스트 변환 기능을 위한 API 라우트.
"""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File

from app.dependencies import get_speech_to_text_service
from app.models.speech_to_text import AudioQuery, TranscriptionResult
from app.services.speech_to_text_service import SpeechToTextService

# 라우터 경로를 /api/v1/speech-to-text로 변경
router = APIRouter(prefix="/api/v1/speech-to-text", tags=["speech-to-text"])


@router.post("/audio-url", response_model=TranscriptionResult, summary="오디오 URL에서 음성을 텍스트로 변환")
async def convert_speech_to_text(
        query: AudioQuery,
        stt_service: SpeechToTextService = Depends(get_speech_to_text_service)
):
    """
    오디오 URL에서 음성을 텍스트로 변환합니다.

    Args:
        query: 텍스트로 변환할 오디오 쿼리
        stt_service: 음성-텍스트 변환 서비스 (주입됨)

    Returns:
        변환된 텍스트가 포함된 응답

    Raises:
        HTTPException: 음성을 텍스트로 변환하는 중 오류가 발생한 경우
    """
    try:
        # 서비스를 사용하여 음성을 텍스트로 변환
        text = stt_service.speech_to_text(str(query.audio_url))

        # 변환된 텍스트 반환
        return TranscriptionResult(text=text)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"음성을 텍스트로 변환하는 중 오류 발생: {str(e)}"
        )


@router.post("/upload", response_model=TranscriptionResult, summary="MP3 파일 업로드로 음성을 텍스트로 변환")
async def convert_speech_to_text_from_file(
        file: UploadFile = File(...),
        stt_service: SpeechToTextService = Depends(get_speech_to_text_service)
):
    """
    업로드된 MP3 파일에서 음성을 텍스트로 변환합니다.

    Args:
        file: 텍스트로 변환할 오디오 파일 (MP3 형식)
        stt_service: 음성-텍스트 변환 서비스 (주입됨)

    Returns:
        변환된 텍스트가 포함된 응답

    Raises:
        HTTPException: 음성을 텍스트로 변환하는 중 오류가 발생한 경우
    """
    try:
        # 파일 유형 확인
        if not file.content_type.startswith("audio/"):
            raise HTTPException(
                status_code=400,
                detail="오디오 파일만 업로드할 수 있습니다."
            )

        # 서비스를 사용하여 음성을 텍스트로 변환
        text = await stt_service.speech_to_text_from_file(file)

        # 변환된 텍스트 반환
        return TranscriptionResult(text=text)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"업로드된 오디오를 텍스트로 변환하는 중 오류 발생: {str(e)}"
        )
