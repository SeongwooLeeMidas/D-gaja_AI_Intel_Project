import cv2
import pickle
import numpy as np
import struct  # 바이트 데이터 처리를 위한 모듈
import zlib    # 데이터 압축을 위한 모듈
import socket  # 네트워크 통신을 위한 모듈
import dadetect
import dadetect2_lsw


HOST = '192.168.5.156'        # 서버 IP 주소 (빈 문자열은 현재 호스트의 모든 네트워크 인터페이스를 의미)
PORT = 8485      # 사용할 포트 번호

# TCP 소켓 생성
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket created')

# 소켓에 IP 주소와 포트 번호를 바인드
s.bind((HOST, PORT))
print('Socket bind complete')

# 클라이언트의 연결 요청을 기다림
s.listen(10)
print('Socket now listening')

# 클라이언트로부터 연결 요청을 수락하고, 연결된 소켓과 클라이언트 주소를 리턴
conn, addr = s.accept()

data = b""  # 수신된 데이터를 저장할 버퍼
payload_size = struct.calcsize(">L")  # 데이터의 크기를 패킹하기 위한 바이트 수 계산
print("payload_size: {}".format(payload_size))

global key_ui, i ,compass 
compass = 180
i=0
def info_ui (frame):
    global key_ui,i
    if (i % 4 == 0) or(i % 5 == 0) or (i % 6 == 0)or(i % 7 == 0) :
            cv2.putText(frame, "--------", (110, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)
            cv2.putText(frame, "|            |", (110, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)
            cv2.putText(frame, "--------", (110, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)
    i = i+1
    if i == 8 : i = 0
    cv2.putText(frame, "DTS", (90, 70), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 153, 255), 2)
    cv2.putText(frame, "Press Key!", (120, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)
    cv2.putText(frame, "A : auto-mode, M: modify-degree,  Q: quit-program", (7, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 255, 255), 1)
    key = cv2.waitKey(1)
    if key == ord('q'):
        key_ui = 'q'
    elif key == ord('a'):
        key_ui = 'a'
    if key == ord('m'):
        key_ui = 'm'
    
def modify_degree(frame):
    global key_ui,compass
    cv2.putText(frame, "Modifying", (10, 12), cv2.FONT_HERSHEY_SIMPLEX, 0.38, (0, 255, 255), 1)
    cv2.putText(frame, "Q: quit, Space-bar : auto-detectmode", (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.38, (0, 255, 255), 1)
    direct = 's'
    key = cv2.waitKey(1)
    if key == ord('w'): #방향 설정 
        direct = 'w'
    elif key == ord('s'):
        direct = 'x'
    elif key == ord('a'):
        direct = 'a'
    elif key == ord('d'):
        direct = 'd'
    elif key == ord('q'): #인포 ui로 
        key_ui = 'i'
    elif key == ord(' '): #자동 디텍트모드 
        compass = 180
        key_ui = 'a'
    return frame, direct

key_ui ='i'

def cal_compass(direct):
    global compass
    if direct_key == 'q'or direct == 'a'or direct == 'z':
        compass = compass -2 
    elif direct == 'e'or direct == 'd'or direct == 'c':
        compass = compass+2
    return compass

while True:
    # 데이터의 크기를 수신할 때까지 반복하여 수신
    while len(data) < payload_size:
        #print("Recv: {}".format(len(data)))
        data += conn.recv(4096)

    #print("Done Recv: {}".format(len(data)))
    packed_msg_size = data[:payload_size]  # 패킹된 데이터의 크기만큼 버퍼에서 잘라냄
    data = data[payload_size:]             # 수신된 데이터에서 패킹된 데이터 크기만큼을 제외한 나머지 부분

    # 패킹된 데이터의 크기를 언패킹하여 메시지의 크기를 구함
    msg_size = struct.unpack(">L", packed_msg_size)[0]
    #print("msg_size: {}".format(msg_size))

    # 메시지의 크기만큼 데이터를 수신할 때까지 반복하여 수신
    while len(data) < msg_size:
        data += conn.recv(4096)

    # 메시지 데이터를 잘라내고 나머지 데이터를 다시 버퍼에 저장
    frame_data = data[:msg_size]
    data = data[msg_size:]

    # pickle을 사용하여 직렬화된 데이터를 원래의 형태로 변환
    frame = pickle.loads(frame_data, fix_imports=True, encoding="bytes")

    diret_key = 's'
    # OpenCV를 사용하여 이미지 데이터를 디코딩
    frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
    if key_ui == 'i':
        #info-UI
        info_ui(frame)
   
    elif key_ui == 'm':
        #수동 조절 
        frame, diret_key = modify_degree(frame)
    
    elif key_ui == 'a':
        #자동 디텍팅 
        frame,diret_key = dadetect.run_inference(frame)
        cv2.putText(frame,"Direct"+ str(compass), (1, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)
        print(diret_key)
    elif key_ui =='q':
        break
    #print(diret_key)
    # 디코딩된 이미지를 화면에 표시
    resized_frame = cv2.resize(frame, (640, 640))
    if diret_key == 'q'or diret_key == 'a'or diret_key == 'z':
        compass = compass -2 
    elif diret_key == 'e'or diret_key == 'd'or diret_key == 'c':
        compass = compass+2
 
    cv2.imshow('ImageWindow', resized_frame)

    conn.sendall(diret_key.encode())
    
    
   # 'q' 키를 누르면 프로그램 종료
    key = cv2.waitKey(1)
    if key == 27:
        break
    elif key == ord('q'):
        key_ui = 'i'


# 모든 창 닫기
cv2.destroyAllWindows()

# 연결된 소켓 종료
conn.close()

