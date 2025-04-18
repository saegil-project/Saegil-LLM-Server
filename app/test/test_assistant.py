"""
OpenAI Assistants API 테스트 스크립트.
"""
import requests

# API 엔드포인트 URL
BASE_URL = "http://localhost:9090"
ASSISTANT_ENDPOINT = f"{BASE_URL}/api/v1/assistant"


def test_assistant_text_query():
    """
    텍스트 쿼리에 대한 Assistant 응답을 테스트합니다.
    """
    print("\n=== Assistant 텍스트 쿼리 테스트 ===")

    # 요청 데이터
    data = {
        "text": "안녕하세요, 당신은 누구인가요?"
    }

    # API 요청
    response = requests.post(
        ASSISTANT_ENDPOINT,
        json=data
    )

    # 응답 확인
    if response.status_code == 200:
        result = response.json()
        print(f"응답: {result['response']}")
        print(f"스레드 ID: {result['thread_id']}")

        # 스레드 ID 저장
        thread_id = result['thread_id']

        # 두 번째 쿼리 (대화 문맥 유지 테스트)
        print("\n=== 대화 문맥 유지 테스트 ===")
        data = {
            "text": "내가 방금 무엇에 대해 물어봤나요?",
            "thread_id": thread_id
        }

        # 두 번째 API 요청
        response = requests.post(
            ASSISTANT_ENDPOINT,
            json=data
        )

        # 응답 확인
        if response.status_code == 200:
            result = response.json()
            print(f"응답: {result['response']}")
            print(f"스레드 ID: {result['thread_id']}")
            return True
        else:
            print(f"오류: {response.status_code}")
            print(response.text)
            return False
    else:
        print(f"오류: {response.status_code}")
        print(response.text)
        return False


if __name__ == "__main__":
    # 서버가 실행 중인지 확인
    try:
        response = requests.get(f"{BASE_URL}/docs")
        if response.status_code != 200:
            print("서버가 실행 중이지 않습니다. 먼저 서버를 실행하세요.")
            exit(1)
    except requests.exceptions.ConnectionError:
        print("서버가 실행 중이지 않습니다. 먼저 서버를 실행하세요.")
        exit(1)

    # 테스트 실행
    test_assistant_text_query()
