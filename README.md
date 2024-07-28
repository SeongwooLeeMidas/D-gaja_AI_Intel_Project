# DTS (Drone Tracking System)

군사용 Anti-Drone System은 존재하는데, 민간용은 존재하지 않아서 저렴한 Anti-Drone System 제작을 목표로 설정했다. 


웹캠으로 드론에 대한 입력을 받아 객체 인식 알고리즘을 사용하여 드론을 감지하고, 이를 기반으로 드론을 추적하는 알고리즘을 실행하여 모터를 제어해 카메라를 회전시킨다. 


실시간 영상 데이터를 소켓 통신을 통해 전송 및 수신하며, 드론을 감지하고 추적하기 위해 무선 통신을 사용한다. 다른 객체가 감지되면 사용자에게 알림을 보낸다.


## System Diagram
![image](https://github.com/kyoonw/D-gaja/assets/170689181/0f8e5abe-79e4-4a28-97df-f8174818dc20)


## Flow Chart
![image](https://github.com/kyoonw/D-gaja/assets/170689181/a07804d7-750b-40c4-a8f1-22bb975f5341)


## Circuit Diagram
![image](https://github.com/kyoonw/D-gaja/assets/170689181/02a2f16f-0451-436e-970c-399432458d4d)


## ProJect Schedule
![image](https://github.com/kyoonw/D-gaja/assets/170689181/249d19c5-d74f-4213-bc66-d2c0765f6dba)


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

* [(참고 자료 및 알아두어야할 사항들 기술)](https://github.com/kyoonw/D-gaja)
