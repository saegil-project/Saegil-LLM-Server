import logging
from typing import Literal, Optional

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query
from fastapi.responses import StreamingResponse

from app.core.config import settings
from app.dependencies import get_assistant_service, get_speech_to_text_service, get_text_to_speech_service
from app.models.assistant import AssistantQuery, AssistantResponse
from app.services.assistant_service import AssistantService
from app.services.speech_to_text_service import SpeechToTextService
from app.services.text_to_speech_service import TextToSpeechService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/assistant", tags=["assistant"])


def _validate_thread_id(thread_id: Optional[str]) -> Optional[str]:
    if thread_id and not thread_id.startswith("thread_"):
        logger.warning(f"잘못된 형식의 thread_id 수신: {thread_id}. None으로 처리합니다.")
        return None
    return thread_id


@router.post("/", response_model=AssistantResponse, summary="텍스트 쿼리에 대한 Assistant 응답 가져오기")
async def get_assistant_response(
        query: AssistantQuery,
        thread_id: Optional[str] = Query(None, description="대화 스레드 ID (없으면 새로 생성됨)"),
        assistant_service: AssistantService = Depends(get_assistant_service)
):
    try:
        validated_thread_id = _validate_thread_id(thread_id)
        logger.info(f"Assistant 서비스 호출 전 thread_id: {validated_thread_id}")
        
        question, response_text, final_thread_id = assistant_service.get_response(query.text, validated_thread_id)

        return AssistantResponse(
            question=question,
            response=response_text, 
            thread_id=final_thread_id
        )
    except Exception as e:
        logger.error(f"Assistant 응답 처리 중 오류 발생: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Assistant 응답을 가져오는 중 오류 발생: {str(e)}"
        )


@router.post("/upload", response_model=AssistantResponse, summary="오디오 파일 업로드로 STT 변환 후 Assistant 응답 가져오기")
async def get_assistant_response_from_upload(
        file: UploadFile = File(...),
        thread_id: Optional[str] = Query(None, description="대화 스레드 ID (없으면 새로 생성됨)"),
        stt_service: SpeechToTextService = Depends(get_speech_to_text_service),
        assistant_service: AssistantService = Depends(get_assistant_service)
):
    try:
        if not file.content_type or not file.content_type.startswith("audio/"):
            raise HTTPException(
                status_code=400,
                detail="오디오 파일만 업로드할 수 있습니다."
            )

        text = await stt_service.speech_to_text_from_file(file)
        validated_thread_id = _validate_thread_id(thread_id)
        logger.info(f"Assistant 서비스 호출 전 (upload) thread_id: {validated_thread_id}")

        question, response_text, final_thread_id = assistant_service.get_response(text, validated_thread_id)

        return AssistantResponse(
            question=question,
            response=response_text, 
            thread_id=final_thread_id
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"업로드된 오디오 처리 중 오류 발생: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"업로드된 오디오를 처리하는 중 오류 발생: {str(e)}"
        )


@router.post("/audio", summary="텍스트 쿼리에 대한 Assistant 응답을 음성으로 가져오기")
async def get_assistant_audio_response(
        query: AssistantQuery,
        thread_id: Optional[str] = Query(None, description="대화 스레드 ID (없으면 새로 생성됨)"),
        provider: Literal["elevenlabs", "openai"] = Query(default="openai", description="사용할 음성 제공자"),
        assistant_service: AssistantService = Depends(get_assistant_service),
        tts_service: TextToSpeechService = Depends(get_text_to_speech_service)
):
    try:
        validated_thread_id = _validate_thread_id(thread_id)
        logger.info(f"Assistant 서비스 호출 전 (audio) thread_id: {validated_thread_id}")

        question, response_text, final_thread_id = assistant_service.get_response(query.text, validated_thread_id)
        audio_stream = tts_service.text_to_speech_stream(response_text, provider=provider)

        return StreamingResponse(
            audio_stream,
            media_type="audio/mpeg",
            headers={
                "Content-Disposition": f"attachment; filename=assistant_response.mp3",
                "X-Thread-ID": final_thread_id
            }
        )
    except Exception as e:
        logger.error(f"Assistant 음성 응답 처리 중 오류 발생: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Assistant 음성 응답을 가져오는 중 오류 발생: {str(e)}"
        )


@router.post("/upload/audio", summary="오디오 파일 업로드로 STT 변환 후 Assistant 응답을 음성으로 가져오기")
async def get_assistant_audio_response_from_upload(
        file: UploadFile = File(...),
        thread_id: Optional[str] = Query(None, description="대화 스레드 ID (없으면 새로 생성됨)"),
        provider: Literal["elevenlabs", "openai"] = Query(default="openai", description="사용할 음성 제공자"),
        stt_service: SpeechToTextService = Depends(get_speech_to_text_service),
        assistant_service: AssistantService = Depends(get_assistant_service),
        tts_service: TextToSpeechService = Depends(get_text_to_speech_service)
):
    try:
        if not file.content_type or not file.content_type.startswith("audio/"):
            raise HTTPException(
                status_code=400,
                detail="오디오 파일만 업로드할 수 있습니다."
            )

        text = await stt_service.speech_to_text_from_file(file)
        validated_thread_id = _validate_thread_id(thread_id)
        logger.info(f"Assistant 서비스 호출 전 (upload/audio) thread_id: {validated_thread_id}")

        question, response_text, final_thread_id = assistant_service.get_response(text, validated_thread_id)
        audio_stream = tts_service.text_to_speech_stream(response_text, provider=provider)

        return StreamingResponse(
            audio_stream,
            media_type="audio/mpeg",
            headers={
                "Content-Disposition": f"attachment; filename=assistant_response.mp3",
                "X-Thread-ID": final_thread_id
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"업로드된 오디오 음성 응답 처리 중 오류 발생: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"업로드된 오디오를 처리하는 중 오류 발생: {str(e)}"
        )
