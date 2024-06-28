import cv2
import sys
import numpy as np
import time 
from openvino.runtime import Core, Tensor

# 모델 경로 정의
model_xml = "model/model.xml"
model_bin = "model/model.bin"

# OpenVINO core 초기화
ie = Core()

# 모델 로드 및 네트워크 컴파일
try: 
    model = ie.read_model(model=model_xml, weights=model_bin)
    compiled_model = ie.compile_model(model=model, device_name="CPU")
except Exception as e:
    print(f"모델 로드 오류: {e}")
    exit(1)

# 고정된 입력 크기
input_height = 640
input_width = 640

# 추적기 초기화
trackers = []
tracker_colors = [(0, 255, 0), (255, 0, 0), (0, 0, 255), (255, 255, 0)]  # 각 드론에 대한 색상 정의
drone_id = 1

# 입력 프레임 전처리 함수 정의
def preprocess_frame(frame):
    resized_frame = cv2.resize(frame, (input_width, input_height))
    transposed_frame = np.transpose(resized_frame, (2, 0, 1))  # (H, W, C) to (C, H, W)
    input_data = np.expand_dims(transposed_frame, axis=0)  # (C, H, W) to (1, C, H, W)
    input_data = input_data.astype(np.float32)  # 모델이 float32 타입의 입력을 기대할 수 있으므로 변환
    return input_data

# 모델 출력 후처리 함수 정의
def postprocess_output(frame, boxes, labels, conf_threshold=0.75):
    global frame_height,frame_width
    frame_height, frame_width = frame.shape[:2]
    detections = []
    k='s'
    for box, label in zip(boxes, labels):
        x_min, y_min, x_max, y_max, confidence = box
        if confidence > conf_threshold:
            x_min = int(x_min * frame_width / 640)
            y_min = int(y_min * frame_height / 640)
            x_max = int(x_max * frame_width / 640)
            y_max = int(y_max * frame_height / 640)
            x_cent = int((x_min+x_max)/2)
            y_cent = int((y_min+y_max)/2)
            cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
            k = direct_cal(x_cent,y_cent,frame_width,frame_height)
            label = f"Drone: {confidence:.2f}"
            cv2.putText(frame, label, (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            #detections.append((x_min, y_min, x_max, y_max))
    return detections ,k

def direct_cal (x_cent,y_cent,width,height):
    up = down = left = right =0 
    if x_cent>((width/3)*2): right=1
    if x_cent<((width/3)*1): left=1
    if y_cent>((height/3)*2): down=1
    if y_cent<((height/3)*1): up=1
    print(up,down,left,right)
    k = 's'
    if left:
        if up:
            k='q'
        elif down:
            k='z'
        else:
            k='a'
    elif right:
        if up:
            k='e'
        elif down:
            k='c'
        else:
            k='d'
    else:
        if up:
            k='w'
        elif down:
            k='x'
        else:
            k='s'
    return k



# 메인 추론 함수 정의
def run_inference(frame):
    global frame_height,frame_width

    # 드론 검출
    input_data = preprocess_frame(frame)
    results = compiled_model([input_data])
    boxes = results[0][0]
    labels = results[1][0]


    detections,k = postprocess_output(frame, boxes, labels)
    for bbox in detections:
        x_min, y_min, x_max, y_max = bbox
        
        cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 255, 255), 2)
    return frame ,k