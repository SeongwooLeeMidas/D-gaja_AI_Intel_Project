# DTS (Drone Tracking System)

군사용 Anti-Drone System은 존재하는데, 민간용은 존재하지 않아서 저렴한 Anti-Drone System 제작을 목표로 설정했다. 


드론에 피해를 입히면 범죄에 휘말릴 수 있기 때문에 카메라를 활용해 드론 객체를 추적하여 경찰에 알려주는 시스템을 개발하는 것이 목표이다.



## System Diagram
![image](https://github.com/kyoonw/D-gaja/assets/170689181/0f8e5abe-79e4-4a28-97df-f8174818dc20)


## Flow Chart
![image](https://github.com/kyoonw/D-gaja/assets/170689181/6b639baa-5e29-4ce0-a796-fad63a311a30)


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

## Steps to build

* pc가상환경을 통해 testbuild 후 board-depoly

```shell
cd ~/xxxx
source .venv/bin/activate

make
make install
```

## Steps to run

* pc가상환경을 통해 test build 후 board-depoly

```shell
cd ~/xxxx
source .venv/bin/activate

cd /path/to/repo/xxx/
python demo.py -i xxx -m yyy -d zzz
```

## Output

* (프로젝트 실행 화면 캡쳐)

![image](https://github.com/kyoonw/D-gaja/assets/170689181/afcd1fee-880e-4435-8ec4-a44f15ed67f1)

## Appendix

* (참고 자료 및 알아두어야할 사항들 기술)
