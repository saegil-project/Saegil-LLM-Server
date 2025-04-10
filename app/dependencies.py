"""
Dependency injection functions for the application.
"""

from app.services.text_to_speech import TextToSpeechService, text_to_speech_service


def get_text_to_speech_service() -> TextToSpeechService:
    """
    Dependency for getting the text-to-speech service.
    
    Returns:
        An instance of the TextToSpeechService
    """
    return text_to_speech_service
