# 텍스트-음성 변환 웹 애플리케이션

FastAPI로 구축된 REST API를 갖춘 웹 애플리케이션으로, ElevenLabs API를 사용하여 텍스트 쿼리를 음성으로 변환합니다.

## 사전 요구사항

- Python 3.7+
- ElevenLabs API 키

## 설치 방법

1. 이 저장소를 클론합니다
2. 필요한 의존성을 설치합니다:

```bash
pip install -r requirements.txt
```

3. ElevenLabs API 키를 환경 변수로 설정합니다:

```bash
export ELEVENLABS_API_KEY="your-api-key-here"
```

또는 프로젝트 루트에 다음 내용이 포함된 `.env` 파일을 생성할 수 있습니다:

```
ELEVENLABS_API_KEY=your-api-key-here
```

## 애플리케이션 실행

서버 시작:

```bash
python app.py
```

웹 애플리케이션은 http://localhost:8000 에서 사용할 수 있습니다.

대화형 API 문서는 http://localhost:8000/docs 에서 접근할 수 있습니다.

## 웹 인터페이스 사용 방법

1. 브라우저를 열고 http://localhost:8000 으로 이동합니다
2. 텍스트 영역에 음성으로 변환하고 싶은 텍스트를 입력합니다
3. "Convert to Speech" 버튼을 클릭합니다
4. 변환이 완료될 때까지 기다립니다
5. 오디오는 브라우저에서 자동으로 재생됩니다
6. "Download MP3" 버튼을 클릭하여 MP3 파일을 다운로드할 수 있습니다

## API 엔드포인트

### GET /

웹 애플리케이션 인터페이스를 제공합니다.

### POST /text-to-speech

텍스트를 음성으로 변환하고 오디오 파일을 반환합니다.

**요청 본문:**

```json
{
  "text": "음성으로 변환할 텍스트"
}
```

**응답:**

오디오 파일 (MP3 형식)

## API 테스트

API 사용 방법을 보여주는 테스트 스크립트가 제공됩니다:

```bash
# 다른 터미널에서 API 서버가 실행 중인지 확인하세요
python test_api.py
```

이 스크립트는 샘플 텍스트로 API에 요청을 보내고 결과 오디오를 `test_output.mp3`로 저장합니다.

## 구현 세부 사항

- 이 애플리케이션은 HTTP 요청 처리 및 웹 인터페이스 제공을 위해 FastAPI를 사용합니다
- 텍스트-음성 변환은 ElevenLabs API를 사용하여 수행됩니다
- 오디오는 MP3 파일 형식으로 클라이언트에게 스트리밍됩니다
- 웹 인터페이스는 HTML, CSS 및 JavaScript로 구축되었습니다
- HTML 렌더링을 위해 Jinja2 템플릿이 사용됩니다
- 애플리케이션은 CSS 및 JavaScript 파일을 위한 정적 파일 서빙을 사용합니다
