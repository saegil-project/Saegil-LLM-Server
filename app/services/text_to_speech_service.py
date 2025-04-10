"""
Service for text-to-speech conversion using ElevenLabs API.
"""
from io import BytesIO
from typing import IO

from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs

from app.core.config import settings


class TextToSpeechService:
    """
    Service for text-to-speech conversion.
    """

    def __init__(self, api_key: str = settings.ELEVENLABS_API_KEY):
        """
        Initialize the service with the ElevenLabs API key.
        """
        self.client = ElevenLabs(api_key=api_key)

    def text_to_speech_stream(self, text: str) -> IO[bytes]:
        """
        Convert text to speech and return an audio stream.
        
        Args:
            text: The text to convert to speech
            
        Returns:
            A BytesIO stream containing the audio data
        """
        # Perform the text-to-speech conversion
        response = self.client.text_to_speech.convert(
            voice_id=settings.ELEVENLABS_VOICE_ID,
            output_format="mp3_22050_32",
            text=text,
            model_id=settings.ELEVENLABS_MODEL_ID,
            # Optional voice settings that allow you to customize the output
            voice_settings=VoiceSettings(
                stability=0.0,
                similarity_boost=1.0,
                style=0.0,
                use_speaker_boost=True,
                speed=1.0,
            ),
        )

        # Create a BytesIO object to hold the audio data in memory
        audio_stream = BytesIO()

        # Write each chunk of audio data to the stream
        for chunk in response:
            if chunk:
                audio_stream.write(chunk)

        # Reset stream position to the beginning
        audio_stream.seek(0)

        # Return the stream for further use
        return audio_stream


# Create a default instance of the service
text_to_speech_service = TextToSpeechService()
