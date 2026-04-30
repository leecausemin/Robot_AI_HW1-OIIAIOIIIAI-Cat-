# Robot_AI_HW1-OIIAIOIIIAI-Cat-
이 프로젝트는 로봇AI의 첫번째 과제입니다.
OIIAIOIIIAI-Cat(Spining Cat)에 영감을 받아 이 과제를 진행했습니다.
고양이의 모델링은 친구네 고양이를 모티브로 제작했습니다.

<p align="center">
  <a href="link">
    <img src="https://github.com/user-attachments/assets/e73712dd-eb85-4710-9e8a-820dd7249f87" width="30%">
  </a>
  <a href="link">
    <img src="https://github.com/user-attachments/assets/4d4d765b-b726-4075-a637-3d4405c451f1" width="30%">
  </a>
  <a href="link">
    <img src="https://github.com/user-attachments/assets/73fdaf66-7df6-4c25-93c3-04432b26fd52" width="30%">
  </a>
</p>

## 모델링
<p align="center">
  <img src="https://github.com/user-attachments/assets/f0ccfa29-94c3-438a-8146-2ecb0000b2cc" width="296">
  <img src="https://github.com/user-attachments/assets/804e4525-d5c5-4e3c-82c2-f29771a058ab" width="296">
</p>

<p align="center">
  좌: RViz2 | 우: Gazebo
</p>

## 비교
<p align="center">
  <img src="https://github.com/user-attachments/assets/2bfc99e2-95aa-4657-8991-4741ab8380a3" width="49%">
  <img src="https://github.com/user-attachments/assets/d933d302-f6b4-41c0-b129-75c6678f209a" width="49%">
</p>

## 시작 순서
### 0. 사전 준비
```bash
mkdir -p ~/hw_yumin_ws/src
cd ~/hw_yumin_ws/src
git clone https://github.com/leecausemin/Robot_AI_HW1-OIIAIOIIIAI-Cat-.git
cd ~/hw_yumin_ws
colcon build --symlink-install
source install/setup.bash
```

### 1. 로봇 모델 가시화(RViz2)
```bash
ros2 launch bringup display.launch.py
```

### 2. 로봇 시뮬레이션(Gazebo)
```bash
ros2 launch bringup gazebo.launch.py
```

### 3. 로봇 동작 프로그래밍
- 춤추게 하기:
```bash
ros2 service call /stand_up std_srvs/srv/SetBool "{data: false}"
```
- 춤 멈추게 하게:
```bash
ros2 service call /stand_up std_srvs/srv/SetBool "{data: true}"
```
