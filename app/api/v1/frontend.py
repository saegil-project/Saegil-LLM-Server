"""
API routes for frontend pages.
"""
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

# Set up templates
templates = Jinja2Templates(directory="app/templates")

router = APIRouter(tags=["frontend"])


@router.get("/", response_class=HTMLResponse, summary="Get the web application")
async def get_web_app(request: Request):
    """
    Serve the web application's main page.
    
    Args:
        request: The request object
        
    Returns:
        The HTML template response
    """
    return templates.TemplateResponse("index.html", {"request": request})
