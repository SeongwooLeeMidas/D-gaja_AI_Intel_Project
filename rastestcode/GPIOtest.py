import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)  # GPIO 경고를 비활성화

GPIO.setmode(GPIO.BCM)  # GPIO 핀 번호를 BCM 방식으로 설정

LED_PIN = 26  # LED가 연결된 GPIO 핀 번호

GPIO.setup(LED_PIN, GPIO.OUT)  # LED_PIN을 출력 모드로 설정

try:
    for i in range(20):  # 20번 반복
        GPIO.output(LED_PIN, GPIO.HIGH)  # LED를 켭니다 (HIGH = 1)
        time.sleep(1)  # 1초 대기
        GPIO.output(LED_PIN, GPIO.LOW)  # LED를 끕니다 (LOW = 0)
        time.sleep(1)  # 1초 대기

except KeyboardInterrupt:
    print("프로그램이 종료되었습니다.")

finally:
    GPIO.cleanup()  # GPIO 설정 초기화
