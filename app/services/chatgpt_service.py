"""
OpenAI API를 사용한 ChatGPT 서비스.
"""
from openai import OpenAI

from app.core.config import settings


class ChatGPTService:
    """
    ChatGPT 서비스.
    """

    def __init__(self, api_key: str = settings.OPENAI_API_KEY):
        """
        OpenAI API 키로 서비스를 초기화합니다.
        """
        self.client = OpenAI(api_key=api_key)
        self.model = settings.OPENAI_CHAT_MODEL

    def get_response(self, text: str) -> str:
        """
        텍스트 쿼리에 대한 ChatGPT 응답을 가져옵니다.

        Args:
            text: ChatGPT에게 보낼 텍스트 쿼리

        Returns:
            ChatGPT의 응답 텍스트

        Raises:
            Exception: ChatGPT 응답을 가져오는 중 오류가 발생한 경우
        """
        try:
            # OpenAI API를 사용하여 ChatGPT 응답 생성
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "당신은 도움이 되는 AI 비서입니다."},
                    {"role": "user", "content": text}
                ]
            )

            # 결과 반환
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"ChatGPT 응답을 가져오는 중 오류 발생: {str(e)}")


# 서비스의 기본 인스턴스 생성
chatgpt_service = ChatGPTService()
