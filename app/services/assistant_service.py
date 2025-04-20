"""
OpenAI Assistants API를 사용한 서비스.
"""
import logging
import time
from typing import Optional, Tuple

from openai import OpenAI
from openai.types.beta.threads import Run

from app.core.config import settings

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AssistantService:
    """
    OpenAI Assistants API를 사용한 서비스.
    """

    def __init__(self, api_key: str = settings.OPENAI_API_KEY, assistant_id: str = settings.OPENAI_ASSISTANT_ID):
        """
        OpenAI API 키와 Assistant ID로 서비스를 초기화합니다.
        """
        self.client = OpenAI(api_key=api_key)
        self.assistant_id = assistant_id

        # Assistant ID가 제공되지 않은 경우 새 Assistant 생성
        if not self.assistant_id:
            logger.info("Assistant ID가 제공되지 않았습니다. 새 Assistant를 생성합니다.")
            self.assistant_id = self._create_assistant()
            logger.info(f"새 Assistant가 생성되었습니다. ID: {self.assistant_id}")

    def _create_assistant(self) -> str:
        """
        새 Assistant를 생성합니다.
        
        Returns:
            생성된 Assistant의 ID
        """
        try:
            assistant = self.client.beta.assistants.create(
                name="Saegil Assistant",
                instructions="당신은 도움이 되는 AI 비서입니다. 사용자의 질문에 친절하고 정확하게 답변해 주세요.",
                model=settings.OPENAI_ASSISTANT_MODEL,
            )
            return assistant.id
        except Exception as e:
            logger.error(f"Assistant 생성 중 오류 발생: {str(e)}")
            raise

    def create_thread(self) -> str:
        """
        새 대화 스레드를 생성합니다.
        
        Returns:
            생성된 스레드의 ID
        """
        try:
            thread = self.client.beta.threads.create()
            return thread.id
        except Exception as e:
            logger.error(f"스레드 생성 중 오류 발생: {str(e)}")
            raise

    def get_response(self, text: str, thread_id: Optional[str] = None) -> Tuple[str, str]:
        """
        텍스트 쿼리에 대한 Assistant 응답을 가져옵니다.
        
        Args:
            text: Assistant에게 보낼 텍스트 쿼리
            thread_id: 기존 대화 스레드 ID (없으면 새로 생성됨)
            
        Returns:
            Assistant의 응답 텍스트와 스레드 ID의 튜플
            
        Raises:
            Exception: Assistant 응답을 가져오는 중 오류가 발생한 경우
        """
        try:
            # 스레드 ID가 없으면 새로 생성
            if not thread_id:
                thread_id = self.create_thread()
                logger.info(f"새 스레드가 생성되었습니다. ID: {thread_id}")

            logger.info(f"OpenAI 메시지 생성 호출 전 thread_id: {thread_id}") # 로깅 추가

            # 메시지 추가
            self.client.beta.threads.messages.create(
                thread_id=thread_id,
                role="user",
                content=text
            )

            # 실행 생성 및 완료 대기
            run = self.client.beta.threads.runs.create(
                thread_id=thread_id,
                assistant_id=self.assistant_id
            )

            # 실행 완료 대기
            run = self._wait_for_run_completion(thread_id, run.id)

            # 응답 메시지 가져오기
            messages = self.client.beta.threads.messages.list(
                thread_id=thread_id
            )

            # 가장 최근의 assistant 메시지 찾기
            for message in messages.data:
                if message.role == "assistant":
                    # 텍스트 콘텐츠 추출
                    content_text = ""
                    for content in message.content:
                        if content.type == "text":
                            content_text += content.text.value

                    return content_text, thread_id

            # assistant 메시지를 찾지 못한 경우
            return "응답을 생성하지 못했습니다.", thread_id

        except Exception as e:
            logger.error(f"Assistant 응답을 가져오는 중 오류 발생: {str(e)}")
            raise Exception(f"Assistant 응답을 가져오는 중 오류 발생: {str(e)}")

    def _wait_for_run_completion(self, thread_id: str, run_id: str, timeout: int = 60) -> Run:
        """
        실행이 완료될 때까지 대기합니다.
        
        Args:
            thread_id: 스레드 ID
            run_id: 실행 ID
            timeout: 최대 대기 시간(초)
            
        Returns:
            완료된 실행 객체
            
        Raises:
            Exception: 실행이 시간 초과되거나 실패한 경우
        """
        start_time = time.time()
        while time.time() - start_time < timeout:
            run = self.client.beta.threads.runs.retrieve(
                thread_id=thread_id,
                run_id=run_id
            )

            if run.status == "completed":
                return run
            elif run.status in ["failed", "cancelled", "expired"]:
                logger.error(f"실행이 실패했습니다. 상태: {run.status}")
                raise Exception(f"실행이 실패했습니다. 상태: {run.status}")

            # 잠시 대기 후 다시 확인
            time.sleep(1)

        # 시간 초과
        logger.error("실행 시간이 초과되었습니다.")
        self.client.beta.threads.runs.cancel(
            thread_id=thread_id,
            run_id=run_id
        )
        raise Exception("실행 시간이 초과되었습니다.")


# 서비스의 기본 인스턴스 생성
assistant_service = AssistantService()
