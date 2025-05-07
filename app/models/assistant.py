"""
OpenAI Assistants API를 위한 Pydantic 모델.
"""
from pydantic import BaseModel, Field
from humps import camelize


def camel_case(snake_str):
    """snake_case를 camelCase로 변환합니다."""
    return camelize(snake_str)


class AssistantQuery(BaseModel):
    """
    OpenAI Assistants API 요청을 위한 모델.
    """
    text: str = Field(..., description="Assistant에게 보낼 텍스트 쿼리")
    # thread_id 필드 제거

    model_config = {
        "populate_by_name": True,  # 이름으로도 필드를 채울 수 있게 합니다.
        "alias_generator": camel_case,  # snake_case 필드명을 camelCase로 변환합니다.
        "json_schema_extra": {
            "example": {
                "text": "안녕하세요, 오늘 날씨가 어떤가요?"
                # thread_id 예시 제거
            }
        }
    }


class AssistantResponse(BaseModel):
    """
    OpenAI Assistants API 응답을 위한 모델.
    """
    question: str = Field(..., description="사용자의 원본 질문")
    response: str = Field(..., description="Assistant의 응답 텍스트")
    thread_id: str = Field(..., description="대화 스레드 ID")

    model_config = {
        "populate_by_name": True,  # 이름으로도 필드를 채울 수 있게 합니다.
        "alias_generator": camel_case,  # snake_case 필드명을 camelCase로 변환합니다.
        "json_schema_extra": {
            "example": {
                "question": "오늘 날씨가 어떤가요?",
                "response": "안녕하세요! 오늘 날씨는 지역에 따라 다를 수 있습니다.",
                "threadId": "thread_abc123"
            }
        }
    }
