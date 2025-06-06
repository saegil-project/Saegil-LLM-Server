import uuid

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import StreamingResponse

from app.core.config import settings
from app.dependencies import get_speech_to_text_service, get_chatgpt_service, get_text_to_speech_service
from app.models.stt_chatgpt_tts import STTChatGPTTTSResponse
from app.services.chatgpt_service import ChatGPTService
from app.services.speech_to_text_service import SpeechToTextService
from app.services.text_to_speech_service import TextToSpeechService

router = APIRouter(prefix="/stt-chatgpt-tts", tags=["stt-chatgpt-tts"])


@router.post("/upload", summary="음성 파일 업로드로 STT-ChatGPT-TTS 통합 처리")
async def process_stt_chatgpt_tts_from_upload(
        file: UploadFile = File(...),
        stt_service: SpeechToTextService = Depends(get_speech_to_text_service),
        chatgpt_service: ChatGPTService = Depends(get_chatgpt_service),
        tts_service: TextToSpeechService = Depends(get_text_to_speech_service)
):
    try:
        if not file.content_type or not file.content_type.startswith("audio/"):
            raise HTTPException(
                status_code=400,
                detail="오디오 파일만 업로드할 수 있습니다."
            )

        text = await stt_service.speech_to_text_from_file(file)
        response_text = chatgpt_service.get_response(text)
        audio_stream = tts_service.text_to_speech_stream(response_text)

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
    try:
        if not file.content_type or not file.content_type.startswith("audio/"):
            raise HTTPException(
                status_code=400,
                detail="오디오 파일만 업로드할 수 있습니다."
            )

        text = await stt_service.speech_to_text_from_file(file)
        response_text = chatgpt_service.get_response(text)
        audio_url = f"/stt-chatgpt-tts/audio/{uuid.uuid4()}.mp3"

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
