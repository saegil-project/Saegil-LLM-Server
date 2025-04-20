"""
ChatGPT 기능을 위한 API 라우트.
"""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File

from app.dependencies import get_chatgpt_service, get_speech_to_text_service
from app.models.chatgpt import ChatGPTQuery, ChatGPTResponse, ChatGPTSttQuery, ChatGPTAudioUrlQuery
from app.services.chatgpt_service import ChatGPTService
from app.services.speech_to_text_service import SpeechToTextService

# 라우터 경로를 /api/v1/chatgpt로 변경
router = APIRouter(prefix="/api/v1/chatgpt", tags=["chatgpt"])


@router.post("/", response_model=ChatGPTResponse, summary="텍스트 쿼리에 대한 ChatGPT 응답 가져오기")
async def get_chatgpt_response(
        query: ChatGPTQuery,
        chatgpt_service: ChatGPTService = Depends(get_chatgpt_service)
):
    """
    텍스트 쿼리에 대한 ChatGPT 응답을 가져옵니다.

    Args:
        query: ChatGPT에게 보낼 텍스트 쿼리
        chatgpt_service: ChatGPT 서비스 (주입됨)

    Returns:
        ChatGPT의 응답이 포함된 응답

    Raises:
        HTTPException: ChatGPT 응답을 가져오는 중 오류가 발생한 경우
    """
    try:
        # 서비스를 사용하여 ChatGPT 응답 가져오기
        response_text = chatgpt_service.get_response(query.text)

        # 응답 반환
        return ChatGPTResponse(response=response_text)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"ChatGPT 응답을 가져오는 중 오류 발생: {str(e)}"
        )


@router.post("/stt-text", response_model=ChatGPTResponse, summary="STT 텍스트 쿼리에 대한 ChatGPT 응답 가져오기")
async def get_chatgpt_response_from_stt_text(
        query: ChatGPTSttQuery,
        chatgpt_service: ChatGPTService = Depends(get_chatgpt_service)
):
    """
    STT로 변환된 텍스트 쿼리에 대한 ChatGPT 응답을 가져옵니다.

    Args:
        query: ChatGPT에게 보낼 STT로 변환된 텍스트 쿼리
        chatgpt_service: ChatGPT 서비스 (주입됨)

    Returns:
        ChatGPT의 응답이 포함된 응답

    Raises:
        HTTPException: ChatGPT 응답을 가져오는 중 오류가 발생한 경우
    """
    try:
        # 서비스를 사용하여 ChatGPT 응답 가져오기
        response_text = chatgpt_service.get_response(query.audio_text)

        # 응답 반환
        return ChatGPTResponse(response=response_text, text=query.audio_text)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"ChatGPT 응답을 가져오는 중 오류 발생: {str(e)}"
        )


@router.post("/audio-url", response_model=ChatGPTResponse, summary="오디오 URL로부터 ChatGPT 응답 가져오기")
async def get_chatgpt_response_from_audio_url(
        query: ChatGPTAudioUrlQuery,
        stt_service: SpeechToTextService = Depends(get_speech_to_text_service),
        chatgpt_service: ChatGPTService = Depends(get_chatgpt_service)
):
    """
    오디오 URL에서 추출한 텍스트에 대한 ChatGPT 응답을 가져옵니다.

    Args:
        query: 오디오 URL 쿼리
        stt_service: 음성-텍스트 변환 서비스 (주입됨)
        chatgpt_service: ChatGPT 서비스 (주입됨)

    Returns:
        ChatGPT의 응답이 포함된 응답

    Raises:
        HTTPException: 처리 중 오류가 발생한 경우
    """
    try:
        # 서비스를 사용하여 음성을 텍스트로 변환
        text = stt_service.speech_to_text(str(query.audio_url))

        # 서비스를 사용하여 ChatGPT 응답 가져오기
        response_text = chatgpt_service.get_response(text)

        # 응답 반환 (텍스트 포함)
        return ChatGPTResponse(response=response_text, text=text)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"오디오 URL을 처리하는 중 오류 발생: {str(e)}"
        )


@router.post("/upload", response_model=ChatGPTResponse, summary="MP3 파일 업로드로 ChatGPT 응답 가져오기")
async def get_chatgpt_response_from_upload(
        file: UploadFile = File(...),
        stt_service: SpeechToTextService = Depends(get_speech_to_text_service),
        chatgpt_service: ChatGPTService = Depends(get_chatgpt_service)
):
    """
    업로드된 MP3 파일에서 음성을 텍스트로 변환한 후 ChatGPT 응답을 가져옵니다.

    Args:
        file: 텍스트로 변환할 오디오 파일 (MP3 형식)
        stt_service: 음성-텍스트 변환 서비스 (주입됨)
        chatgpt_service: ChatGPT 서비스 (주입됨)

    Returns:
        ChatGPT의 응답이 포함된 응답

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

        # 서비스를 사용하여 ChatGPT 응답 가져오기
        response_text = chatgpt_service.get_response(text)

        # 응답 반환 (텍스트 포함)
        return ChatGPTResponse(response=response_text, text=text)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"업로드된 오디오를 처리하는 중 오류 발생: {str(e)}"
        )
