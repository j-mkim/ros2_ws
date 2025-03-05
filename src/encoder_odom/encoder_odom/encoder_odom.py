#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Quaternion, Twist
import math
import tf_transformations
import serial

class EncoderOdom(Node):
    def __init__(self):
        super().__init__('encoder_odom')
        try:
            self.ser = serial.Serial('/dev/ttyACM0', 115200, timeout=0.1)
            self.get_logger().info("Serial port opened successfully")
        except Exception as e:
            self.get_logger().error(f"Failed to open serial port: {e}")
            exit(1)
        
        # Create a timer to call read_serial periodically (every 10ms)
        self.create_timer(0.2, self.read_serial)
        
        # Subscription for teleop commands
        self.create_subscription(Twist, '/cmd_vel', self.cmd_vel_callback, 10)

        # Publisher for odometry
        self.odom_pub = self.create_publisher(Odometry, 'odom', 10)
        
        # Robot parameters (adjust these to your robot)
        self.wheel_radius = 0.03         # in meters
        self.wheel_separation = 0.15     # in meters (distance between wheels)
        self.ticks_per_rev = 576         # number of encoder ticks per wheel revolution
        
        # Scaling factor for converting velocity to PWM
        self.scaling_factor = 100  # adjust based on your motor/driver calibration

        # Pose state variables
        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0
        
        # For delta calculations
        self.prev_left_ticks = None
        self.prev_right_ticks = None
        self.prev_time = self.get_clock().now()

    def read_serial(self):
        try:
            line = self.ser.readline().decode('utf-8').strip()
        except Exception as e:
            self.get_logger().error(f"Serial read error: {e}")
            return

        if not line:
            return

        # Expecting a string like: "<tick1,tick2,tick3,tick4>"
        if line.startswith('<') and line.endswith('>'):
            try:
                parts = line[1:-1].split(',')
                if len(parts) != 4:
                    self.get_logger().warn("Received encoder data with incorrect format")
                    return
                # Convert parts to integers
                ticks = [int(x) for x in parts]
                # Compute average ticks for left and right sides (first two: left, next two: right)
                left_ticks = (ticks[0] + ticks[1]) / 2.0
                right_ticks = (ticks[2] + ticks[3]) / 2.0
                # Update odometry based on the received encoder ticks
                self.compute_odometry(left_ticks, right_ticks)
            except ValueError:
                self.get_logger().warn("Failed to parse encoder ticks")

    def compute_odometry(self, left_ticks, right_ticks):
        current_time = self.get_clock().now()
        dt = (current_time - self.prev_time).nanoseconds * 1e-9
        self.prev_time = current_time
        
        # On the first reading, just store the ticks.
        if self.prev_left_ticks is None or self.prev_right_ticks is None:
            self.prev_left_ticks = left_ticks
            self.prev_right_ticks = right_ticks
            return
        
        # Compute change in ticks
        delta_left = left_ticks - self.prev_left_ticks
        delta_right = right_ticks - self.prev_right_ticks
        
        self.prev_left_ticks = left_ticks
        self.prev_right_ticks = right_ticks
        
        # Convert tick differences to distance traveled by each wheel
        d_left = (2 * math.pi * self.wheel_radius * delta_left) / self.ticks_per_rev
        d_right = (2 * math.pi * self.wheel_radius * delta_right) / self.ticks_per_rev
        
        # Differential drive kinematics
        d_center = (d_left + d_right) / 2.0
        d_theta = (d_right - d_left) / self.wheel_separation
        
        # Update robot's pose
        self.x += d_center * math.cos(self.theta + d_theta / 2.0)
        self.y += d_center * math.sin(self.theta + d_theta / 2.0)
        self.theta += d_theta
        
        # Create and publish the odometry message
        odom_msg = Odometry()
        odom_msg.header.stamp = current_time.to_msg()
        odom_msg.header.frame_id = "odom"
        odom_msg.child_frame_id = "base_link"
        
        odom_msg.pose.pose.position.x = self.x
        odom_msg.pose.pose.position.y = self.y
        odom_msg.pose.pose.position.z = 0.0
        
        quat = tf_transformations.quaternion_from_euler(0, 0, self.theta)
        odom_msg.pose.pose.orientation = Quaternion(
            x=quat[0], y=quat[1], z=quat[2], w=quat[3]
        )
        
        if dt > 0:
            vx = d_center / dt
            vth = d_theta / dt
        else:
            vx = 0.0
            vth = 0.0
        
        odom_msg.twist.twist.linear.x = vx
        odom_msg.twist.twist.angular.z = vth
        
        self.odom_pub.publish(odom_msg)
        self.get_logger().info(
            f"Odom published: x={self.x:.2f}, y={self.y:.2f}, theta={self.theta:.2f}"
        )

    def cmd_vel_callback(self, msg: Twist):
        # Differential drive conversion:
        # left_velocity = v - (wheel_separation/2)*w
        # right_velocity = v + (wheel_separation/2)*w
        v = msg.linear.x      # m/s
        w = msg.angular.z     # rad/s
        
        left_velocity  = v - (self.wheel_separation / 2.0) * w
        right_velocity = v + (self.wheel_separation / 2.0) * w
        
        # Convert velocities to PWM values using scaling factor
        left_pwm = int(max(min(left_velocity * self.scaling_factor, 255), -255))
        right_pwm = int(max(min(right_velocity * self.scaling_factor, 255), -255))
        
        # Construct command string for four motors:
        # Assuming motors 2 and 4 are left and motors 1 and 3 are right.
        command_str = f"({right_pwm}, {left_pwm}, {right_pwm}, {left_pwm})\n"
        try:
            self.ser.write(command_str.encode('utf-8'))
            self.get_logger().info(f"Sent motor command: {command_str.strip()}")
        except Exception as e:
            self.get_logger().error(f"Error sending command: {e}")


def main(args=None):
    rclpy.init(args=args)
    node = EncoderOdom()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
