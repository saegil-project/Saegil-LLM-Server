from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import StreamingResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.services.text_to_speech_stream import text_to_speech_stream
import uvicorn
import os
from pydantic import BaseModel

# Define request model
class TextQuery(BaseModel):
    text: str

# Create FastAPI app
app = FastAPI(
    title="Text-to-Speech API",
    description="API that converts text queries to speech using ElevenLabs",
    version="1.0.0"
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# static 및 templates 디렉토리는 app/ 내부에 있으므로 절대경로로 지정
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

@app.post("/text-to-speech")
async def convert_text_to_speech(query: TextQuery):
    """
    Convert text to speech and return audio stream
    """
    try:
        # Convert text to speech using the existing function
        audio_stream = text_to_speech_stream(query.text)

        # Return the audio as a streaming response
        return StreamingResponse(
            audio_stream,
            media_type="audio/mpeg",
            headers={
                "Content-Disposition": "attachment; filename=speech.mp3"
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error converting text to speech: {str(e)}")

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """
    Root endpoint that serves the web application
    """
    return templates.TemplateResponse("index.html", {"request": request})

# Run the app if this file is executed directly
if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
