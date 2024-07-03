from stepmotor import StepperMotor
from Motor import Motor
import cv2

webcam = cv2.VideoCapture(-1)
#모터 세팅 
StepPins = [8,9,10,11] # 스텝모터 핀설정 
ServoPins = 12  # 서보모터 핀 설정 
motor = Motor(ServoPins,StepPins) #모터 클래스 선언 

global up,down,left,right

#모터 구동 추론 
def direct_cal (x_cent,y_cent,width,height):
    global up,down,left,right
    if x_cent>((width/3)*2): right=1
    if x_cent<((width/3)*1): left=1
    if y_cent>((height/3)*2): down=1
    if y_cent<((height/3)*1): up=1

a=k=1

if not webcam.isOpened():
    print("Could not open webcam")
    exit()
toggle = 0 
while webcam.isOpened():
    status, frame = webcam.read()
    frame_height, frame_width = frame.shape[:2]
    up = 0
    down = 0
    left = 0
    right = 0
    if status:
        cv2.imshow("test", frame)
    '''
    if a>180:
        a=1
    if k > frame_height:
        k=1
    direct_cal (a,k,frame_width,frame_height)
    a = a*10
    k= k*10
    '''
    key = cv2.waitKey(1)
    if key == ord('q'):
        break    
    elif key == ord('a'):
        left = 1
    elif key == ord('d'):
        right = 1
    elif key == ord('w'):
        up = 1
    elif key == ord('s'):
        down = 1
    motor.input(up,down,left,right)

webcam.release()
cv2.destroyAllWindows()
