# 베이스 이미지
FROM python:3.12-slim

# ffmpeg 설치에 필요한 도구 먼저 설치 후 ffmpeg 설치
RUN apt-get update && \
    apt-get install -y ffmpeg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# 작업 디렉토리 설정
WORKDIR /app

# 종속성 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 파일 복사
COPY . .

# 포트 노출
EXPOSE 9090

# FastAPI 실행 명령
CMD ["uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "9090"]
