import pyaudio
import numpy as np
import wave

# 파라미터 설정
FORMAT = pyaudio.paInt16  # 오디오 포맷 설정 (16bit, 1채널)
CHANNELS = 1              # 마이크 채널 수
RATE = 44100              # 샘플 레이트 (비트레이트)
CHUNK = 1024              # 버퍼 사이즈 (오디오 데이터 읽기)
RECORD_SECONDS = 5        # 녹음할 시간 (초)
WAVE_OUTPUT_FILENAME = "output.wav"  # 저장할 WAV 파일 이름

# 오디오 입력 시작
audio = pyaudio.PyAudio()

stream = audio.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

print("마이크에서 소리 감지 및 저장 중...")

frames = []

try:
    for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

except KeyboardInterrupt:
    print("감지 및 녹음 종료")

finally:
    print("녹음 완료")

    # 스트림 정리
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # WAV 파일 작성
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    print(f"녹음된 소리를 {WAVE_OUTPUT_FILENAME}에 저장했습니다.")

