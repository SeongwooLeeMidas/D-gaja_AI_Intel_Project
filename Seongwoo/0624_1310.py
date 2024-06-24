import cv2
import os
import sys
import numpy as np
import time 
import threading
from openvino.runtime import AsyncInferQueue, Core, InferRequest, Layout, Type
#from openvino.runtime import IECore
from openvino.preprocess import PrePostProcessor, ResizeAlgorithm
from argparse import SUPPRESS, ArgumentParser
from pathlib import Path

# 모델 경로 정의
model_xml = "/home/ubuntu/workspace1/otx_detection/outputs/D-gaja/Chanuks/deploy1/model/model.xml"
model_bin = "/home/ubuntu/workspace1/otx_detection/outputs/D-gaja/Chanuks/deploy1/model/model.bin"

# OpenVINO core 초기화
ie = Core()

# 모델 로드 및 네트워크 컴파일
try:
    model = ie.read_model(model=model_xml, weights=model_bin)
    compiled_model = ie.compile_model(model=model, device_name="CPU")
except Exception as e:
    print(f"모델 로드 오류: {e}")
    exit(1)

input_layer = compiled_model.input(0)
output_layer = compiled_model.output(0)

# 고정된 입력 크기
input_height = 384
input_width = 384

# 입력 프레임 전처리 함수 정의
def preprocess_frame(frame):
    resized_frame = cv2.resize(frame, (input_width, input_height))
    transposed_frame = np.transpose(resized_frame, (2, 0, 1))  # (H, W, C) to (C, H, W)
    input_data = np.expand_dims(transposed_frame, axis=0)  # (C, H, W) to (1, C, H, W)
    input_data = input_data.astype(np.float32)  # 모델이 float32 타입의 입력을 기대할 수 있으므로 변환
    return input_data

# 모델 출력 후처리 함수 정의
def postprocess_output(frame, boxes, labels, conf_threshold=0.5):
    frame_height, frame_width = frame.shape[:2]
    for box, label in zip(boxes, labels):
        x_min, y_min, x_max, y_max, confidence = box
        if confidence > conf_threshold:
            x_min = int(x_min * frame_width / 384)
            y_min = int(y_min * frame_height / 384)
            x_max = int(x_max * frame_width / 384)
            y_max = int(y_max * frame_height / 384)
            cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
            label = f"Drone: {confidence:.2f}"
            cv2.putText(frame, label, (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

# 메인 추론 함수 정의
def run_inference():
    try:
        cap = cv2.VideoCapture(0)
        assert cap.isOpened(), "비디오 파일을 읽는 데 오류가 발생했습니다."

        ret, frame = cap.read()
        if not ret:
            print("비디오 파일을 읽는 데 실패했습니다.")
            exit(1)

        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                print("비디오 프레임이 비어 있거나 비디오 처리가 완료되었습니다.")
                break

            input_data = preprocess_frame(frame)
                        
            results = compiled_model([input_data])
            boxes = results[0][0]
            labels = results[1][0]
           
            postprocess_output(frame, boxes, labels)

            cv2.imshow('Frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except KeyboardInterrupt:
        print("중단됨")

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    run_inference()
    sys.exit(0)

