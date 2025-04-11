"""
OpenAI API를 사용한 음성-텍스트 변환 서비스.
"""
import os
import tempfile

import requests
from fastapi import UploadFile
from openai import OpenAI

from app.core.config import settings


class SpeechToTextService:
    """
    음성-텍스트 변환 서비스.
    """

    def __init__(self, api_key: str = settings.OPENAI_API_KEY):
        """
        OpenAI API 키로 서비스를 초기화합니다.
        """
        self.client = OpenAI(api_key=api_key)
        self.model = settings.OPENAI_MODEL

    def speech_to_text(self, audio_url: str) -> str:
        """
        오디오 URL에서 음성을 텍스트로 변환합니다.

        Args:
            audio_url: 텍스트로 변환할 오디오 파일의 URL

        Returns:
            변환된 텍스트

        Raises:
            Exception: 오디오를 텍스트로 변환하는 중 오류가 발생한 경우
        """
        try:
            # URL에서 오디오 파일 다운로드
            response = requests.get(audio_url)
            response.raise_for_status()  # 오류 발생 시 예외 발생

            # 임시 파일로 오디오 저장
            with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_file:
                temp_file_path = temp_file.name
                temp_file.write(response.content)

            try:
                # OpenAI API를 사용하여 음성을 텍스트로 변환
                with open(temp_file_path, "rb") as audio_file:
                    transcript = self.client.audio.transcriptions.create(
                        model=self.model,
                        file=audio_file
                    )

                # 결과 반환
                return transcript.text
            finally:
                # 임시 파일 삭제
                if os.path.exists(temp_file_path):
                    os.remove(temp_file_path)

        except Exception as e:
            raise Exception(f"음성을 텍스트로 변환하는 중 오류 발생: {str(e)}")

    async def speech_to_text_from_file(self, file: UploadFile) -> str:
        """
        업로드된 MP3 파일에서 음성을 텍스트로 변환합니다.

        Args:
            file: 텍스트로 변환할 업로드된 오디오 파일

        Returns:
            변환된 텍스트

        Raises:
            Exception: 오디오를 텍스트로 변환하는 중 오류가 발생한 경우
        """
        try:
            # 임시 파일로 업로드된 오디오 저장
            with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_file:
                temp_file_path = temp_file.name
                content = await file.read()
                temp_file.write(content)

            try:
                # OpenAI API를 사용하여 음성을 텍스트로 변환
                with open(temp_file_path, "rb") as audio_file:
                    transcript = self.client.audio.transcriptions.create(
                        model=self.model,
                        file=audio_file
                    )

                # 결과 반환
                return transcript.text
            finally:
                # 임시 파일 삭제
                if os.path.exists(temp_file_path):
                    os.remove(temp_file_path)

        except Exception as e:
            raise Exception(f"업로드된 오디오를 텍스트로 변환하는 중 오류 발생: {str(e)}")


# 서비스의 기본 인스턴스 생성
speech_to_text_service = SpeechToTextService()
