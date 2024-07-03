import RPi.GPIO as GPIO     # 라즈베리파이 GPIO 관련 모듈을 불러옴
from time import sleep      #time 라이브러리의 sleep함수 사용

GPIO.setmode(GPIO.BCM)      # GPIO 핀들의 번호를 지정하는 규칙 설정

### 이부분은 아두이노 코딩의 setup()에 해당합니다
servo_pin = 12                   # 서보핀은 라즈베리파이 GPIO 12번핀으로 

GPIO.setup(servo_pin, GPIO.OUT)  # 서보핀을 출력으로 설정 
servo = GPIO.PWM(servo_pin, 50)  # 서보핀을 PWM 모드 50Hz로 사용
servo.start(0)  # 서보모터의 초기값을 0으로 설정

servo_min_duty = 3               # 최소 듀티비를 3으로
servo_max_duty = 12              # 최대 듀티비를 12로

def set_servo_degree(degree):    # 각도를 입력하면 듀티비를 알아서 설정해주는 함수
    # 각도는 최소0, 최대 180으로 설정
    if degree > 180:
        degree = degree-180
    elif degree < 0:
        degree = 180 + degree
    # 입력한 각도(degree)를 듀티비로 환산하는 식
    duty = servo_min_duty+(degree*(servo_max_duty-servo_min_duty)/180.0)
    # 환산한 듀티비를 서보모터에 전달
    servo.ChangeDutyCycle(duty)

### 이부분은 아두이노 코딩의 loop()에 해당합니다
try:                                    # 이 try 안의 구문을 먼저 수행하고
    while True:                         # 무한루프 시작: 아두이노의 loop()와 같음
        set_servo_degree(0)             # 서보모터의 각도를 0도로
        print("move")
        sleep(1)                        # 1초간 대기
        set_servo_degree(45)
        print("move")
        sleep(1)
        set_servo_degree(90)
        print("move")
        sleep(1)
        set_servo_degree(135)
        print("move")
        sleep(1)
        set_servo_degree(180)
        print("move")
        sleep(1)

### 이부분은 반드시 추가해주셔야 합니다.
finally:                                # try 구문이 종료되면
    GPIO.cleanup()                      # GPIO 핀들을 초기화

#
#      공대선배 라즈베리파이썬 #8-2 서보모터를 부드럽게 제어
#      youtube 바로가기: https://www.youtube.com/c/공대선배
#      for문을 이용해 서보모터를 부드럽게 제어하는 코드
#

import RPi.GPIO as GPIO     # 라즈베리파이 GPIO 관련 모듈을 불러옴
from time import sleep      #time 라이브러리의 sleep함수 사용

GPIO.setmode(GPIO.BCM)      # GPIO 핀들의 번호를 지정하는 규칙 설정

### 이부분은 아두이노 코딩의 setup()에 해당합니다
servo_pin = 12                   # 서보핀은 라즈베리파이 GPIO 12번핀으로 

GPIO.setup(servo_pin, GPIO.OUT)  # 서보핀을 출력으로 설정 
servo = GPIO.PWM(servo_pin, 50)  # 서보핀을 PWM 모드 50Hz로 사용
servo.start(0)  # 서보모터의 초기값을 0으로 설정

servo_min_duty = 3               # 최소 듀티비를 3으로 (#8-1에서 확인한 것)
servo_max_duty = 12              # 최대 듀티비를 12로 (#8-1에서 확인한 것)
def set_servo_degree(degree):    # 각도를 입력하면 듀티비를 알아서 설정해주는 함수
    # 각도는 최소0, 최대 180으로 설정
    if degree > 180:
        degree = 180
    elif degree < 0:
        degree = 0

    # 입력한 각도(degree)를 듀티비로 환산하는 식
    duty = servo_min_duty+(degree*(servo_max_duty-servo_min_duty)/180.0)
    # 환산한 듀티비를 서보모터에 전달
    servo.ChangeDutyCycle(duty)

### 이부분은 아두이노 코딩의 loop()에 해당합니다
try:                                    # 이 try 안의 구문을 먼저 수행하고
    while True:                         # 무한루프 시작: 아두이노의 loop()와 같음
        for ii in range(0, 180, 5):     # 0부터 180까지 5단위로 ii가 변하는 루프
            set_servo_degree(ii)        # ii만큼 서보모터를 움직여줌
            sleep(0.1)                  # 0.1초간 대기
        for ii in reversed(range(0, 180, 5)):   # 180부터 0까지 5단위로 ii가 변하는 루프
            set_servo_degree(ii)
            sleep(0.1)

### 이부분은 반드시 추가해주셔야 합니다.
finally:                                # try 구문이 종료되면
    GPIO.cleanup()                      # GPIO 핀들을 초기화    