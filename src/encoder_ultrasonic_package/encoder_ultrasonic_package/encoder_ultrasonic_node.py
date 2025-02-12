import math
import rclpy
from rclpy.node import Node
import serial
import re
from sensor_msgs.msg import JointState, Range
from geometry_msgs.msg import Twist, Quaternion
from nav_msgs.msg import Odometry
class EncoderUltrasonicNode(Node):
    def __init__(self):
        super().__init__('encoder_ultrasonic_node')
        self.serial_port = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
        
        # Publishers
        self.encoder_pub = self.create_publisher(JointState, 'encoder_counts', 10)
        # self.ultrasonic_pub = self.create_publisher(Range, 'ultrasonic_range', 10)
        # Subscribe to /cmd_vel topic
        self.cmd_vel_sub = self.create_subscription(Twist, 'cmd_vel', self.cmd_vel_callback, 10)
        # Timer to read from serial at 10 Hz
        self.create_timer(0.1, self.read_serial_data)
        # Robot parameters (adjust these values to match your robot)
        self.wheel_radius = 0.065  # Wheel radius in meters
        self.wheel_base = 0.09     # Distance between front and rear wheels (length-wise)
        self.wheel_track = 0.13    # Distance between left and right wheels (width-wise)
        self.encoder_resolution = 150  # Encoder counts per wheel revolution

        # Pose variables
        self.x = 0.0  # Position along the x-axis
        self.y = 0.0  # Position along the y-axis
        self.theta = 0.0  # Orientation angle in radians

        self.prev_encoder_counts = [0.0, 0.0, 0.0, 0.0]  # Previous encoder counts
        self.prev_time = self.get_clock().now()
        self.odom_pub = self.create_publisher(Odometry, 'odom', 10)

    def calculate_motor_speeds(linear_speed, angular_speed):
        # Implement kinematics to convert linear and angular speeds to motor speeds
        # This depends on your robot's drive configuration (e.g., differential, skid-steer)
        max_speed = 255  # Maximum speed value
        wheel_base = 0.5  # Distance between wheels (adjust as needed)

        v_left = linear_speed - (angular_speed * wheel_base / 2)
        v_right = linear_speed + (angular_speed * wheel_base / 2)

        # Map speeds to motor values
        m1_speed = int(v_left * max_speed)
        m2_speed = int(v_right * max_speed)
        m3_speed = int(v_left * max_speed)
        m4_speed = int(v_right * max_speed)
    
        return [m1_speed, m2_speed, m3_speed, m4_speed]

    
    def cmd_vel_callback(self, msg):
        # Convert Twist message to motor speeds
        linear_speed = msg.linear.x  # Forward/backward
        angular_speed = msg.angular.z  # Rotation

        # Calculate motor speeds
        motor_speeds = calculate_motor_speeds(linear_speed, angular_speed)

        # Create command string
        command = f"<{motor_speeds[0]},{motor_speeds[1]},{motor_speeds[2]},{motor_speeds[3]}>\n"
        # Send command over serial
        self.serial_port.write(command.encode('utf-8'))

    def quaternion_from_euler(roll, pitch, yaw):
    #Convert Euler angles to quaternion.
        qx = math.sin(roll/2) * math.cos(pitch/2) * math.cos(yaw/2) - \
             math.cos(roll/2) * math.sin(pitch/2) * math.sin(yaw/2)
        qy = math.cos(roll/2) * math.sin(pitch/2) * math.cos(yaw/2) + \
             math.sin(roll/2) * math.cos(pitch/2) * math.sin(yaw/2)
        qz = math.cos(roll/2) * math.cos(pitch/2) * math.sin(yaw/2) - \
             math.sin(roll/2) * math.sin(pitch/2) * math.cos(yaw/2)
        qw = math.cos(roll/2) * math.cos(pitch/2) * math.cos(yaw/2) + \
             math.sin(roll/2) * math.sin(pitch/2) * math.sin(yaw/2)
        return [qx, qy, qz, qw]

    def read_serial_data(self):
        if self.serial_port.in_waiting > 0:
            try:
                line = self.serial_port.readline().decode('utf-8').strip()
                if line.startswith('<') and line.endswith('>'):
                    data = line[1:-1]  # Remove angle brackets
                    values = data.split(',')
                    if len(values) == 5:
                        # Parse encoder counts
                        encoder_counts = [float(v) for v in values[:4]]
                        distance_cm = float(values[4])

                        current_time = self.get_clock().now()

                        # Calculate time difference
                        dt = (current_time - self.prev_time).nanoseconds / 1e9  # Convert nanoseconds to seconds
                        if dt == 0:
                            return  # Avoid division by zero

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

                    # Compute odometry for skid-steer robot
                    left_distance = (wheel_distances[0] + wheel_distances[2]) / 2.0  # Left wheels
                    right_distance = (wheel_distances[1] + wheel_distances[3]) / 2.0  # Right wheels

                    delta_s = (left_distance + right_distance) / 2.0  # Linear displacement
                    delta_theta = (right_distance - left_distance) / self.wheel_track  # Angular displacement

                    # Update pose
                    self.x += delta_s * math.cos(self.theta + delta_theta / 2.0)
                    self.y += delta_s * math.sin(self.theta + delta_theta / 2.0)
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

                    # Publish encoder counts and ultrasonic data as before...

                    # Update previous counts and time
                    self.prev_encoder_counts = encoder_counts
                    self.prev_time = current_time
            except Exception as e:
                self.get_logger().error(f'Error reading serial data: {e}')

    # def read_serial_data(self):
        # if self.serial_port.in_waiting > 0:
        #     try:
        #         line = self.serial_port.readline().decode('utf-8').strip()
        #         if line.startswith('<') and line.endswith('>'):
        #             data = line[1:-1]  # Remove angle brackets
        #             values = data.split(',')
        #             if len(values) == 5:
        #                 # Parse encoder counts
        #                 encoder_counts = [float(v) for v in values[:4]]
        #                 distance_cm = float(values[4])

        #                 # Publish encoder counts
        #                 joint_state_msg = JointState()
        #                 joint_state_msg.header.stamp = self.get_clock().now().to_msg()
        #                 joint_state_msg.name = ['Rear Left', 'Rear Right', 'Front Left', 'Front Right']
        #                 joint_state_msg.position = encoder_counts
        #                 self.encoder_pub.publish(joint_state_msg)

        #                 # Publish ultrasonic reading
        #                 range_msg = Range()
        #                 range_msg.header.stamp = self.get_clock().now().to_msg()
        #                 range_msg.radiation_type = Range.ULTRASOUND
        #                 range_msg.field_of_view = 0.5  # Adjust as per your sensor
        #                 range_msg.min_range = 0.02  # Minimum range in meters
        #                 range_msg.max_range = 4.0   # Maximum range in meters
        #                 range_msg.range = distance_cm / 100.0  # Convert cm to meters
        #                 self.ultrasonic_pub.publish(range_msg)
        #     except Exception as e:
        #         self.get_logger().error(f'Error reading serial data: {e}')
                
def main(args=None):
    rclpy.init(args=args)
    node = EncoderUltrasonicNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
