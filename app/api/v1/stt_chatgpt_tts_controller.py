"""
STT-ChatGPT-TTS 통합 기능을 위한 API 라우트.
"""
import uuid

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import StreamingResponse

from app.core.config import settings
from app.dependencies import get_speech_to_text_service, get_chatgpt_service, get_text_to_speech_service
from app.models.stt_chatgpt_tts import STTChatGPTTTSResponse
from app.services.chatgpt_service import ChatGPTService
from app.services.speech_to_text_service import SpeechToTextService
from app.services.text_to_speech_service import TextToSpeechService

# 라우터 경로에서 기본 경로만 지정하고 API_V1_STR은 main.py에서 처리되도록 수정
router = APIRouter(prefix="/stt-chatgpt-tts", tags=["stt-chatgpt-tts"])


@router.post("/upload", summary="음성 파일 업로드로 STT-ChatGPT-TTS 통합 처리")
async def process_stt_chatgpt_tts_from_upload(
        file: UploadFile = File(...),
        stt_service: SpeechToTextService = Depends(get_speech_to_text_service),
        chatgpt_service: ChatGPTService = Depends(get_chatgpt_service),
        tts_service: TextToSpeechService = Depends(get_text_to_speech_service)
):
    """
    업로드된 음성 파일을 처리하여 다음 단계를 수행합니다:
    1. 음성을 텍스트로 변환 (STT)
    2. 텍스트를 ChatGPT에 전송하여 응답 생성
    3. ChatGPT 응답을 음성으로 변환 (TTS)
    4. 오디오 응답 반환

    Args:
        file: 텍스트로 변환할 오디오 파일(MP3, M4A 등 형식)
        stt_service: 음성-텍스트 변환 서비스 (주입됨)
        chatgpt_service: ChatGPT 서비스 (주입됨)
        tts_service: 텍스트-음성 변환 서비스 (주입됨)

    Returns:
        오디오 데이터가 포함된 스트리밍 응답

    Raises:
        HTTPException: 처리 중 오류가 발생한 경우
    """
    try:
        # 파일 유형 확인
        if not file.content_type.startswith("audio/"):
            raise HTTPException(
                status_code=400,
                detail="오디오 파일만 업로드할 수 있습니다."
            )

        # 1. 음성을 텍스트로 변환 (STT)
        text = await stt_service.speech_to_text_from_file(file)

        # 2. 텍스트를 ChatGPT에 전송하여 응답 생성
        response_text = chatgpt_service.get_response(text)

        # 3. ChatGPT 응답을 음성으로 변환 (TTS)
        audio_stream = tts_service.text_to_speech_stream(response_text)

        # 4. 오디오 응답 반환
        return StreamingResponse(
            audio_stream,
            media_type="audio/mpeg",
            headers={
                "Content-Disposition": "attachment; filename=response.mp3"
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"STT-ChatGPT-TTS 처리 중 오류 발생: {str(e)}"
        )


@router.post("/upload/json", response_model=STTChatGPTTTSResponse, summary="음성 파일 업로드로 STT-ChatGPT-TTS 통합 처리 (JSON 응답)")
async def process_stt_chatgpt_tts_from_upload_json(
        file: UploadFile = File(...),
        stt_service: SpeechToTextService = Depends(get_speech_to_text_service),
        chatgpt_service: ChatGPTService = Depends(get_chatgpt_service),
        tts_service: TextToSpeechService = Depends(get_text_to_speech_service)
):
    """
    업로드된 음성 파일을 처리하여 다음 단계를 수행하고 JSON 응답을 반환합니다:
    1. 음성을 텍스트로 변환 (STT)
    2. 텍스트를 ChatGPT에 전송하여 응답 생성
    3. ChatGPT 응답을 음성으로 변환 (TTS)
    4. 텍스트 및 오디오 URL이 포함된 JSON 응답 반환

    Args:
        file: 텍스트로 변환할 오디오 파일(MP3, M4A 등 형식)
        stt_service: 음성-텍스트 변환 서비스 (주입됨)
        chatgpt_service: ChatGPT 서비스 (주입됨)
        tts_service: 텍스트-음성 변환 서비스 (주입됨)

    Returns:
        텍스트, 응답 및 오디오 URL이 포함된 JSON 응답

    Raises:
        HTTPException: 처리 중 오류가 발생한 경우
    """
    try:
        # 파일 유형 확인
        if not file.content_type.startswith("audio/"):
            raise HTTPException(
                status_code=400,
                detail="오디오 파일만 업로드할 수 있습니다."
            )

        # 1. 음성을 텍스트로 변환 (STT)
        text = await stt_service.speech_to_text_from_file(file)

        # 2. 텍스트를 ChatGPT에 전송하여 응답 생성
        response_text = chatgpt_service.get_response(text)

        # 3. 오디오 URL 생성 (실제 구현에서는 오디오 파일을 저장하고 URL을 반환해야 함)
        audio_url = f"/stt-chatgpt-tts/audio/{uuid.uuid4()}.mp3"

        # 4. JSON 응답 반환
        return STTChatGPTTTSResponse(
            text=text,
            response=response_text,
            audio_url=audio_url
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"STT-ChatGPT-TTS 처리 중 오류 발생: {str(e)}"
        )
