import cv2
import sys
import numpy as np
import time 
from openvino.runtime import Core, Tensor

# 모델 경로 정의
model_xml = "/home/ubuntu/workspace1/otx_detection/outputs/D-gaja/Chanuks/deploy0625/model/model.xml"
model_bin = "/home/ubuntu/workspace1/otx_detection/outputs/D-gaja/Chanuks/deploy0625/model/model.bin"

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
input_height = 256
input_width = 256

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
def postprocess_output(frame, boxes, labels, conf_threshold=0.5):
    frame_height, frame_width = frame.shape[:2]
    detections = []
    for box, label in zip(boxes, labels):
        x_min, y_min, x_max, y_max, confidence = box
        if confidence > conf_threshold:
            x_min = int(x_min * frame_width / 256)
            y_min = int(y_min * frame_height / 256)
            x_max = int(x_max * frame_width / 256)
            y_max = int(y_max * frame_height / 256)
            cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
            label = f"Drone: {confidence:.2f}"
            cv2.putText(frame, label, (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            #detections.append((x_min, y_min, x_max, y_max))
    return detections

# 메인 추론 함수 정의
def run_inference():
    global drone_id # 전역 변수를 함수 내에서 수정 가능

    try:
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("웹캠을 켜는데 오류가 발생했습니다.")
            return

        ret, frame = cap.read()
        if not ret:
            print("웹캠을 켜는데 실패했습니다.")
            exit(1)

        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        start_time = time.time()
        frame_number = 0

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print("웹캠이 종료되었습니다.")
                continue
            
            if len(trackers) < len(tracker_colors): # 원하는 드론 개수만큼 추적기 추가
                # 드론 검출
                input_data = preprocess_frame(frame)
                results = compiled_model([input_data])
                boxes = results[0][0]
                labels = results[1][0]

                try:
                    detections = postprocess_output(frame, boxes, labels)
                    for bbox in detections:
                        x_min, y_min, x_max, y_max = bbox
                        cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)

                except:
                    continue
            else:
                # 드론 추적
                new_trackers = []
                for id, tracker, color in trackers:
                    ok, bbox = tracker.update(frame)
                    if ok: # 추적 성공
                        (x, y, w, h) = map(int,bbox)
                        cv2.rectangle(frame, (x,y), (x + w, y + h), color, 2)
                        cv2.putText(frame, f"Drone {id}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)
                        new_trackers.append((tracker, color, id))
                    else: # 추적 실패, 드론 재검출
                        print(f"드론 {id}번 추적 실패")
                trackers[:] = new_trackers # 추적 성공한 tracker만 유지

            # 프레임 수 계산
            frame_number +=1
        
            cv2.imshow('frame', frame)

            key = cv2.waitKey(1)
            if key == 27:
                break

    except KeyboardInterrupt:
        print("중단됨")
    except RuntimeError as e:
        print (e)

    cap.release()
    cv2.destroyAllWindows()

    # FPS 계산 및 출력
    stop_time = time.time()
    total_time = stop_time - start_time
    fps = frame_number / total_time
    print(f"FPS: {fps:.2f}")
    return fps

if __name__ == "__main__":
    fps = run_inference()
    sys.exit(0)