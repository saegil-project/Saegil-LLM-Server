"""
OpenAI API를 사용한 음성-텍스트 변환 서비스.
"""
import os
import tempfile
import mimetypes
from pathlib import Path

import requests
from fastapi import UploadFile
from openai import OpenAI

from app.core.config import settings

from pydub import AudioSegment

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

    def _convert_m4a_to_mp3(self, input_path: str) -> str:
        """
        m4a 파일을 mp3로 변환합니다.

        Args:
            input_path: 변환할 m4a 파일 경로

        Returns:
            변환된 mp3 파일 경로
        """
        output_path = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False).name
        audio = AudioSegment.from_file(input_path, format="m4a")
        audio.export(output_path, format="mp3")
        return output_path

    def _transcribe_with_openai(self, file_path: str) -> str:
        """
        OpenAI를 사용하여 파일에서 텍스트를 추출합니다.
        """
        with open(file_path, "rb") as audio_file:
            transcript = self.client.audio.transcriptions.create(
                model=self.model,
                file=audio_file
            )
        return transcript.text

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
            
            # 파일 확장자 결정
            content_type = response.headers.get('Content-Type', '')
            ext = self._get_extension_from_content_type(content_type)
            
            if not ext:
                # URL에서 확장자 추출 시도
                ext = Path(audio_url).suffix
                if not ext:
                    ext = ".mp3"  # 기본값

            # 임시 파일로 오디오 저장
            with tempfile.NamedTemporaryFile(suffix=ext, delete=False) as temp_file:
                temp_file_path = temp_file.name
                temp_file.write(response.content)

            try:
                # m4a라면 mp3로 변환
                if ext == ".m4a":
                    converted_path = self._convert_m4a_to_mp3(temp_file_path)
                    os.remove(temp_file_path)
                    temp_file_path = converted_path

                # OpenAI API를 사용하여 음성을 텍스트로 변환
                return self._transcribe_with_openai(temp_file_path)
            finally:
                # 임시 파일 삭제
                if os.path.exists(temp_file_path):
                    os.remove(temp_file_path)

        except Exception as e:
            raise Exception(f"음성을 텍스트로 변환하는 중 오류 발생: {str(e)}")

    async def speech_to_text_from_file(self, file: UploadFile) -> str:
        """
        업로드된 오디오 파일에서 음성을 텍스트로 변환합니다.

        Args:
            file: 텍스트로 변환할 업로드된 오디오 파일

        Returns:
            변환된 텍스트

        Raises:
            Exception: 오디오를 텍스트로 변환하는 중 오류가 발생한 경우
        """
        try:
            # 파일 확장자 결정
            ext = self._get_extension_from_filename(file.filename) or self._get_extension_from_content_type(file.content_type)
            
            # 임시 파일로 업로드된 오디오 저장
            with tempfile.NamedTemporaryFile(suffix=ext, delete=False) as temp_file:
                temp_file_path = temp_file.name
                content = await file.read()
                temp_file.write(content)

            try:
                # m4a라면 mp3로 변환
                if ext == ".m4a":
                    converted_path = self._convert_m4a_to_mp3(temp_file_path)
                    os.remove(temp_file_path)
                    temp_file_path = converted_path

                # OpenAI API를 사용하여 음성을 텍스트로 변환
                return self._transcribe_with_openai(temp_file_path)
            finally:
                # 임시 파일 삭제
                if os.path.exists(temp_file_path):
                    os.remove(temp_file_path)

        except Exception as e:
            raise Exception(f"업로드된 오디오를 텍스트로 변환하는 중 오류 발생: {str(e)}")
    
    def _get_extension_from_content_type(self, content_type: str) -> str:
        """
        MIME 타입으로부터 적절한 파일 확장자를 결정합니다.
        
        Args:
            content_type: 파일의 MIME 타입
            
        Returns:
            파일 확장자(.mp3, .m4a 등)
        """
        if not content_type:
            return ".mp3"
        
        # 직접 매핑
        if "mpeg" in content_type or "mp3" in content_type:
            return ".mp3"
        elif "mp4" in content_type or "m4a" in content_type:
            return ".m4a"
        elif "wav" in content_type:
            return ".wav"
        
        # mimetypes 라이브러리 사용
        ext = mimetypes.guess_extension(content_type)
        if ext:
            return ext
            
        return ".mp3"  # 기본값
    
    def _get_extension_from_filename(self, filename: str) -> str:
        """
        파일명에서 확장자를 추출합니다.
        
        Args:
            filename: 파일 이름
            
        Returns:
            파일 확장자(.mp3, .m4a 등) 또는 None
        """
        if not filename:
            return None
            
        ext = Path(filename).suffix
        if ext:
            return ext
            
        return None


# 서비스의 기본 인스턴스 생성
speech_to_text_service = SpeechToTextService()
