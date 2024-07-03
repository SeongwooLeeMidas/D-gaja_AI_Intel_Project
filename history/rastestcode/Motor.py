import RPi.GPIO as GPIO     # 라즈베리파이 GPIO 관련 모듈을 불러옴
import time 

GPIO.setmode(GPIO.BCM)      # GPIO 핀들의 번호를 지정하는 규칙 설정


class Motor:
    
    def __init__(self,servo_pin,step_pins):
        self.servo =0 #서보 핀 설정 
        self.servo_min_duty = 3 #최소 듀티비
        self.servo_max_duty =12 #최대 듀티비
        self.hor_degree = 0 #수직 각도
        self.ver_degree = 0 #수평 각도 
        self.StepPins = step_pins
        self.StepCounter = 0
        self.StepCount = 4
        self.delay = 0.003
        self.Seq = [[0,0,1,1],
                    [0,1,1,0],
                    [1,1,0,0],
                    [1,0,0,1]]
        self.RevSeq = [
                [1, 0, 0, 1],
                [1, 1, 0, 0],
                [0, 1, 1, 0],
                [0, 0, 1, 1]
            ]
            
        GPIO.setmode(GPIO.BCM)

        GPIO.setup(servo_pin, GPIO.OUT)  # 서보핀을 출력으로 설정 

        self.servo = GPIO.PWM(servo_pin, 50)  # 서보핀을 PWM 모드 50Hz로 사용
        self.servo.start(0)  # 서보모터의 초기값을 0으로 설정
        for pin in self.StepPins:
            GPIO.setup(pin,GPIO.OUT)
            GPIO.output(pin,False)        

    def step(self,direct_right): #모터 구동  direct_right = 1 : 정방향, 0 : 역방향  
        for _ in range(32):
            if direct_right:
                for pin in range(4):
                    xpin = self.StepPins[pin]
                    if self.Seq[self.StepCounter][pin] != 0:
                        GPIO.output(xpin, True)
                    else:
                        GPIO.output(xpin, False)
                #self.rightcount = self.rightcount + 1

            else:
                for pin in range(4):
                    xpin = self.StepPins[pin]
                    if self.RevSeq[self.StepCounter][pin] != 0:
                        GPIO.output(xpin, True)
                    else:
                        GPIO.output(xpin, False)
                #self.rightcount = self.rightcount - 1

                

            self.StepCounter += 1
            if self.StepCounter == self.StepCount:
                self.StepCounter = 0

            time.sleep(self.delay)

    def degree_clamp(self,degree):
        if degree>180: degree=180
        if degree<0: degree =0
        return degree
    def set_servo_degree(self,degree):    # 각도를 입력하면 듀티비를 알아서 설정해주는 함수
        # 각도는 최소0, 최대 180으로 설정
        if degree > 180:
            degree = degree-180
        elif degree < 0:
            degree = 180 + degree
        # 입력한 각도(degree)를 듀티비로 환산하는 식
        duty = self.servo_min_duty+(degree*(self.servo_max_duty-self.servo_min_duty)/180.0)
        # 환산한 듀티비를 서보모터에 전달
        self.servo.ChangeDutyCycle(duty)

    def input(self,up,down,left,right):
        if up: self.hor_degree = self.hor_degree+ 2
        if down : self.hor_degree = self.hor_degree -2
        if left : self.step(0)
        if right :self.step(1)
        self.hor_degree = self.degree_clamp(self.hor_degree)
        self.set_servo_degree(self.hor_degree)

    def decode(self,key):
        up = down = left = right =0
        if key == 'q':
            up = 1
            left = 1
        elif key =='w':
            up=1
        elif key =='e':
            up =1 
            right =1
        elif key =='a':
            left =1
        elif key =='d':
            right=1
        elif key =='z':
            left =1
            down=1
        elif key =='x':
            down =1
        elif key =='c':
            down =1
            right =1  
        self.input(up,down,left,right)
