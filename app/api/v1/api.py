"""
API router that includes all API v1 endpoints.
"""
from fastapi import APIRouter

from app.api.v1 import frontend

api_router = APIRouter()

# Include all API v1 routers
api_router.include_router(frontend.router)
api_router.include_router(text_to_speech.router)
