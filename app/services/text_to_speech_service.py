"""
ElevenLabs API를 사용한 텍스트-음성 변환 서비스.
"""
from io import BytesIO
from typing import IO

from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs

from app.core.config import settings


class TextToSpeechService:
    """
    텍스트-음성 변환 서비스.
    """

    def __init__(self, api_key: str = settings.ELEVENLABS_API_KEY):
        """
        ElevenLabs API 키로 서비스를 초기화합니다.
        """
        self.client = ElevenLabs(api_key=api_key)

    def text_to_speech_stream(self, text: str) -> IO[bytes]:
        """
        텍스트를 음성으로 변환하고 오디오 스트림을 반환합니다.

        Args:
            text: 음성으로 변환할 텍스트

        Returns:
            오디오 데이터가 포함된 BytesIO 스트림
        """
        # 텍스트를 음성으로 변환 수행
        response = self.client.text_to_speech.convert(
            voice_id=settings.ELEVENLABS_VOICE_ID,
            output_format="mp3_22050_32",
            text=text,
            model_id=settings.ELEVENLABS_MODEL_ID,
            # 출력을 사용자 정의할 수 있는 선택적 음성 설정
            voice_settings=VoiceSettings(
                stability=0.0,
                similarity_boost=1.0,
                style=0.0,
                use_speaker_boost=True,
                speed=1.0,
            ),
        )

        # 메모리에 오디오 데이터를 저장할 BytesIO 객체 생성
        audio_stream = BytesIO()

        # 각 오디오 데이터 청크를 스트림에 쓰기
        for chunk in response:
            if chunk:
                audio_stream.write(chunk)

        # 스트림 위치를 처음으로 재설정
        audio_stream.seek(0)

        # 추가 사용을 위해 스트림 반환
        return audio_stream


# 서비스의 기본 인스턴스 생성
text_to_speech_service = TextToSpeechService()
