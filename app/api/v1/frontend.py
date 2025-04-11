"""
프론트엔드 페이지를 위한 API 라우트.
"""
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

# Set up templates
templates = Jinja2Templates(directory="app/templates")

router = APIRouter(tags=["frontend"])


@router.get("/", response_class=HTMLResponse, summary="웹 애플리케이션 가져오기")
async def get_web_app(request: Request):
    """
    웹 애플리케이션의 메인 페이지를 제공합니다.

    Args:
        request: 요청 객체

    Returns:
        HTML 템플릿 응답
    """
    return templates.TemplateResponse("index.html", {"request": request})
