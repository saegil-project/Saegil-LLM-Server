import os
import tempfile
import time

import pygame
from text_to_speech_stream import text_to_speech_stream


def play_audio_stream(audio_stream):
    """
    pygame을 사용하여 BytesIO 스트림에서 오디오를 재생합니다.
    """
    # pygame 믹서를 초기화합니다.
    pygame.mixer.init()

    # 오디오를 저장할 임시 파일을 생성합니다.
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_file:
        temp_filename = temp_file.name
        # 오디오 데이터를 임시 파일에 씁니다.
        temp_file.write(audio_stream.read())

    try:
        # 오디오 파일을 로드하고 재생합니다.
        pygame.mixer.music.load(temp_filename)
        pygame.mixer.music.play()

        # 오디오 재생이 끝날 때까지 대기합니다.
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    finally:
        # 임시 파일을 정리합니다.
        if os.path.exists(temp_filename):
            os.unlink(temp_filename)

def speak_sentences(sentences):
    """
    문장 목록을 음성으로 변환하여 하나씩 재생합니다.
    """
    for sentence in sentences:
        print(f"Speaking: {sentence}")
        # 텍스트를 음성으로 변환합니다.
        audio_stream = text_to_speech_stream(sentence)
        # 오디오를 재생합니다.
        play_audio_stream(audio_stream)
        # 문장 사이에 잠시 대기합니다.
        time.sleep(0.5)

# 재생할 문장 목록
sentences = [
    "안녕하세요, ElevenLabs 텍스트 음성 변환 데모에 오신 것을 환영합니다.",
    "이는 여러 문장을 음성으로 변환하는 예시입니다.",
    "text_to_speech_stream 함수는 고품질 오디오 생성을 쉽게 만들어줍니다.",
    "이 데모를 들어주셔서 감사합니다."
]

# 모든 문장을 변환하고 재생합니다.
speak_sentences(sentences)

# 아래와 같이 단일 문장을 변환하고 재생할 수도 있습니다:
# audio_stream = text_to_speech_stream("안녕하세요, Elevenlabs API 사용하기 어렵습니다!!")
# play_audio_stream(audio_stream)
