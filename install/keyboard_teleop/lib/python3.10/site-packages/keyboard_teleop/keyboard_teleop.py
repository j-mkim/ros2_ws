#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import sys, select, termios, tty

class keyboard_teleop(Node):
    def __init__(self):
        super().__init__('keyboard_teleop')
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        self.settings = termios.tcgetattr(sys.stdin)
        self.get_logger().info("Custom Teleop Node Initialized")

    def getKey(self):
        tty.setraw(sys.stdin.fileno())
        select.select([sys.stdin], [], [], 0)
        key = sys.stdin.read(1)
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.settings)
        return key

    def run(self):
        try:
            self.get_logger().info("Use WASD keys to control, Space or X to stop, Ctrl-C to exit.")
            while rclpy.ok():
                key = self.getKey()
                twist = Twist()
                if key == 'w':
                    twist.linear.x = 255.0  # forward
                elif key == 's':
                    twist.linear.x = -255.0  # backward
                elif key == 'a':
                    twist.angular.z = 300.0  # turn left
                elif key == 'd':
                    twist.angular.z = -300.0  # turn right
                elif key == ' ' or key == 'x':
                    twist.linear.x = 0.0
                    twist.angular.z = 0.0
                elif key == '\x03':  # Ctrl-C
                    break
                else:
                    # For any other key, do nothing.
                    continue

                self.publisher_.publish(twist)
                self.get_logger().info(f"Published: linear.x={twist.linear.x:.2f}, angular.z={twist.angular.z:.2f}")

        except Exception as e:
            self.get_logger().error(f"Error: {e}")
        finally:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.settings)
            rclpy.shutdown()

def main(args=None):
    rclpy.init(args=args)
    teleop_node = keyboard_teleop()
    teleop_node.run()
    teleop_node.destroy_node()

if __name__ == '__main__':
    main()
