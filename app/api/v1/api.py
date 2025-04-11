"""
API router that includes all API v1 endpoints.
"""
from fastapi import APIRouter

from app.api.v1 import frontend, text_to_speech_controller as text_to_speech, \
    speech_to_text_controller as speech_to_text, chatgpt_controller as chatgpt

api_router = APIRouter()

# Include all API v1 routers
api_router.include_router(frontend.router)
api_router.include_router(text_to_speech.router)
api_router.include_router(speech_to_text.router)
api_router.include_router(chatgpt.router)
