import time
import RPi.GPIO as GPIO

class StepperMotor:
    def __init__(self, pins,input_delay): #input  핀할당배열, 속도 조절 input_delay : 1일반속도 2는 두배 
        GPIO.setmode(GPIO.BCM)
        self.StepPins = pins
        self.StepCounter = 0
        self.StepCount = 4
        self.delay = 0.01/input_delay
        self.rightcount = 0
        self.Seq = [
            [0, 0, 1, 1],
            [0, 1, 1, 0],
            [1, 1, 0, 0],
            [1, 0, 0, 1]
        ]
        self.RevSeq = [
            [1, 1, 0, 0],
            [0, 1, 1, 0],
            [0, 0, 1, 1],
            [1, 0, 0, 1]
        ]

        for pin in self.StepPins:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, False)

    def step(self,direct_right): #모터 구동  direct_right = 1 : 정방향 0 : 역방향  
        for _ in range(64):
            if direct_right:
                for pin in range(4):
                    xpin = self.StepPins[pin]
                    if self.Seq[self.StepCounter][pin] != 0:
                        GPIO.output(xpin, True)
                    else:
                        GPIO.output(xpin, False)
                self.rightcount = self.rightcount + 1

            else:
                for pin in range(4):
                    xpin = self.StepPins[pin]
                    if self.RevSeq[self.StepCounter][pin] != 0:
                        GPIO.output(xpin, True)
                    else:
                        GPIO.output(xpin, False)
                self.rightcount = self.rightcount - 1

                

            self.StepCounter += 1
            if self.StepCounter == self.StepCount:
                self.StepCounter = 0

            time.sleep(self.delay)

    def run(self, steps):
        try:
            for _ in range(steps):
                self.step(self.delay)
        except KeyboardInterrupt:
            pass
        finally:
            GPIO.cleanup()
    
    def __del__(self):
        GPIO.cleanup()

 