import time

import RPi.GPIO as GPIO

 

GPIO.setmode(GPIO.BCM)

StepPins = [8,9,10,11]

 

#핀 출력 설정

for pin in StepPins:

  GPIO.setup(pin,GPIO.OUT)

  GPIO.output(pin,False)

 

StepCounter = 0 

 

# 싱글 코일 여자 방식 시퀀스

StepCount = 4

Seq = [[0,0,0,1],

       [0,0,1,0],

       [0,1,0,0],

       [1,0,0,0]]

 

try:

    while 1: 
        for pin in range(0, 4):

            xpin = StepPins[pin]

            if Seq[StepCounter][pin]!=0: 

                GPIO.output(xpin, True)

            else:

                GPIO.output(xpin, False)

        StepCounter += 1 

        # 시퀀스가 끝나면 다시 시작

        if (StepCounter==StepCount):

            StepCounter = 0

        if (StepCounter<0):

            StepCounter = StepCount

        #다음 동작 기다리기

        time.sleep(0.01)

except KeyboardInterrupt: 

    GPIO.cleanup()