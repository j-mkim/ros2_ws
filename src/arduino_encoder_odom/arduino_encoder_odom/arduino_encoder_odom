#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from geometry_msgs.msg import TransformStamped
import serial
import math
import tf2_ros
import threading

class ArduinoEncoderOdomNode(Node):
    def __init__(self):
        super().__init__('encoder_odom_node')
        # Parameters (adjust these to match your robot)
        self.declare_parameter('serial_port', '/dev/ttyACM0')
        self.declare_parameter('baud_rate', 115200)
        self.declare_parameter('wheel_radius', 0.03)            # in meters (example)
        self.declare_parameter('ticks_per_revolution', 576)       # encoder ticks per revolution
        self.declare_parameter('wheel_base', 0.15)                # distance between left & right wheels (meters)
        
        self.serial_port_name = self.get_parameter('serial_port').get_parameter_value().string_value
        self.baud_rate = self.get_parameter('baud_rate').get_parameter_value().integer_value
        self.wheel_radius = self.get_parameter('wheel_radius').get_parameter_value().double_value
        self.ticks_per_rev = self.get_parameter('ticks_per_revolution').get_parameter_value().integer_value
        self.wheel_base = self.get_parameter('wheel_base').get_parameter_value().double_value
        
        self.odom_pub = self.create_publisher(Odometry, 'odom', 10)
        self.tf_broadcaster = tf2_ros.TransformBroadcaster(self)
        
        try:
            self.serial = serial.Serial(self.serial_port_name, self.baud_rate, timeout=1)
            self.get_logger().info(f"Opened serial port {self.serial_port_name}")
        except Exception as e:
            self.get_logger().error(f"Failed to open serial port: {e}")
            rclpy.shutdown()
        
        # Initialize previous encoder readings (for odometry delta calculations)
        self.prev_left = None  # average of left encoders (Rear Left & Front Left)
        self.prev_right = None # average of right encoders (Rear Right & Front Right)
        
        # Odometry state (x, y, theta)
        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0
        
        # Last update time
        self.last_time = self.get_clock().now()
        
        # Start serial reading thread
        self.serial_thread = threading.Thread(target=self.read_serial)
        self.serial_thread.daemon = True
        self.serial_thread.start()
        
    def read_serial(self):
        while rclpy.ok():
            try:
                line = self.serial.readline().decode('utf-8').strip()
                if line.startswith("<") and line.endswith(">"):
                    # Remove the angle brackets and split by commas
                    data = line[1:-1]
                    parts = data.split(',')
                    if len(parts) == 4:
                        try:
                            e1 = int(parts[0])
                            e2 = int(parts[1])
                            e3 = int(parts[2])
                            e4 = int(parts[3])
                            self.process_encoder_data(e1, e2, e3, e4)
                        except Exception as e:
                            self.get_logger().error(f"Error parsing encoder values: {e}")
            except Exception as e:
                self.get_logger().error(f"Error reading serial: {e}")
    
    def process_encoder_data(self, e1, e2, e3, e4):
        # Assume:
        #   Rear Left  & Front Left  are on the left side
        #   Rear Right & Front Right are on the right side
        left = (e1 + e3) / 2.0
        right = (e2 + e4) / 2.0
        
        if self.prev_left is None or self.prev_right is None:
            self.prev_left = left
            self.prev_right = right
            return
        
        # Compute differences since last reading
        delta_left = left - self.prev_left
        delta_right = right - self.prev_right
        
        self.prev_left = left
        self.prev_right = right
        
        # Convert encoder ticks to distance traveled
        # Each tick represents: (2 * pi * wheel_radius) / ticks_per_rev meters.
        distance_per_tick = (2 * math.pi * self.wheel_radius) / self.ticks_per_rev
        d_left = delta_left * distance_per_tick
        d_right = delta_right * distance_per_tick
        
        # Compute center displacement and change in orientation (differential drive kinematics)
        d_center = (d_left + d_right) / 2.0
        delta_theta = (d_right - d_left) / self.wheel_base
        
        # Update odometry (using a simple integration scheme)
        self.x += d_center * math.cos(self.theta + delta_theta / 2.0)
        self.y += d_center * math.sin(self.theta + delta_theta / 2.0)
        self.theta += delta_theta
        
        current_time = self.get_clock().now()
        dt = (current_time - self.last_time).nanoseconds / 1e9
        self.last_time = current_time
        
        vx = d_center / dt if dt > 0 else 0.0
        vth = delta_theta / dt if dt > 0 else 0.0
        
        # Create and publish Odometry message
        odom = Odometry()
        odom.header.stamp = current_time.to_msg()
        odom.header.frame_id = "odom"
        odom.child_frame_id = "base_link"
        odom.pose.pose.position.x = self.x
        odom.pose.pose.position.y = self.y
        odom.pose.pose.position.z = 0.0
        q = self.quaternion_from_yaw(self.theta)
        odom.pose.pose.orientation.x = q[0]
        odom.pose.pose.orientation.y = q[1]
        odom.pose.pose.orientation.z = q[2]
        odom.pose.pose.orientation.w = q[3]
        odom.twist.twist.linear.x = vx
        odom.twist.twist.angular.z = vth
        
        self.odom_pub.publish(odom)
        
        # Also broadcast the transform from odom to base_link
        t = TransformStamped()
        t.header.stamp = current_time.to_msg()
        t.header.frame_id = "odom"
        t.child_frame_id = "base_link"
        t.transform.translation.x = self.x
        t.transform.translation.y = self.y
        t.transform.translation.z = 0.0
        t.transform.rotation.x = q[0]
        t.transform.rotation.y = q[1]
        t.transform.rotation.z = q[2]
        t.transform.rotation.w = q[3]
        self.tf_broadcaster.sendTransform(t)
    
    def quaternion_from_yaw(self, yaw):
        # Convert a yaw angle (in radians) into a quaternion (x, y, z, w)
        qx = 0.0
        qy = 0.0
        qz = math.sin(yaw / 2.0)
        qw = math.cos(yaw / 2.0)
        return (qx, qy, qz, qw)

def main(args=None):
    rclpy.init(args=args)
    node = ArduinoEncoderOdomNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
