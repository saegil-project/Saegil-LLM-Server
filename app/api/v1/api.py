"""
API router that includes all API v1 endpoints.
"""
from fastapi import APIRouter

from app.api.v1 import text_to_speech_controller as text_to_speech, \
    speech_to_text_controller as speech_to_text, chatgpt_controller as chatgpt, \
    stt_chatgpt_tts_controller as stt_chatgpt_tts, assistant_controller as assistant

api_router = APIRouter()

api_router.include_router(text_to_speech.router)
api_router.include_router(speech_to_text.router)
api_router.include_router(chatgpt.router)
api_router.include_router(stt_chatgpt_tts.router)
api_router.include_router(assistant.router)
