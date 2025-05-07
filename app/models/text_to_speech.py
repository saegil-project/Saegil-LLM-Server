"""
텍스트-음성 변환을 위한 Pydantic 모델.
"""
from pydantic import BaseModel


class TextQuery(BaseModel):
    """
    텍스트-음성 변환 요청 모델.
    """
    text: str
