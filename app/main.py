import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api.v1.api import api_router
from app.core.config import settings

# Define tags metadata for better organization in Swagger UI
tags_metadata = [
    {
        "name": "text-to-speech",
        "description": "ElevenLabs API를 사용한 텍스트-음성 변환 관련 작업.",
    },
    {
        "name": "speech-to-text",
        "description": "OpenAI API를 사용한 음성-텍스트 변환 관련 작업.",
    },
    {
        "name": "chatgpt",
        "description": "OpenAI API를 사용한 ChatGPT 응답 관련 작업.",
    },
    {
        "name": "stt-chatgpt-tts",
        "description": "음성-텍스트 변환, ChatGPT 응답, 텍스트-음성 변환을 통합한 작업.",
    },
    {
        "name": "frontend",
        "description": "웹 애플리케이션 프론트엔드 제공 관련 작업.",
    },
]

# Create FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    description=f"""
    {settings.PROJECT_DESCRIPTION}

    ## API 기능

    * **텍스트-음성 변환**: ElevenLabs API를 사용하여 텍스트를 고품질 음성으로 변환
    * **음성-텍스트 변환**: OpenAI Whisper API를 사용하여 오디오를 텍스트로 변환
    * **스트리밍 오디오**: 효율적인 전송을 위한 스트리밍 응답으로 오디오 제공

    ## 인증

    이 API는 다음 API 키를 사용합니다:
    * **ElevenLabs API 키**: 텍스트-음성 변환 기능을 위해 필요
    * **OpenAI API 키**: 음성-텍스트 변환 기능을 위해 필요

    환경 변수에 API 키를 설정하세요.

    ## 사용량 제한

    이 API를 사용할 때 ElevenLabs 및 OpenAI의 사용량 제한 정책을 숙지하세요.
    """,
    version=settings.VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    swagger_ui_parameters={
        "defaultModelsExpandDepth": 1,
        "deepLinking": True,
        "displayRequestDuration": True,
        "syntaxHighlight.theme": "monokai"
    },
    contact={
        "name": "API 지원팀",
        "email": "support@example.com",
        "url": "https://example.com/support",
    },
    license_info={
        "name": "MIT 라이선스",
        "url": "https://opensource.org/licenses/MIT",
    },
    openapi_tags=tags_metadata
)

# Mount static files directory
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Include API router
app.include_router(api_router)

# Run the app if this file is executed directly
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=9090, reload=True)
