"""
OpenAI Assistants API를 위한 API 라우트.
"""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File

from app.dependencies import get_assistant_service, get_speech_to_text_service
from app.models.assistant import AssistantQuery, AssistantResponse
from app.services.assistant_service import AssistantService
from app.services.speech_to_text_service import SpeechToTextService

router = APIRouter(prefix="/assistant", tags=["assistant"])


@router.post("/", response_model=AssistantResponse, summary="텍스트 쿼리에 대한 Assistant 응답 가져오기")
async def get_assistant_response(
        query: AssistantQuery,
        assistant_service: AssistantService = Depends(get_assistant_service)
):
    """
    텍스트 쿼리에 대한 OpenAI Assistant 응답을 가져옵니다.
    
    이 엔드포인트는 대화 문맥을 유지하면서 응답을 생성합니다.
    thread_id를 제공하면 기존 대화를 계속하고, 제공하지 않으면 새 대화를 시작합니다.

    Args:
        query: Assistant에게 보낼 텍스트 쿼리와 선택적 thread_id
        assistant_service: Assistant 서비스 (주입됨)

    Returns:
        Assistant의 응답이 포함된 응답

    Raises:
        HTTPException: Assistant 응답을 가져오는 중 오류가 발생한 경우
    """
    try:
        # 서비스를 사용하여 Assistant 응답 가져오기
        response_text, thread_id = assistant_service.get_response(query.text, query.thread_id)

        # 응답 반환
        return AssistantResponse(response=response_text, thread_id=thread_id, text=query.text)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Assistant 응답을 가져오는 중 오류 발생: {str(e)}"
        )


@router.post("/upload", response_model=AssistantResponse, summary="MP3 파일 업로드로 STT 변환 후 Assistant 응답 가져오기")
async def get_assistant_response_from_upload(
        file: UploadFile = File(...),
        thread_id: str = None,
        stt_service: SpeechToTextService = Depends(get_speech_to_text_service),
        assistant_service: AssistantService = Depends(get_assistant_service)
):
    """
    업로드된 MP3 파일에서 음성을 텍스트로 변환한 후 OpenAI Assistant 응답을 가져옵니다.
    
    이 엔드포인트는 대화 문맥을 유지하면서 응답을 생성합니다.
    thread_id를 제공하면 기존 대화를 계속하고, 제공하지 않으면 새 대화를 시작합니다.

    Args:
        file: 텍스트로 변환할 오디오 파일 (MP3 형식)
        thread_id: 선택적 대화 스레드 ID
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

        # 서비스를 사용하여 Assistant 응답 가져오기
        response_text, new_thread_id = assistant_service.get_response(text, thread_id)

        # 응답 반환 (텍스트 포함)
        return AssistantResponse(response=response_text, thread_id=new_thread_id, text=text)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"업로드된 오디오를 처리하는 중 오류 발생: {str(e)}"
        )
