import cv2
import socket
import struct
import pickle
from Motor import Motor

# 소켓 생성 및 서버에 연결
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('192.168.5.15', 8485))

#모터 세팅 
StepPins = [8,9,10,11] # 스텝모터 핀설정 
ServoPins = 2  # 서보모터 핀 설정 
motor = Motor(ServoPins,StepPins) #모터 클래스 선언 

HOST = '192.168.5.15'        # 서버 IP 주소 (빈 문자열은 현재 호스트의 모든 네트워크 인터페이스를 의미)
PORT = 8485      # 사용할 포트 번호

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))


# 소켓을 이용한 파일 객체 생성 (이미지 데이터 전송을 위해 사용)
connection = client_socket.makefile('wb')

# 카메라 열기
cam = cv2.VideoCapture(-1)

# 카메라 해상도 설정
cam.set(3, 320)  # 너비
cam.set(4, 240)  # 높이

# 이미지 카운터 초기화
img_counter = 0

# JPEG 압축 파라미터 설정
encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

while True:
    # 카메라에서 프레임 읽기
    ret, frame = cam.read()
    
    # JPEG 포맷으로 프레임 인코딩
    result, frame = cv2.imencode('.jpg', frame, encode_param)
    
    # 프레임을 바이너리로 직렬화 (pickle 사용)
    data = pickle.dumps(frame, 0)
    
    # 직렬화된 데이터의 크기 계산
    size = len(data)

    # 직렬화된 데이터의 크기를 패킹하여 송신
    client_socket.sendall(struct.pack(">L", size) + data)
    
    data = client_socket.recv(4096)
    data = data.decode()
    if data != 's':
        print(data)
        motor.decode(data)
        data = 's'

    # 전송한 이미지의 정보 출력
    #print("{}: {}".format(img_counter, size))
    
    # 이미지 카운터 증가
    img_counter += 1

# 카메라 리소스 해제
cam.release()
