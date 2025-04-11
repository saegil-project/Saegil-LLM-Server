# Saegil-LLM-Server

Saegil-LLM-Server는 텍스트를 음성으로 변환하는 웹 애플리케이션 및 API 서버입니다. ElevenLabs의 음성 합성 기술을 활용하여 고품질 음성을 생성합니다.

## 프로젝트 개요

이 프로젝트는 다음과 같은 기능을 제공합니다:

- 텍스트를 음성으로 변환하는 REST API
- 사용자 친화적인 웹 인터페이스
- ElevenLabs API를 통한 고품질 음성 합성
- 생성된 음성 파일 다운로드 기능

## 아키텍처

### 기술 스택

- **백엔드**: FastAPI (Python)
- **프론트엔드**: HTML, CSS, JavaScript
- **템플릿 엔진**: Jinja2
- **음성 합성**: ElevenLabs API
- **서버**: Uvicorn (ASGI)
- **컨테이너화**: Docker

### 주요 컴포넌트

1. **FastAPI 애플리케이션**: 웹 서버 및 API 엔드포인트 제공
2. **텍스트-음성 변환 서비스**: ElevenLabs API와 통신하여 텍스트를 음성으로 변환
3. **웹 인터페이스**: 사용자가 텍스트를 입력하고 음성을 들을 수 있는 UI 제공

### 디렉토리 구조

```
Saegil-LLM-Server/
├── app/
│   ├── api/                 # API 라우터 및 엔드포인트
│   │   └── v1/              # API 버전 1
│   ├── core/                # 핵심 설정 및 유틸리티
│   ├── models/              # Pydantic 모델
│   ├── services/            # 비즈니스 로직 서비스
│   ├── static/              # 정적 파일 (CSS, JS)
│   ├── templates/           # HTML 템플릿
│   ├── test/                # 테스트 코드
│   └── main.py              # 애플리케이션 진입점
├── Dockerfile               # Docker 컨테이너 설정
└── requirements.txt         # 프로젝트 의존성
```

## 설치 방법

### 로컬 개발 환경

1. 저장소 클론:
   ```bash
   git clone https://github.com/your-username/Saegil-LLM-Server.git
   cd Saegil-LLM-Server
   ```

2. 가상 환경 생성 및 활성화:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. 의존성 설치:
   ```bash
   pip install -r requirements.txt
   ```

4. 환경 변수 설정:
   `.env` 파일을 생성하고 다음 내용을 추가:
   ```
   ELEVENLABS_API_KEY=your_elevenlabs_api_key
   ELEVENLABS_VOICE_ID=your_preferred_voice_id  # 기본값: uyVNoMrnUku1dZyVEXwD (Adam)
   ELEVENLABS_MODEL_ID=your_preferred_model_id  # 기본값: eleven_flash_v2_5
   ```

5. 애플리케이션 실행:
   ```bash
   uvicorn app.main:app --reload
   ```

6. 브라우저에서 `http://localhost:8000` 접속

### Docker를 이용한 배포

1. Docker 이미지 빌드:
   ```bash
   docker build -t saegil-llm-server .
   ```

2. Docker 컨테이너 실행:
   ```bash
   docker run -p 8000:8000 -e ELEVENLABS_API_KEY=your_api_key saegil-llm-server
   ```

3. 브라우저에서 `http://localhost:8000` 접속

## 사용 방법

### 웹 인터페이스

1. 브라우저에서 `http://localhost:8000` 접속
2. 텍스트 입력 필드에 변환하고 싶은 텍스트 입력
3. "Convert to Speech" 버튼 클릭
4. 생성된 음성을 재생하거나 다운로드

### API 사용

텍스트를 음성으로 변환하는 API 엔드포인트:

- 엔드포인트: `/text-to-speech/`
- 메소드: POST
- 요청 형식: JSON (`{"text": "변환할 텍스트"}`)
- 응답: MP3 형식의 오디오 스트림

이 API는 `/app/api/v1/text_to_speech.py` 파일에 구현되어 있으며, ElevenLabs API를 사용하여 텍스트를 고품질 음성으로 변환합니다. 클라이언트는 이 API를 호출하여 텍스트를
보내고, 응답으로 MP3 오디오 파일을 받을 수 있습니다.

```bash
curl -X POST "http://localhost:8000/text-to-speech/" \
     -H "Content-Type: application/json" \
     -d '{"text":"안녕하세요, 반갑습니다."}'
```

응답으로 MP3 형식의 오디오 스트림이 반환됩니다.

## API 문서

FastAPI의 자동 생성 문서는 다음 URL에서 확인할 수 있습니다:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
- OpenAPI JSON 스키마: `http://localhost:8000/openapi.json`

### Swagger UI 기능

Swagger UI는 클라이언트 개발자를 위한 강력한 도구로, 다음과 같은 기능을 제공합니다:

- **대화형 API 테스트**: 브라우저에서 직접 API 요청을 테스트할 수 있습니다.
- **요청/응답 예시**: 각 엔드포인트의 요청 및 응답 형식을 확인할 수 있습니다.
- **모델 스키마**: 요청 및 응답 데이터 모델의 상세 스키마를 확인할 수 있습니다.
- **인증 정보**: API 인증 방식에 대한 정보를 제공합니다.
- **요청 시간 표시**: API 요청 처리 시간을 확인할 수 있습니다.

### 주요 엔드포인트

- `GET /`: 웹 애플리케이션 메인 페이지
- `POST /text-to-speech/`: 텍스트를 음성으로 변환

### API 태그

API 엔드포인트는 다음과 같은 태그로 구분됩니다:

- **text-to-speech**: 텍스트를 음성으로 변환하는 엔드포인트
- **frontend**: 웹 애플리케이션 프론트엔드 관련 엔드포인트

## 주의사항

- ElevenLabs API는 사용량에 따라 요금이 부과될 수 있습니다.

## 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.
