from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import Command, LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    use_gui = LaunchConfiguration("use_gui")
    model = PathJoinSubstitution(
        [FindPackageShare("description"), "urdf", "robot.urdf.xacro"]
    )
    rviz_config = PathJoinSubstitution(
        [FindPackageShare("description"), "rviz", "robot.rviz"]
    )

    robot_description = {"robot_description": Command(["xacro ", model, " use_ros2_control:=false"])}

    return LaunchDescription(
        [
            DeclareLaunchArgument("use_gui", default_value="true"),
            Node(
                package="robot_state_publisher",
                executable="robot_state_publisher",
                parameters=[robot_description],
                output="screen",
            ),
            Node(
                package="joint_state_publisher_gui",
                executable="joint_state_publisher_gui",
                parameters=[{"use_gui": use_gui}],
            ),
            Node(
                package="rviz2",
                executable="rviz2",
                arguments=["-d", rviz_config],
                output="screen",
            ),
        ]
    )
