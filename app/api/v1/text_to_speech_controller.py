"""
API routes for text-to-speech functionality.
"""
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse

from app.dependencies import get_text_to_speech_service
from app.models.text_to_speech import TextQuery
from app.services.text_to_speech_service import TextToSpeechService

router = APIRouter(prefix="/text-to-speech", tags=["text-to-speech"])


@router.post("/", summary="Convert text to speech")
async def convert_text_to_speech(
        query: TextQuery,
        tts_service: TextToSpeechService = Depends(get_text_to_speech_service)
):
    """
    Convert text to speech and return audio stream.
    
    Args:
        query: The text query to convert to speech
        tts_service: The text-to-speech service (injected)
        
    Returns:
        A streaming response with the audio data
        
    Raises:
        HTTPException: If there's an error converting text to speech
    """
    try:
        # Convert text to speech using the service
        audio_stream = tts_service.text_to_speech_stream(query.text)

        # Return the audio as a streaming response
        return StreamingResponse(
            audio_stream,
            media_type="audio/mpeg",
            headers={
                "Content-Disposition": "attachment; filename=speech.mp3"
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error converting text to speech: {str(e)}"
        )
