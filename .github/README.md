# Saegil LLM Server

FastAPI 기반 LLM API 서버로, OpenAI API를 활용한 ChatGPT, 음성-텍스트 변환(STT), 텍스트-음성 변환(TTS), OpenAI Assistant API 기능을 제공합니다.

## API 사용 가이드

### 기본 URL

```
http://[server-address]/api/v1
```

## 1. ChatGPT API

텍스트 쿼리를 ChatGPT에 전송하여 응답을 받습니다.

### 텍스트 쿼리 요청

**엔드포인트**: `POST /chatgpt/`

**요청 본문**:

```json
{
  "text": "안녕하세요, 오늘 날씨가 어떤가요?"
}
```

**응답**:

```json
{
  "response": "안녕하세요! 제가 현재 날씨 정보에 직접 접근할 수는 없지만, 날씨가 궁금하시면 날씨 앱이나 웹사이트를 확인해보시는 것이 좋겠습니다. 오늘 하루 즐겁게 보내세요!"
}
```

### 음성 파일 업로드 후 ChatGPT 응답 요청

**엔드포인트**: `POST /chatgpt/upload`

**요청**: `multipart/form-data`로 오디오 파일 업로드

**응답**:

```json
{
  "response": "ChatGPT의 응답 텍스트",
  "text": "변환된 원본 음성 텍스트"
}
```

## 2. 음성-텍스트 변환(STT) API

음성을 텍스트로 변환합니다.

### URL에서 음성 변환

**엔드포인트**: `POST /speech-to-text/`

**요청 본문**:

```json
{
  "audio_url": "https://example.com/audio.mp3"
}
```

**응답**:

```json
{
  "text": "변환된 텍스트"
}
```

### 음성 파일 업로드 후 변환

**엔드포인트**: `POST /speech-to-text/upload`

**요청**: `multipart/form-data`로 오디오 파일 업로드

**응답**:

```json
{
  "text": "변환된 텍스트"
}
```

## 3. 텍스트-음성 변환(TTS) API

텍스트를 음성으로 변환합니다.

**엔드포인트**: `POST /text-to-speech/`

**요청 본문**:
```json
{
  "text": "음성으로 변환할 텍스트",
  "provider": "openai"
}
```

**쿼리 파라미터**:

- `provider`: (선택) "elevenlabs" 또는 "openai" (요청 본문의 provider보다 우선함)

**응답**: 오디오 스트림 (MP3 형식)

## 4. STT-ChatGPT-TTS 통합 API

음성을 텍스트로 변환하고, ChatGPT 응답을 받은 후, 다시 음성으로 변환하는 통합 과정을 수행합니다.

### 음성 파일 업로드 후 음성 응답 받기

**엔드포인트**: `POST /stt-chatgpt-tts/upload`

**요청**: `multipart/form-data`로 오디오 파일 업로드

**응답**: 오디오 스트림 (MP3 형식)

### 음성 파일 업로드 후 JSON 응답 받기

**엔드포인트**: `POST /stt-chatgpt-tts/upload/json`

**요청**: `multipart/form-data`로 오디오 파일 업로드

**응답**:
```json
{
  "text": "변환된 원본 음성 텍스트",
  "response": "ChatGPT의 응답 텍스트",
  "audio_url": "/stt-chatgpt-tts/audio/[uuid].mp3"
}
```

## 5. OpenAI Assistant API

OpenAI의 Assistant API를 활용하여 대화 문맥을 유지한 응답을 제공합니다.

### 텍스트 쿼리 요청

**엔드포인트**: `POST /assistant/`

**요청 본문**:
```json
{
  "text": "안녕하세요, 저는 김철수입니다.",
  "thread_id": "thread_abc123"
}
```

**쿼리 파라미터**:

- `thread_id`: (선택) 대화 스레드 ID (요청 본문의 thread_id보다 우선함)

**응답**:

```json
{
  "response": "안녕하세요, 김철수님! 무엇을 도와드릴까요?",
  "thread_id": "thread_abc123",
  "text": "안녕하세요, 저는 김철수입니다."
}
```

### 음성 파일 업로드 후 Assistant 응답 요청

**엔드포인트**: `POST /assistant/upload`

**요청**: `multipart/form-data`로 오디오 파일 업로드

**쿼리 파라미터**:

- `thread_id`: (선택) 대화 스레드 ID

**응답**:

```json
{
  "response": "Assistant의 응답 텍스트",
  "thread_id": "thread_abc123",
  "text": "변환된 원본 음성 텍스트"
}
```

### 텍스트 쿼리 요청 후 음성 응답 받기

**엔드포인트**: `POST /assistant/audio`

**요청 본문**:

```json
{
  "text": "안녕하세요, 저는 김철수입니다.",
  "thread_id": "thread_abc123"
}
```

**쿼리 파라미터**:

- `thread_id`: (선택) 대화 스레드 ID (요청 본문의 thread_id보다 우선함)
- `provider`: (선택) "elevenlabs" 또는 "openai" (기본값: "openai")

**응답**: 오디오 스트림 (MP3 형식)

### 음성 파일 업로드 후 음성 응답 받기

**엔드포인트**: `POST /assistant/upload/audio`

**요청**: `multipart/form-data`로 오디오 파일 업로드

**쿼리 파라미터**:

- `thread_id`: (선택) 대화 스레드 ID
- `provider`: (선택) "elevenlabs" 또는 "openai" (기본값: "openai")

**응답**: 오디오 스트림 (MP3 형식)

## 오류 처리

모든 API 엔드포인트는 오류 발생 시 적절한 HTTP 상태 코드와 함께 오류 메시지를 반환합니다:

```json
{
  "detail": "오류 메시지"
}
```

일반적인 오류 코드:

- 400: 잘못된 요청 (예: 오디오 파일이 아닌 파일 업로드)
- 500: 서버 내부 오류 (API 호출 중 발생한 오류)

## SpringBoot에서 API 호출 예제 코드

### 1. 필요한 의존성 추가 (build.gradle.kts)

```kotlin
plugins {
    id("org.springframework.boot") version "3.2.0"
    id("io.spring.dependency-management") version "1.1.4"
    kotlin("jvm") version "1.9.22"
    kotlin("plugin.spring") version "1.9.22"
}

group = "com.example"
version = "0.0.1-SNAPSHOT"

java {
    sourceCompatibility = JavaVersion.VERSION_21
}

repositories {
    mavenCentral()
}

dependencies {
    // Spring Web
    implementation("org.springframework.boot:spring-boot-starter-web")
    
    // WebClient
    implementation("org.springframework.boot:spring-boot-starter-webflux")
}
```

자바 프로젝트인 경우 다음과 같이 작성할 수 있습니다:

```kotlin
plugins {
    id("org.springframework.boot") version "3.2.0"
    id("io.spring.dependency-management") version "1.1.4"
    id("java")
}

group = "com.example"
version = "0.0.1-SNAPSHOT"

java {
    sourceCompatibility = JavaVersion.VERSION_21
}

repositories {
    mavenCentral()
}

dependencies {
    // Spring Web
    implementation("org.springframework.boot:spring-boot-starter-web")
    
    // WebClient
    implementation("org.springframework.boot:spring-boot-starter-webflux")
}
```

### 2. API 호출을 위한 서비스 클래스 구현

```java
package com.example.demo.service;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.io.ByteArrayResource;
import org.springframework.core.io.Resource;
import org.springframework.http.*;
import org.springframework.stereotype.Service;
import org.springframework.util.LinkedMultiValueMap;
import org.springframework.util.MultiValueMap;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.multipart.MultipartFile;
import org.springframework.web.reactive.function.BodyInserters;
import org.springframework.web.reactive.function.client.WebClient;
import org.springframework.web.util.UriComponentsBuilder;

import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

@Service
public class SaegilLLMService {

    private final RestTemplate restTemplate;
    private final WebClient webClient;
    private final String baseUrl;

    public SaegilLLMService(
            RestTemplate restTemplate,
            WebClient.Builder webClientBuilder,
            @Value("${saegil.llm.base-url}") String baseUrl
    ) {
        this.restTemplate = restTemplate;
        this.webClient = webClientBuilder.baseUrl(baseUrl).build();
        this.baseUrl = baseUrl;
    }

    /**
     * ChatGPT API - 텍스트 쿼리 요청
     */
    public Map<String, Object> getChatGPTResponse(String text) {
        Map<String, Object> requestBody = new HashMap<>();
        requestBody.put("text", text);
        
        ResponseEntity<Map> response = restTemplate.exchange(
                baseUrl + "/chatgpt/",
                HttpMethod.POST,
                new HttpEntity<>(requestBody, createJsonHeaders()),
                Map.class
        );
        
        return response.getBody();
    }
    
    /**
     * ChatGPT API - 음성 파일 업로드 후 응답 요청
     */
    public Map<String, Object> getChatGPTResponseFromAudio(MultipartFile audioFile) throws IOException {
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.MULTIPART_FORM_DATA);
        
        MultiValueMap<String, Object> body = new LinkedMultiValueMap<>();
        body.add("file", createResource(audioFile));
        
        HttpEntity<MultiValueMap<String, Object>> requestEntity = new HttpEntity<>(body, headers);
        
        ResponseEntity<Map> response = restTemplate.exchange(
                baseUrl + "/chatgpt/upload",
                HttpMethod.POST,
                requestEntity,
                Map.class
        );
        
        return response.getBody();
    }
    
    /**
     * 음성-텍스트 변환(STT) API - URL에서 음성 변환
     */
    public Map<String, Object> convertSpeechToText(String audioUrl) {
        Map<String, Object> requestBody = new HashMap<>();
        requestBody.put("audio_url", audioUrl);
        
        ResponseEntity<Map> response = restTemplate.exchange(
                baseUrl + "/speech-to-text/",
                HttpMethod.POST,
                new HttpEntity<>(requestBody, createJsonHeaders()),
                Map.class
        );
        
        return response.getBody();
    }
    
    /**
     * 음성-텍스트 변환(STT) API - 음성 파일 업로드 후 변환
     */
    public Map<String, Object> convertSpeechToTextFromFile(MultipartFile audioFile) throws IOException {
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.MULTIPART_FORM_DATA);
        
        MultiValueMap<String, Object> body = new LinkedMultiValueMap<>();
        body.add("file", createResource(audioFile));
        
        HttpEntity<MultiValueMap<String, Object>> requestEntity = new HttpEntity<>(body, headers);
        
        ResponseEntity<Map> response = restTemplate.exchange(
                baseUrl + "/speech-to-text/upload",
                HttpMethod.POST,
                requestEntity,
                Map.class
        );
        
        return response.getBody();
    }
    
    /**
     * 텍스트-음성 변환(TTS) API - 텍스트를 음성으로 변환 (바이트 배열로 수신)
     */
    public byte[] convertTextToSpeech(String text, String provider) {
        Map<String, Object> requestBody = new HashMap<>();
        requestBody.put("text", text);
        if (provider != null) {
            requestBody.put("provider", provider);
        }
        
        String uri = UriComponentsBuilder.fromHttpUrl(baseUrl + "/text-to-speech/")
                .queryParamIfPresent("provider", provider != null ? java.util.Optional.of(provider) : java.util.Optional.empty())
                .toUriString();
        
        ResponseEntity<byte[]> response = restTemplate.exchange(
                uri,
                HttpMethod.POST,
                new HttpEntity<>(requestBody, createJsonHeaders()),
                byte[].class
        );
        
        return response.getBody();
    }
    
    /**
     * 텍스트-음성 변환(TTS) API - 텍스트를 음성으로 변환 (WebClient 사용하여 스트리밍)
     */
    public byte[] streamTextToSpeech(String text, String provider) {
        Map<String, Object> requestBody = new HashMap<>();
        requestBody.put("text", text);
        
        return webClient.post()
                .uri(uriBuilder -> uriBuilder
                        .path("/text-to-speech/")
                        .queryParamIfPresent("provider", provider != null ? java.util.Optional.of(provider) : java.util.Optional.empty())
                        .build())
                .contentType(MediaType.APPLICATION_JSON)
                .body(BodyInserters.fromValue(requestBody))
                .retrieve()
                .bodyToMono(byte[].class)
                .block();
    }
    
    /**
     * STT-ChatGPT-TTS 통합 API - 음성 파일 업로드 후 JSON 응답 받기
     */
    public Map<String, Object> processSTTChatGPTTTSJson(MultipartFile audioFile) throws IOException {
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.MULTIPART_FORM_DATA);
        
        MultiValueMap<String, Object> body = new LinkedMultiValueMap<>();
        body.add("file", createResource(audioFile));
        
        HttpEntity<MultiValueMap<String, Object>> requestEntity = new HttpEntity<>(body, headers);
        
        ResponseEntity<Map> response = restTemplate.exchange(
                baseUrl + "/stt-chatgpt-tts/upload/json",
                HttpMethod.POST,
                requestEntity,
                Map.class
        );
        
        return response.getBody();
    }
    
    /**
     * STT-ChatGPT-TTS 통합 API - 음성 파일 업로드 후 음성 응답 받기 (바이트 배열)
     */
    public byte[] processSTTChatGPTTTSAudio(MultipartFile audioFile) throws IOException {
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.MULTIPART_FORM_DATA);
        
        MultiValueMap<String, Object> body = new LinkedMultiValueMap<>();
        body.add("file", createResource(audioFile));
        
        HttpEntity<MultiValueMap<String, Object>> requestEntity = new HttpEntity<>(body, headers);
        
        ResponseEntity<byte[]> response = restTemplate.exchange(
                baseUrl + "/stt-chatgpt-tts/upload",
                HttpMethod.POST,
                requestEntity,
                byte[].class
        );
        
        return response.getBody();
    }
    
    /**
     * Assistant API - 텍스트 쿼리 요청
     */
    public Map<String, Object> getAssistantResponse(String text, String threadId) {
        Map<String, Object> requestBody = new HashMap<>();
        requestBody.put("text", text);
        if (threadId != null) {
            requestBody.put("thread_id", threadId);
        }
        
        String uri = UriComponentsBuilder.fromHttpUrl(baseUrl + "/assistant/")
                .queryParamIfPresent("thread_id", threadId != null ? java.util.Optional.of(threadId) : java.util.Optional.empty())
                .toUriString();
        
        ResponseEntity<Map> response = restTemplate.exchange(
                uri,
                HttpMethod.POST,
                new HttpEntity<>(requestBody, createJsonHeaders()),
                Map.class
        );
        
        return response.getBody();
    }
    
    /**
     * Assistant API - 음성 파일 업로드 후 응답 요청
     */
    public Map<String, Object> getAssistantResponseFromAudio(MultipartFile audioFile, String threadId) throws IOException {
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.MULTIPART_FORM_DATA);
        
        MultiValueMap<String, Object> body = new LinkedMultiValueMap<>();
        body.add("file", createResource(audioFile));
        
        String uri = UriComponentsBuilder.fromHttpUrl(baseUrl + "/assistant/upload")
                .queryParamIfPresent("thread_id", threadId != null ? java.util.Optional.of(threadId) : java.util.Optional.empty())
                .toUriString();
        
        HttpEntity<MultiValueMap<String, Object>> requestEntity = new HttpEntity<>(body, headers);
        
        ResponseEntity<Map> response = restTemplate.exchange(
                uri,
                HttpMethod.POST,
                requestEntity,
                Map.class
        );
        
        return response.getBody();
    }
    
    /**
     * Assistant API - 텍스트 쿼리 후 음성 응답 받기
     */
    public byte[] getAssistantAudioResponse(String text, String threadId, String provider) {
        Map<String, Object> requestBody = new HashMap<>();
        requestBody.put("text", text);
        if (threadId != null) {
            requestBody.put("thread_id", threadId);
        }
        
        String uri = UriComponentsBuilder.fromHttpUrl(baseUrl + "/assistant/audio")
                .queryParamIfPresent("thread_id", threadId != null ? java.util.Optional.of(threadId) : java.util.Optional.empty())
                .queryParamIfPresent("provider", provider != null ? java.util.Optional.of(provider) : java.util.Optional.empty())
                .toUriString();
        
        ResponseEntity<byte[]> response = restTemplate.exchange(
                uri,
                HttpMethod.POST,
                new HttpEntity<>(requestBody, createJsonHeaders()),
                byte[].class
        );
        
        return response.getBody();
    }
    
    /**
     * Helper 메소드 - JSON용 헤더 생성
     */
    private HttpHeaders createJsonHeaders() {
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);
        return headers;
    }
    
    /**
     * Helper 메소드 - MultipartFile을 Resource로 변환
     */
    private Resource createResource(MultipartFile file) throws IOException {
        return new ByteArrayResource(file.getBytes()) {
            @Override
            public String getFilename() {
                return file.getOriginalFilename();
            }
        };
    }
}
```

### 3. 구성 파일 (application.properties 또는 application.yml)

```properties
# application.properties
saegil.llm.base-url=http://localhost:8000/api/v1
```

### 4. RestTemplate 및 WebClient 설정

```java
package com.example.demo.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.reactive.function.client.ExchangeStrategies;
import org.springframework.web.reactive.function.client.WebClient;

@Configuration
public class WebClientConfig {

    @Bean
    public RestTemplate restTemplate() {
        return new RestTemplate();
    }
    
    @Bean
    public WebClient.Builder webClientBuilder() {
        return WebClient.builder()
                .exchangeStrategies(ExchangeStrategies.builder()
                        .codecs(configurer -> configurer
                                .defaultCodecs()
                                .maxInMemorySize(16 * 1024 * 1024)) // 16MB 제한 설정
                        .build());
    }
}
```

### 5. 컨트롤러 예제 - API 호출

```java
package com.example.demo.controller;

import com.example.demo.service.SaegilLLMService;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.util.Map;

@RestController
@RequestMapping("/api/llm")
public class LlmController {

    private final SaegilLLMService llmService;
    
    public LlmController(SaegilLLMService llmService) {
        this.llmService = llmService;
    }
    
    @PostMapping("/chatgpt")
    public ResponseEntity<Map<String, Object>> getChatGPTResponse(@RequestBody Map<String, String> request) {
        Map<String, Object> response = llmService.getChatGPTResponse(request.get("text"));
        return ResponseEntity.ok(response);
    }
    
    @PostMapping("/chatgpt/upload")
    public ResponseEntity<Map<String, Object>> getChatGPTResponseFromAudio(@RequestParam("file") MultipartFile file) throws IOException {
        Map<String, Object> response = llmService.getChatGPTResponseFromAudio(file);
        return ResponseEntity.ok(response);
    }
    
    @PostMapping("/speech-to-text")
    public ResponseEntity<Map<String, Object>> convertSpeechToText(@RequestBody Map<String, String> request) {
        Map<String, Object> response = llmService.convertSpeechToText(request.get("audio_url"));
        return ResponseEntity.ok(response);
    }
    
    @PostMapping("/speech-to-text/upload")
    public ResponseEntity<Map<String, Object>> convertSpeechToTextFromFile(@RequestParam("file") MultipartFile file) throws IOException {
        Map<String, Object> response = llmService.convertSpeechToTextFromFile(file);
        return ResponseEntity.ok(response);
    }
    
    @PostMapping("/text-to-speech")
    public ResponseEntity<byte[]> convertTextToSpeech(
            @RequestBody Map<String, String> request,
            @RequestParam(value = "provider", required = false) String provider
    ) {
        byte[] audioData = llmService.convertTextToSpeech(request.get("text"), provider);
        return ResponseEntity.ok()
                .contentType(MediaType.parseMediaType("audio/mpeg"))
                .header(HttpHeaders.CONTENT_DISPOSITION, "attachment; filename=speech.mp3")
                .body(audioData);
    }
    
    @PostMapping("/stt-chatgpt-tts/upload")
    public ResponseEntity<byte[]> processSTTChatGPTTTSAudio(@RequestParam("file") MultipartFile file) throws IOException {
        byte[] audioData = llmService.processSTTChatGPTTTSAudio(file);
        return ResponseEntity.ok()
                .contentType(MediaType.parseMediaType("audio/mpeg"))
                .header(HttpHeaders.CONTENT_DISPOSITION, "attachment; filename=response.mp3")
                .body(audioData);
    }
    
    @PostMapping("/stt-chatgpt-tts/upload/json")
    public ResponseEntity<Map<String, Object>> processSTTChatGPTTTSJson(@RequestParam("file") MultipartFile file) throws IOException {
        Map<String, Object> response = llmService.processSTTChatGPTTTSJson(file);
        return ResponseEntity.ok(response);
    }
    
    @PostMapping("/assistant")
    public ResponseEntity<Map<String, Object>> getAssistantResponse(
            @RequestBody Map<String, String> request,
            @RequestParam(value = "thread_id", required = false) String threadIdParam
    ) {
        String text = request.get("text");
        String threadId = threadIdParam != null ? threadIdParam : request.get("thread_id");
        
        Map<String, Object> response = llmService.getAssistantResponse(text, threadId);
        return ResponseEntity.ok(response);
    }
    
    @PostMapping("/assistant/upload")
    public ResponseEntity<Map<String, Object>> getAssistantResponseFromAudio(
            @RequestParam("file") MultipartFile file,
            @RequestParam(value = "thread_id", required = false) String threadId
    ) throws IOException {
        Map<String, Object> response = llmService.getAssistantResponseFromAudio(file, threadId);
        return ResponseEntity.ok(response);
    }
    
    @PostMapping("/assistant/audio")
    public ResponseEntity<byte[]> getAssistantAudioResponse(
            @RequestBody Map<String, String> request,
            @RequestParam(value = "thread_id", required = false) String threadIdParam,
            @RequestParam(value = "provider", required = false) String provider
    ) {
        String text = request.get("text");
        String threadId = threadIdParam != null ? threadIdParam : request.get("thread_id");
        
        byte[] audioData = llmService.getAssistantAudioResponse(text, threadId, provider);
        return ResponseEntity.ok()
                .contentType(MediaType.parseMediaType("audio/mpeg"))
                .header(HttpHeaders.CONTENT_DISPOSITION, "attachment; filename=assistant_response.mp3")
                .body(audioData);
    }
}
```