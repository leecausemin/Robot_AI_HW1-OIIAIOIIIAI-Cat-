import rclpy
from geometry_msgs.msg import Twist
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.executors import MultiThreadedExecutor
from rclpy.node import Node
from std_msgs.msg import Float64MultiArray
from std_srvs.srv import SetBool


class MotionManager(Node):
    """Starts loaf spin and handles the stand-up signal."""

    def __init__(self):
        super().__init__("motion_manager")
        self.declare_parameter("cmd_vel_topic", "/diff_drive_controller/cmd_vel_unstamped")
        self.declare_parameter("posture_topic", "/cat_posture_controller/commands")
        self.declare_parameter("spin_angular_speed", 20.0)
        self.declare_parameter("fold_to_spin_delay", 1.5)

        self.callback_group = ReentrantCallbackGroup()
        topic = self.get_parameter("cmd_vel_topic").value
        posture_topic = self.get_parameter("posture_topic").value

        self.cmd_vel_publisher = self.create_publisher(Twist, topic, 10)
        self.posture_publisher = self.create_publisher(Float64MultiArray, posture_topic, 10)
        self.loaf_spin = False
        self._spin_arm_timer = None

        self.create_service(
            SetBool,
            "loaf_spin",
            self.handle_loaf_spin,
            callback_group=self.callback_group,
        )
        self.create_service(
            SetBool,
            "stand_up",
            self.handle_stand_up,
            callback_group=self.callback_group,
        )

        self._startup_timer = self.create_timer(2.0, self.start_stand_pose)
        self._spin_timer = self.create_timer(0.02, self.publish_spin)
        self.get_logger().info(
            f"Motion manager ready. Command topic: {topic}, posture topic: {posture_topic}"
        )

    def start_stand_pose(self):
        self.publish_stand_posture()
        self.loaf_spin = False
        self._startup_timer.cancel()
        self.get_logger().info("Initial stand posture published; 4 legs on the ground")

    def handle_loaf_spin(self, request, response):
        if request.data:
            self.loaf_spin = False
            self.stop_robot()
            self.publish_loaf_posture()
            self._arm_spin_after_fold()
            delay = self.get_parameter("fold_to_spin_delay").value
            response.message = f"folding legs; spin will start in {delay:.1f}s"
        else:
            self.loaf_spin = False
            self._cancel_spin_arm()
            self.stop_robot()
            response.message = "loaf_spin stopped"
        response.success = True
        self.get_logger().info(response.message)
        return response

    def handle_stand_up(self, request, response):
        if request.data:
            self.loaf_spin = False
            self._cancel_spin_arm()
            self.stop_robot()
            self.publish_stand_posture()
            response.message = "stand_up signal accepted; standing posture requested"
        else:
            self.stop_robot()
            self.publish_loaf_posture()
            self._arm_spin_after_fold()
            response.message = "stand_up disabled; folding legs and resuming spin"
        response.success = True
        self.get_logger().info(response.message)
        return response

    def _arm_spin_after_fold(self):
        self._cancel_spin_arm()
        delay = float(self.get_parameter("fold_to_spin_delay").value)
        self._spin_arm_timer = self.create_timer(delay, self._engage_spin)

    def _engage_spin(self):
        self._cancel_spin_arm()
        self.loaf_spin = True
        self.get_logger().info("legs folded; spin engaged")

    def _cancel_spin_arm(self):
        if self._spin_arm_timer is not None:
            self._spin_arm_timer.cancel()
            self.destroy_timer(self._spin_arm_timer)
            self._spin_arm_timer = None

    def publish_spin(self):
        if not self.loaf_spin:
            return
        msg = Twist()
        msg.angular.z = float(self.get_parameter("spin_angular_speed").value)
        self.cmd_vel_publisher.publish(msg)

    def stop_robot(self):
        self.cmd_vel_publisher.publish(Twist())

    def publish_stand_posture(self):
        self.publish_posture([0.0, 0.0, 0.0, 0.0, 0.0])

    def publish_loaf_posture(self):
        self.publish_posture([-0.12, 1.57, 1.57, -1.57, -1.57])

    def publish_posture(self, joint_positions):
        msg = Float64MultiArray()
        msg.data = [float(position) for position in joint_positions]
        self.posture_publisher.publish(msg)


def main():
    rclpy.init()
    node = MotionManager()
    executor = MultiThreadedExecutor()
    executor.add_node(node)
    try:
        executor.spin()
    except KeyboardInterrupt:
        pass
    finally:
        node.stop_robot()
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
