"""
애플리케이션을 위한 의존성 주입 함수.
"""

from app.services.speech_to_text_service import SpeechToTextService, speech_to_text_service
from app.services.text_to_speech_service import TextToSpeechService, text_to_speech_service


def get_text_to_speech_service() -> TextToSpeechService:
    """
    텍스트-음성 변환 서비스를 가져오기 위한 의존성.

    Returns:
        TextToSpeechService의 인스턴스
    """
    return text_to_speech_service


def get_speech_to_text_service() -> SpeechToTextService:
    """
    음성-텍스트 변환 서비스를 가져오기 위한 의존성.

    Returns:
        SpeechToTextService의 인스턴스
    """
    return speech_to_text_service
