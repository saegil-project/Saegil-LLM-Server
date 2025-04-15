# Saegil-LLM-Server

## 사용 방법

### API 사용

#### 텍스트를 음성으로 변환 (TTS)

텍스트를 음성으로 변환하는 API 엔드포인트:

- 엔드포인트: `/text-to-speech/`
- 메소드: POST
- 요청 형식: JSON (`{"text": "변환할 텍스트"}`)
- 응답: MP3 형식의 오디오 스트림

이 API는 `/app/api/v1/text_to_speech_controller.py` 파일에 구현되어 있으며, ElevenLabs API를 사용하여 텍스트를 고품질 음성으로 변환합니다. 클라이언트는 이 API를
호출하여 텍스트를
보내고, 응답으로 MP3 오디오 파일을 받을 수 있습니다.

```bash
curl -X POST "http://localhost:9090/text-to-speech/" \
     -H "Content-Type: application/json" \
     -d '{"text":"안녕하세요, 반갑습니다."}'
```

응답으로 MP3 형식의 오디오 스트림이 반환됩니다.

#### 음성을 텍스트로 변환 (STT)

음성을 텍스트로 변환하는 API 엔드포인트는 두 가지 방식을 지원합니다:

##### 1. URL을 통한 오디오 변환

- 엔드포인트: `/speech-to-text/`
- 메소드: POST
- 요청 형식: JSON (`{"audio_url": "변환할 오디오 파일의 URL"}`)
- 응답: JSON (`{"text": "변환된 텍스트"}`)

이 API는 오디오 파일의 URL을 받아 해당 파일을 다운로드하고 텍스트로 변환합니다.

```bash
curl -X POST "http://localhost:9090/speech-to-text/" \
     -H "Content-Type: application/json" \
     -d '{"audio_url":"https://example.com/audio/sample.mp3"}'
```

##### 2. MP3 파일 직접 업로드

- 엔드포인트: `/speech-to-text/upload`
- 메소드: POST
- 요청 형식: 멀티파트 폼 데이터 (파일 필드 이름: `file`)
- 응답: JSON (`{"text": "변환된 텍스트"}`)

이 API는 MP3 파일을 직접 업로드하여 텍스트로 변환할 수 있습니다.

```bash
curl -X POST "http://localhost:9090/speech-to-text/upload" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@/path/to/your/audio.mp3"
```

두 엔드포인트 모두 응답 예시:
```json
{
  "text": "안녕하세요, 이것은 음성에서 변환된 텍스트입니다."
}
```

이 API는 `/app/api/v1/speech_to_text_controller.py` 파일에 구현되어 있으며, OpenAI Whisper API를 사용하여 음성을 텍스트로 변환합니다.

#### ChatGPT를 통한 텍스트 응답 (ChatGPT)

ChatGPT를 통해 텍스트 응답을 받는 API 엔드포인트는 두 가지 방식을 지원합니다:

##### 1. 텍스트 쿼리를 통한 응답

- 엔드포인트: `/chatgpt/`
- 메소드: POST
- 요청 형식: JSON (`{"text": "ChatGPT에게 보낼 텍스트 쿼리"}`)
- 응답: JSON (`{"response": "ChatGPT의 응답 텍스트"}`)

이 API는 텍스트 쿼리를 받아 ChatGPT 응답을 반환합니다.

```bash
curl -X POST "http://localhost:9090/chatgpt/" \
     -H "Content-Type: application/json" \
     -d '{"text":"안녕하세요, 오늘 날씨가 어떤가요?"}'
```

##### 2. MP3 파일 직접 업로드를 통한 응답

- 엔드포인트: `/chatgpt/upload`
- 메소드: POST
- 요청 형식: 멀티파트 폼 데이터 (파일 필드 이름: `file`)
- 응답: JSON (`{"response": "ChatGPT의 응답 텍스트", "text": "STT로 변환된 원본 텍스트"}`)

이 API는 MP3 파일을 직접 업로드하여 텍스트로 변환한 후 ChatGPT 응답을 반환합니다.

```bash
curl -X POST "http://localhost:9090/chatgpt/upload" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@/path/to/your/audio.mp3"
```

ChatGPT 엔드포인트의 응답 예시:

```json
{
   "response": "안녕하세요! 오늘 날씨는 지역에 따라 다를 수 있습니다. 특정 지역을 알려주시면 더 정확한 정보를 제공해 드릴 수 있습니다.",
   "text": "오늘 날씨가 어떤가요?"
}
```

텍스트 쿼리 응답에서는 "text" 필드가 포함되지 않습니다.

이 API는 `/app/api/v1/chatgpt_controller.py` 파일에 구현되어 있으며, OpenAI GPT-4o 모델을 사용하여 텍스트 쿼리에 대한 응답을 생성합니다.

#### STT-ChatGPT-TTS 통합 처리 (STT-ChatGPT-TTS)

STT-ChatGPT-TTS 통합 처리 API 엔드포인트는 음성을 텍스트로 변환하고, ChatGPT 응답을 생성한 후, 응답을 음성으로 변환하는 통합 기능을 제공합니다:

##### 1. MP3 파일 업로드를 통한 통합 처리 (오디오 응답)

- 엔드포인트: `/stt-chatgpt-tts/upload`
- 메소드: POST
- 요청 형식: 멀티파트 폼 데이터 (파일 필드 이름: `file`)
- 응답: MP3 형식의 오디오 스트림

이 API는 MP3 파일을 업로드하여 음성을 텍스트로 변환하고, ChatGPT 응답을 생성한 후, 응답을 음성으로 변환하여 오디오 스트림으로 반환합니다.

```bash
curl -X POST "http://localhost:9090/stt-chatgpt-tts/upload" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@/path/to/your/audio.mp3" \
     --output response.mp3
```

응답으로 MP3 형식의 오디오 스트림이 반환됩니다.

##### 2. MP3 파일 업로드를 통한 통합 처리 (JSON 응답)

- 엔드포인트: `/stt-chatgpt-tts/upload/json`
- 메소드: POST
- 요청 형식: 멀티파트 폼 데이터 (파일 필드 이름: `file`)
- 응답: JSON (`{"text": "변환된 텍스트", "response": "ChatGPT의 응답 텍스트", "audio_url": "생성된 오디오 파일의 URL"}`)

이 API는 MP3 파일을 업로드하여 음성을 텍스트로 변환하고, ChatGPT 응답을 생성한 후, 응답 정보를 JSON으로 반환합니다.

```bash
curl -X POST "http://localhost:9090/stt-chatgpt-tts/upload/json" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@/path/to/your/audio.mp3"
```

응답 예시:

```json
{
  "text": "오늘 날씨가 어떤가요?",
  "response": "안녕하세요! 오늘 날씨는 지역에 따라 다를 수 있습니다. 특정 지역을 알려주시면 더 정확한 정보를 제공해 드릴 수 있습니다.",
  "audio_url": "/stt-chatgpt-tts/audio/response.mp3"
}
```

이 API는 `/app/api/v1/stt_chatgpt_tts_controller.py` 파일에 구현되어 있으며, 음성-텍스트 변환, ChatGPT 응답 생성, 텍스트-음성 변환을 통합하여 처리합니다.

## API 문서

FastAPI의 자동 생성 문서는 다음 URL에서 확인할 수 있습니다:

- Swagger UI: `http://localhost:9090/docs`
- ReDoc: `http://localhost:9090/redoc`
- OpenAPI JSON 스키마: `http://localhost:9090/openapi.json`

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
- `POST /speech-to-text/`: URL을 통해 음성을 텍스트로 변환
- `POST /speech-to-text/upload`: MP3 파일 업로드를 통해 음성을 텍스트로 변환
- `POST /chatgpt/`: 텍스트 쿼리를 통해 ChatGPT 응답 가져오기
- `POST /chatgpt/upload`: MP3 파일 업로드를 통해 음성을 텍스트로 변환한 후 ChatGPT 응답 가져오기
- `POST /stt-chatgpt-tts/upload`: MP3 파일 업로드를 통해 음성을 텍스트로 변환, ChatGPT 응답 생성, 응답을 음성으로 변환하여 반환
- `POST /stt-chatgpt-tts/upload/json`: MP3 파일 업로드를 통해 음성을 텍스트로 변환, ChatGPT 응답 생성, 응답 정보를 JSON으로 반환

### API 태그

API 엔드포인트는 다음과 같은 태그로 구분됩니다:

- **text-to-speech**: 텍스트를 음성으로 변환하는 엔드포인트
- **speech-to-text**: 음성을 텍스트로 변환하는 엔드포인트
- **chatgpt**: ChatGPT를 통한 텍스트 응답 관련 엔드포인트
- **stt-chatgpt-tts**: 음성-텍스트 변환, ChatGPT 응답, 텍스트-음성 변환을 통합한 엔드포인트
- **frontend**: 웹 애플리케이션 프론트엔드 관련 엔드포인트

## 주의사항

- ElevenLabs API는 사용량에 따라 요금이 부과될 수 있습니다.
- OpenAI API는 사용량에 따라 요금이 부과될 수 있습니다.
    - Whisper 모델(음성-텍스트 변환)
    - GPT-4o 모델(ChatGPT 응답)은 토큰 사용량에 따라 더 높은 요금이 부과될 수 있습니다.

## 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.
