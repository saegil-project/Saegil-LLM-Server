from fastapi import APIRouter, Depends, HTTPException, UploadFile, File

from app.core.config import settings
from app.dependencies import get_chatgpt_service, get_speech_to_text_service
from app.models.chatgpt import ChatGPTQuery, ChatGPTResponse, ChatGPTSttQuery, ChatGPTAudioUrlQuery
from app.services.chatgpt_service import ChatGPTService
from app.services.speech_to_text_service import SpeechToTextService

router = APIRouter(prefix="/chatgpt", tags=["chatgpt"])


@router.post("/", response_model=ChatGPTResponse, summary="텍스트 쿼리에 대한 ChatGPT 응답 가져오기")
async def get_chatgpt_response(
        query: ChatGPTQuery,
        chatgpt_service: ChatGPTService = Depends(get_chatgpt_service)
):
    try:
        response_text = chatgpt_service.get_response(query.text)
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
    try:
        response_text = chatgpt_service.get_response(query.audio_text)
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
    try:
        text = stt_service.speech_to_text(str(query.audio_url))
        response_text = chatgpt_service.get_response(text)
        return ChatGPTResponse(response=response_text, text=text)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"오디오 URL을 처리하는 중 오류 발생: {str(e)}"
        )


@router.post("/upload", response_model=ChatGPTResponse, summary="오디오 파일 업로드로 ChatGPT 응답 가져오기")
async def get_chatgpt_response_from_upload(
        file: UploadFile = File(...),
        stt_service: SpeechToTextService = Depends(get_speech_to_text_service),
        chatgpt_service: ChatGPTService = Depends(get_chatgpt_service)
):
    try:
        if not file.content_type or not file.content_type.startswith("audio/"):
            raise HTTPException(
                status_code=400,
                detail="오디오 파일만 업로드할 수 있습니다."
            )

        text = await stt_service.speech_to_text_from_file(file)
        response_text = chatgpt_service.get_response(text)
        return ChatGPTResponse(response=response_text, text=text)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"업로드된 오디오를 처리하는 중 오류 발생: {str(e)}"
        )
