"""
OpenAI Assistants API를 위한 API 라우트.
"""
import logging
from typing import Literal, Optional

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query
from fastapi.responses import StreamingResponse

from app.dependencies import get_assistant_service, get_speech_to_text_service, get_text_to_speech_service
from app.models.assistant import AssistantQuery, AssistantResponse
from app.services.assistant_service import AssistantService
from app.services.speech_to_text_service import SpeechToTextService
from app.services.text_to_speech_service import TextToSpeechService

# 로깅 설정
logger = logging.getLogger(__name__)

# 라우터 경로를 /api/v1/assistant로 변경
router = APIRouter(prefix="/api/v1/assistant", tags=["assistant"])


def _validate_thread_id(thread_id: Optional[str]) -> Optional[str]:
    """thread_id 유효성 검사. 'thread_'로 시작하지 않으면 None 반환."""
    if thread_id and not thread_id.startswith("thread_"):
        logger.warning(f"잘못된 형식의 thread_id 수신: {thread_id}. None으로 처리합니다.")
        return None
    return thread_id


@router.post("/", response_model=AssistantResponse, summary="텍스트 쿼리에 대한 Assistant 응답 가져오기")
async def get_assistant_response(
        query: AssistantQuery,
        thread_id: str = Query(None, description="대화 스레드 ID (없으면 새로 생성됨)"),
        assistant_service: AssistantService = Depends(get_assistant_service)
):
    """
    텍스트 쿼리에 대한 OpenAI Assistant 응답을 가져옵니다.
    
    이 엔드포인트는 대화 문맥을 유지하면서 응답을 생성합니다.
    thread_id를 제공하면 기존 대화를 계속하고, 제공하지 않으면 새 대화를 시작합니다.

    Args:
        query: Assistant에게 보낼 텍스트 쿼리
        thread_id: 대화 스레드 ID (없으면 새로 생성됨)
        assistant_service: Assistant 서비스 (주입됨)

    Returns:
        Assistant의 응답이 포함된 응답

    Raises:
        HTTPException: Assistant 응답을 가져오는 중 오류가 발생한 경우
    """
    try:
        # Query 매개변수의 thread_id를 우선적으로 사용하고, 없으면 body의 thread_id 사용
        raw_thread_id = thread_id or query.thread_id
        # thread_id 유효성 검사
        validated_thread_id = _validate_thread_id(raw_thread_id)
        logger.info(f"Assistant 서비스 호출 전 thread_id: {validated_thread_id}") # 로깅 추가
        
        # 서비스를 사용하여 Assistant 응답 가져오기
        response_text, final_thread_id = assistant_service.get_response(query.text, validated_thread_id)

        # 응답 반환 - Pydantic 모델이 자동으로 camelCase로 변환
        return AssistantResponse(
            response=response_text, 
            thread_id=final_thread_id,
            text=query.text
        )
    except Exception as e:
        logger.error(f"Assistant 응답 처리 중 오류 발생: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Assistant 응답을 가져오는 중 오류 발생: {str(e)}"
        )


@router.post("/upload", response_model=AssistantResponse, summary="MP3 파일 업로드로 STT 변환 후 Assistant 응답 가져오기")
async def get_assistant_response_from_upload(
        file: UploadFile = File(...),
        thread_id: str = Query(None, description="대화 스레드 ID (없으면 새로 생성됨)"),
        stt_service: SpeechToTextService = Depends(get_speech_to_text_service),
        assistant_service: AssistantService = Depends(get_assistant_service)
):
    """
    업로드된 MP3 파일에서 음성을 텍스트로 변환한 후 OpenAI Assistant 응답을 가져옵니다.
    
    이 엔드포인트는 대화 문맥을 유지하면서 응답을 생성합니다.
    thread_id를 제공하면 기존 대화를 계속하고, 제공하지 않으면 새 대화를 시작합니다.

    Args:
        file: 텍스트로 변환할 오디오 파일 (MP3 형식)
        thread_id: 대화 스레드 ID (없으면 새로 생성됨)
        stt_service: 음성-텍스트 변환 서비스 (주입됨)
        assistant_service: Assistant 서비스 (주입됨)

    Returns:
        Assistant의 응답이 포함된 응답

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

        # 서비스를 사용하여 음성을 텍스트로 변환
        text = await stt_service.speech_to_text_from_file(file)

        # thread_id 유효성 검사
        validated_thread_id = _validate_thread_id(thread_id)
        logger.info(f"Assistant 서비스 호출 전 (upload) thread_id: {validated_thread_id}") # 로깅 추가

        # 서비스를 사용하여 Assistant 응답 가져오기
        response_text, final_thread_id = assistant_service.get_response(text, validated_thread_id)

        # 응답 반환 (텍스트 포함) - Pydantic 모델이 자동으로 camelCase로 변환
        return AssistantResponse(
            response=response_text, 
            thread_id=final_thread_id,
            text=text
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
        thread_id: str = Query(None, description="대화 스레드 ID (없으면 새로 생성됨)"),
        provider: Literal["elevenlabs", "openai"] = Query(default="openai", description="사용할 음성 제공자"),
        assistant_service: AssistantService = Depends(get_assistant_service),
        tts_service: TextToSpeechService = Depends(get_text_to_speech_service)
):
    """
    텍스트 쿼리에 대한 OpenAI Assistant 응답을 음성으로 변환하여 반환합니다.
    
    이 엔드포인트는 대화 문맥을 유지하면서 응답을 생성하고, 생성된 텍스트 응답을 
    OpenAI 또는 ElevenLabs를 사용하여 음성으로 변환합니다.
    thread_id를 제공하면 기존 대화를 계속하고, 제공하지 않으면 새 대화를 시작합니다.

    Args:
        query: Assistant에게 보낼 텍스트 쿼리
        thread_id: 대화 스레드 ID (없으면 새로 생성됨)
        provider: 사용할 음성 제공자 ("elevenlabs" 또는 "openai")
        assistant_service: Assistant 서비스 (주입됨)
        tts_service: 텍스트-음성 변환 서비스 (주입됨)

    Returns:
        음성 데이터를 포함한 스트리밍 응답

    Raises:
        HTTPException: Assistant 응답을 가져오거나 음성 변환 중 오류가 발생한 경우
    """
    try:
        # Query 매개변수의 thread_id를 우선적으로 사용하고, 없으면 body의 thread_id 사용
        raw_thread_id = thread_id or query.thread_id
        # thread_id 유효성 검사
        validated_thread_id = _validate_thread_id(raw_thread_id)
        logger.info(f"Assistant 서비스 호출 전 (audio) thread_id: {validated_thread_id}") # 로깅 추가

        # 서비스를 사용하여 Assistant 응답 가져오기
        response_text, final_thread_id = assistant_service.get_response(query.text, validated_thread_id)

        # 응답 텍스트를 음성으로 변환 (기본적으로 OpenAI의 TTS 사용)
        audio_stream = tts_service.text_to_speech_stream(response_text, provider=provider)

        # 오디오 스트림 반환
        return StreamingResponse(
            audio_stream,
            media_type="audio/mpeg",
            headers={
                "Content-Disposition": f"attachment; filename=assistant_response.mp3",
                "X-Thread-ID": final_thread_id # 스레드 ID를 헤더에 추가 (선택 사항)
            }
        )
    except Exception as e:
        logger.error(f"Assistant 음성 응답 처리 중 오류 발생: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Assistant 음성 응답을 가져오는 중 오류 발생: {str(e)}"
        )


@router.post("/upload/audio", summary="MP3 파일 업로드로 STT 변환 후 Assistant 응답을 음성으로 가져오기")
async def get_assistant_audio_response_from_upload(
        file: UploadFile = File(...),
        thread_id: str = Query(None, description="대화 스레드 ID (없으면 새로 생성됨)"),
        provider: Literal["elevenlabs", "openai"] = Query(default="openai", description="사용할 음성 제공자"),
        stt_service: SpeechToTextService = Depends(get_speech_to_text_service),
        assistant_service: AssistantService = Depends(get_assistant_service),
        tts_service: TextToSpeechService = Depends(get_text_to_speech_service)
):
    """
    업로드된 MP3 파일에서 음성을 텍스트로 변환한 후 OpenAI Assistant 응답을 음성으로 반환합니다.
    
    이 엔드포인트는 대화 문맥을 유지하면서 응답을 생성하고, 생성된 텍스트 응답을
    OpenAI 또는 ElevenLabs를 사용하여 음성으로 변환합니다.
    thread_id를 제공하면 기존 대화를 계속하고, 제공하지 않으면 새 대화를 시작합니다.

    Args:
        file: 텍스트로 변환할 오디오 파일 (MP3 형식)
        thread_id: 대화 스레드 ID (없으면 새로 생성됨)
        provider: 사용할 음성 제공자 ("elevenlabs" 또는 "openai")
        stt_service: 음성-텍스트 변환 서비스 (주입됨)
        assistant_service: Assistant 서비스 (주입됨)
        tts_service: 텍스트-음성 변환 서비스 (주입됨)

    Returns:
        음성 데이터를 포함한 스트리밍 응답

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

        # 서비스를 사용하여 음성을 텍스트로 변환
        text = await stt_service.speech_to_text_from_file(file)

        # thread_id 유효성 검사
        validated_thread_id = _validate_thread_id(thread_id)
        logger.info(f"Assistant 서비스 호출 전 (upload/audio) thread_id: {validated_thread_id}") # 로깅 추가

        # 서비스를 사용하여 Assistant 응답 가져오기
        response_text, final_thread_id = assistant_service.get_response(text, validated_thread_id)

        # 응답 텍스트를 음성으로 변환 (기본적으로 OpenAI의 TTS 사용)
        audio_stream = tts_service.text_to_speech_stream(response_text, provider=provider)

        # 오디오 스트림 반환
        return StreamingResponse(
            audio_stream,
            media_type="audio/mpeg",
            headers={
                "Content-Disposition": f"attachment; filename=assistant_response.mp3",
                "X-Thread-ID": final_thread_id # 스레드 ID를 헤더에 추가 (선택 사항)
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
