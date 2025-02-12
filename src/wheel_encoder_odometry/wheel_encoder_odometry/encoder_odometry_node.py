#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
import serial
import math
from sensor_msgs.msg import JointState
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist, Quaternion
from std_msgs.msg import Header
from tf_transformations import euler_from_quaternion, quaternion_from_euler

class EncoderOdometryNode(Node):
    def __init__(self):
        super().__init__('encoder_odometry_node')

        # Parameters
        self.declare_parameter('serial_port', '/dev/ttyACM0')
        self.declare_parameter('baud_rate', 115200)
        self.declare_parameter('wheel_radius', 0.05)  # meters
        self.declare_parameter('wheel_base', 0.3)     # meters
        self.declare_parameter('wheel_track', 0.4)    # meters
        self.declare_parameter('encoder_resolution', 4096)

        # Get parameters
        serial_port = self.get_parameter('serial_port').get_parameter_value().string_value
        baud_rate = self.get_parameter('baud_rate').get_parameter_value().integer_value
        self.wheel_radius = self.get_parameter('wheel_radius').get_parameter_value().double_value
        self.wheel_base = self.get_parameter('wheel_base').get_parameter_value().double_value
        self.wheel_track = self.get_parameter('wheel_track').get_parameter_value().double_value
        self.encoder_resolution = self.get_parameter('encoder_resolution').get_parameter_value().integer_value

        # Open serial port
        try:
            self.serial_port = serial.Serial(serial_port, baud_rate, timeout=1)
            self.get_logger().info(f'Opened serial port {serial_port} at {baud_rate} baud.')
        except serial.SerialException as e:
            self.get_logger().error(f'Failed to open serial port: {e}')
            self.destroy_node()
            rclpy.shutdown()
            return

        # Publishers
        self.encoder_pub = self.create_publisher(JointState, 'encoder_counts', 10)
        self.odom_pub = self.create_publisher(Odometry, 'odom', 10)

        # Subscribers
        self.cmd_vel_sub = self.create_subscription(Twist, 'cmd_vel', self.cmd_vel_callback, 10)

        # Timer to read from serial at 50 Hz
        self.create_timer(0.02, self.read_serial_data)

        # Pose variables
        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0

        self.prev_encoder_counts = [0.0, 0.0, 0.0, 0.0]
        self.prev_time = self.get_clock().now()

    def cmd_vel_callback(self, msg):
        # Implement your motor control logic here
        pass  # For now, we'll leave it empty

    def read_serial_data(self):
        if self.serial_port.in_waiting > 0:
            try:
                line = self.serial_port.readline().decode('utf-8').strip()
                self.get_logger().debug(f'Received serial data: {line}')

                if line.startswith('<') and line.endswith('>'):
                    data = line[1:-1]  # Remove angle brackets
                    values = data.split(',')
                    if len(values) >= 4:
                        # Parse encoder counts
                        encoder_counts = [float(v) for v in values[:4]]
                        current_time = self.get_clock().now()

                        # Compute odometry
                        self.compute_odometry(encoder_counts, current_time)

                        # Publish encoder counts
                        joint_state_msg = JointState()
                        joint_state_msg.header.stamp = current_time.to_msg()
                        joint_state_msg.name = ['wheel_1', 'wheel_2', 'wheel_3', 'wheel_4']
                        joint_state_msg.position = encoder_counts
                        self.encoder_pub.publish(joint_state_msg)

                        # Update previous counts and time
                        self.prev_encoder_counts = encoder_counts
                        self.prev_time = current_time
                    else:
                        self.get_logger().warning('Received data does not have at least 4 values.')
                else:
                    self.get_logger().warning('Received line does not start and end with angle brackets.')
            except Exception as e:
                self.get_logger().error(f'Error reading serial data: {e}')
        else:
            self.get_logger().debug('No data available on serial port.')

    def compute_odometry(self, encoder_counts, current_time):
        dt = (current_time - self.prev_time).nanoseconds / 1e9  # Convert nanoseconds to seconds
        if dt <= 0:
            self.get_logger().warning('Delta time (dt) is zero or negative, skipping odometry computation.')
            return

        # Calculate difference in encoder counts
        delta_counts = [
            encoder_counts[0] - self.prev_encoder_counts[0],
            encoder_counts[1] - self.prev_encoder_counts[1],
            encoder_counts[2] - self.prev_encoder_counts[2],
            encoder_counts[3] - self.prev_encoder_counts[3],
        ]

        # Convert counts to wheel rotations (radians)
        delta_rotations = [
            (delta_count / self.encoder_resolution) * 2 * math.pi
            for delta_count in delta_counts
        ]

        # Compute wheel distances
        wheel_distances = [
            delta_rotation * self.wheel_radius
            for delta_rotation in delta_rotations
        ]

        # Compute odometry for differential drive robot
        left_distance = (wheel_distances[0] + wheel_distances[2]) / 2.0  # Left wheels
        right_distance = (wheel_distances[1] + wheel_distances[3]) / 2.0  # Right wheels

        delta_s = (left_distance + right_distance) / 2.0  # Linear displacement
        delta_theta = (right_distance - left_distance) / self.wheel_track  # Angular displacement

        # Update pose
        delta_x = delta_s * math.cos(self.theta + delta_theta / 2.0)
        delta_y = delta_s * math.sin(self.theta + delta_theta / 2.0)

        self.x += delta_x
        self.y += delta_y
        self.theta += delta_theta

        # Normalize theta to the range [-pi, pi]
        self.theta = (self.theta + math.pi) % (2 * math.pi) - math.pi

        # Compute velocities
        vx = delta_s / dt
        vth = delta_theta / dt

        # Publish odometry message
        odom_msg = Odometry()
        odom_msg.header.stamp = current_time.to_msg()
        odom_msg.header.frame_id = 'odom'
        odom_msg.child_frame_id = 'base_link'

        # Set the position
        odom_msg.pose.pose.position.x = self.x
        odom_msg.pose.pose.position.y = self.y
        odom_msg.pose.pose.position.z = 0.0

        # Set the orientation
        quat = quaternion_from_euler(0, 0, self.theta)
        odom_msg.pose.pose.orientation = Quaternion(
            x=quat[0],
            y=quat[1],
            z=quat[2],
            w=quat[3],
        )

        # Set velocities
        odom_msg.twist.twist.linear.x = vx
        odom_msg.twist.twist.linear.y = 0.0
        odom_msg.twist.twist.angular.z = vth

        self.odom_pub.publish(odom_msg)
        self.get_logger().debug('Published odometry message.')

def main(args=None):
    rclpy.init(args=args)
    node = EncoderOdometryNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
