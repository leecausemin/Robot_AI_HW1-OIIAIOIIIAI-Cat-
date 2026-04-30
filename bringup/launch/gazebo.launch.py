from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, SetEnvironmentVariable, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, EnvironmentVariable, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    model = PathJoinSubstitution(
        [FindPackageShare("description"), "urdf", "robot.urdf.xacro"]
    )
    world = PathJoinSubstitution([FindPackageShare("bringup"), "worlds", "empty.world"])
    gazebo_launch = PathJoinSubstitution([FindPackageShare("gazebo_ros"), "launch", "gazebo.launch.py"])

    robot_description = {"robot_description": Command(["xacro ", model, " use_ros2_control:=true"])}

    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[robot_description],
        output="screen",
    )

    spawn_robot = Node(
        package="gazebo_ros",
        executable="spawn_entity.py",
        arguments=[
            "-topic", "robot_description",
            "-entity", "robot",
            "-z", "0.0",
            "-timeout", "120",
        ],
        output="screen",
    )

    joint_state_broadcaster = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_state_broadcaster"],
        output="screen",
    )

    cat_posture_controller = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["cat_posture_controller"],
        output="screen",
    )

    motion_manager = Node(
        package="control",
        executable="motion_manager",
        output="screen",
    )

    return LaunchDescription(
        [
            SetEnvironmentVariable("LIBGL_ALWAYS_SOFTWARE", "1"),
            SetEnvironmentVariable("QT_X11_NO_MITSHM", "1"),
            SetEnvironmentVariable(
                "GAZEBO_RESOURCE_PATH",
                [
                    FindPackageShare("description"),
                    ":",
                    EnvironmentVariable("GAZEBO_RESOURCE_PATH", default_value=""),
                ],
            ),
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(gazebo_launch),
                launch_arguments={"world": world, "verbose": "ture"}.items(),
            ),
            robot_state_publisher,
            TimerAction(period=2.0, actions=[spawn_robot]),
            TimerAction(period=5.0, actions=[joint_state_broadcaster]),
            TimerAction(period=6.0, actions=[cat_posture_controller]),
            TimerAction(period=7.0, actions=[motion_manager]),
        ]
    )
