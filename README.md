# Robot_AI_HW1-OIIAIOIIIAI-Cat-
이 프로젝트는 로봇AI의 첫번째 과제입니다.
OIIAIOIIIAI-Cat(Spining Cat)에 영감을 받아 이 과제를 진행했습니다.
고양이의 모델링은 친구네 고양이를 모티브로 제작했습니다.



<img width="800" height="450" alt="Image" src="https://github.com/user-attachments/assets/d933d302-f6b4-41c0-b129-75c6678f209a" />


시작 순서
### 0. 사전 준비
$ colcon build --symlink-install
$ source install/setup.bash

### 1. 로봇 시뮬레이션(Gazebo)
$ ros2 launch bringup gazebo.launch.py
### 2. 로봇 동작 프로그래밍
- 춤추게 하기
$ ros2 service call /stand_up std_srvs/srv/SetBool "{data: false}"
- 춤 멈추게 하게
$ ros2 service call /stand_up std_srvs/srv/SetBool "{data: true}"
