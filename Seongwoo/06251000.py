import cv2
import sys
import numpy as np
import time
from openvino.runtime import Core, Tensor
#from openvino.runtime import AsyncInferQueue, Core, InferRequest, Layout, Type
#from openvino.preprocess import PrePostProcessor, ResizeAlgorithm
#from argparse import SUPPRESS, ArgumentParser
#from pathlib import Path

# 중복된 데이터 처리 제거: 현재 코드에서는 두 번의 프레임 전처리를 수행하고 있습니다. 이를 줄입니다.
# 병렬 처리를 통한 비동기 추론 최적화: 추론 요청을 좀 더 효율적으로 전환합니다.
# 불필요한 예외 처리 및 구조 간소화: 필요하지 않은 예외 처리를 제거하고 구조를 단순화합니다.

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

input_layer_drone = model.input(0)
output_layer_drone = model.output(0)

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
            x_min = int(x_min * frame_width / 256)
            y_min = int(y_min * frame_height / 256)
            x_max = int(x_max * frame_width / 256)
            y_max = int(y_max * frame_height / 256)
            cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
            label = f"Drone: {confidence:.2f}"
            cv2.putText(frame, label, (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

# 비동기 추론 함수 정의
def async_api(source=0, use_popup=True):
    frame_number = 0
    curr_request = compiled_model.create_infer_request()
    next_request = compiled_model.create_infer_request()
    async_fps = 0

    try:
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("웹캠을 읽는 데 오류가 발생했습니다.")
            return 

        start_time = time.time()
        if use_popup:
            title = "Press ESC to Exit"
            cv2.namedWindow(title, cv2.WINDOW_GUI_NORMAL | cv2.WINDOW_AUTOSIZE)

        ret, frame = cap.read()
        if not ret:
            print("웹캠을 읽는 데 실패했습니다.")
            return

        curr_request.start_async()
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print("웹캠 스트림이 종료되었습니다.")
                continue
            
            resized_frame = preprocess_frame(frame)
            next_request.set_tensor(input_layer_drone, Tensor(resized_frame))
            next_request.start_async()
            curr_request.wait()
            res = curr_request.get_output_tensor(0).data

            stop_time = time.time()
            total_time = stop_time - start_time
            frame_number = frame_number + 1
            async_fps = frame_number / total_time
            # postprocess_output(frame, res, conf_threshold=0.5)
            curr_request, next_request = next_request, curr_request
            
            input_data = preprocess_frame(frame)
            results = compiled_model([input_data])
            boxes = results[0][0]
            labels = results[1][0]
            try:
                postprocess_output(frame, boxes, labels)
            except:
                continue

            # 결과 보기
            #if use_popup:
            cv2.imshow(title, frame)
            key = cv2.waitKey(1)
            if key == 27:
                break


    except KeyboardInterrupt:
        print("중단됨")
    except RuntimeError as e:
        print (e)

    finally:
        if use_popup:
            cv2.destroyAllWindows()
        if cap is not None:
            cap.release()
        return async_fps

if __name__ == "__main__":
    async_fps = async_api(source=0)
    print(f"Async FPS: {async_fps}")
    sys.exit(0)


