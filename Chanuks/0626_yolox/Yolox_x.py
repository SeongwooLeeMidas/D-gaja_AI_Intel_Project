import cv2
import numpy as np
import time
from openvino.runtime import Core

def preprocess_frame(frame, input_size):
    resized_frame = cv2.resize(frame, input_size)
    transposed_frame = resized_frame.transpose(2, 0, 1)  # (H, W, C) to (C, H, W)
    input_data = np.expand_dims(transposed_frame, axis=0).astype(np.float32)  # (C, H, W) to (1, C, H, W)
    return input_data

def draw_boxes(image, boxes, confidences, conf_threshold=0.5):
    for i in range(len(boxes)):
        if confidences[i] > conf_threshold:
            x_min, y_min, x_max, y_max = map(int, boxes[i])  # 좌표를 정수로 변환
            confidence = confidences[i]
            label = f"Confidence: {confidence:.2f}"
            color = (0, 255, 0)
            cv2.rectangle(image, (x_min, y_min), (x_max, y_max), color, 2)
            cv2.putText(image, label, (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

# 모델과 가중치 파일 경로
model_xml = "/home/ubuntu/workdir/test_0626/deploy/model/model.xml"
model_bin = "/home/ubuntu/workdir/test_0626/deploy/model/model.bin"

# OpenVINO Inference Engine 초기화
ie = Core()

# 모델 로드 및 컴파일
model = ie.read_model(model=model_xml, weights=model_bin)
compiled_model = ie.compile_model(model=model, device_name="AUTO")

# 입력 및 출력 정보 가져오기
input_layer = compiled_model.inputs[0]
output_layer = compiled_model.outputs[0]

# 비디오 캡처 초기화
cap = cv2.VideoCapture(0)

# 입력 크기
input_size = (640, 640)
frame_number = 0
start_time = time.time()

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        print("비디오 프레임이 비어 있거나 비디오 처리가 완료되었습니다.")
        break

    original_height, original_width = frame.shape[:2]
    input_data = preprocess_frame(frame, input_size)
    
    result = compiled_model([input_data])[output_layer]

    # 결과 해석 (박스 좌표 및 신뢰도)
    boxes = []
    confidences = []
    for detection in result[0]:
        x_min, y_min, x_max, y_max, confidence = detection[:5]
        if confidence > 0.8:  # 신뢰도가 0.8보다 큰 경우만 고려
            x_min = int(x_min * original_width / input_size[0])
            y_min = int(y_min * original_height / input_size[1])
            x_max = int(x_max * original_width / input_size[0])
            y_max = int(y_max * original_height / input_size[1])
            boxes.append([x_min, y_min, x_max, y_max])
            confidences.append(float(confidence))

    # 박스 그리기
    draw_boxes(frame, boxes, confidences)

    # FPS 계산 및 출력
    frame_number += 1
    if frame_number % 30 == 0:  # 매 30프레임마다 FPS 업데이트
        end_time = time.time()
        fps = 30 / (end_time - start_time)
        start_time = end_time
        print(f"FPS: {fps:.2f}")

    # 결과 이미지 표시
    cv2.imshow("Detection Results", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
