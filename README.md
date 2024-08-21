# DTS (Drone Tracking System)

군사용 Anti-Drone System은 존재하는데, 민간용은 존재하지 않아서 저렴한 Anti-Drone System 제작을 목표로 설정했다. 


[Intel] Edge AI SW 아카데미 4기에서 진행한 팀 프로젝트로, 웹캠으로 드론에 대한 입력을 받아 객체 인식 알고리즘을 사용하여 드론을 감지하고, 이를 기반으로 드론을 추적하는 알고리즘을 실행하여 모터를 제어해 카메라를 회전시킨다. 


실시간 영상 데이터를 소켓 통신을 통해 전송 및 수신하며, 드론을 감지하고 추적하기 위해 무선 통신을 사용한다. 다른 객체가 감지되면 사용자에게 알림을 보낸다.


## System Diagram
![image](https://github.com/kyoonw/D-gaja/assets/170689181/0f8e5abe-79e4-4a28-97df-f8174818dc20)


## Flow Chart
![image](https://github.com/kyoonw/D-gaja/assets/170689181/a07804d7-750b-40c4-a8f1-22bb975f5341)


## Circuit Diagram
![image](https://github.com/kyoonw/D-gaja/assets/170689181/02a2f16f-0451-436e-970c-399432458d4d)


## ProJect Schedule
![image](https://github.com/kyoonw/D-gaja/assets/170689181/249d19c5-d74f-4213-bc66-d2c0765f6dba)


## 개발 환경
- Python 3.11


- Raspberry Pi


- Camera - Logitech(VU0040)


- Servo Motor, Stepper Motor


- OpenVINO(Object-Detection), Training - OTX


- Ubuntu 22.04.4 LTS (64Bit)

## 개발 인원
4명

## 수행 목표
1) 웹캠으로 드론을 탐지하고 좌표값을 계산해 서버로 전송
2) TCP/IP 소켓 통신을 통해 보드에서 Motor 제어로 Webcam을 회전
3) 객체 인식 및 추적하는 알고리즘을 제작해 드론을 실시간으로 탐지
4) 시스템 안정성 및 성능 모니터링을 통해 최적화 수행

## 담당 역할 및 수행 결과
- 경량화된 MobilenetV2 모델 대신 성능이 우수한 YOLO-X 모델로 변경 후 Accuracy를 0.57에서 0.89로 향상


- Rasberry Pi 보드 성능을 개선하기 위해 모델의 부동 소수점 표현, Input Size, Async를 사용해 FPS 10.7%, CPU 사용량 15.4% 개선


- 사용하려던 Deepsort는 Otx의 데이터 포맷과 처리 방식이 달라 통합이 복잡해 OpenCV 추적기로 변경하여 코드 통합 진행, 가장 성능이 좋은 TrackerCSRT를 사용


- 팀장으로서 프로젝트를 총괄하며, Spreadsheets를 활용해 매일 오전 10시에 진행 상황과 오늘의 목표 팀원들과 공유

## Clone code

* github를 통한 코드 공유 

```shell
git clone https://github.com/kyoonw/D-gaja.git
```

## Prerequite

* requirements.txt를 통해 파이썬 환경설치

```shell
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Steps to run

*PC서버 작동

```shell
cd ~/main
python3 server.py
```
*보드내에서 작동 
```shell
cd ~/main
python3 board.py
```

## Output
* 제품 외관
![image (1)](https://github.com/kyoonw/D-gaja/assets/88040637/836c15e8-a656-4366-807f-c4fff6e9aca8)

* 제품 작동 
![image](https://github.com/kyoonw/D-gaja/assets/170689181/afcd1fee-880e-4435-8ec4-a44f15ed67f1)

## Appendix

[프로젝트 정리 - 노션](https://www.notion.so/DTS-89037e36d4894b45a5a09e315e251974?pvs=4)
[시연 영상](https://youtu.be/B-WaSipJL4Q)
