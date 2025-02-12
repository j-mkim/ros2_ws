import rclpy
from rclpy.node import Node
import serial
import re
from sensor_msgs.msg import JointState, Range
from geometry_msgs.msg import Twist

class EncoderUltrasonicNode(Node):
    def __init__(self):
        super().__init__('encoder_ultrasonic_node')
        self.serial_port = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
        
        # Publishers
        self.encoder_pub = self.create_publisher(JointState, 'encoder_counts', 10)
        self.ultrasonic_pub = self.create_publisher(Range, 'ultrasonic_range', 10)
        # Subscribe to /cmd_vel topic
        self.cmd_vel_sub = self.create_subscription(Twist, 'cmd_vel', self.cmd_vel_callback, 10)
        # Timer to read from serial at 10 Hz
        self.create_timer(0.1, self.read_serial_data)

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

                        # Publish encoder counts
                        joint_state_msg = JointState()
                        joint_state_msg.header.stamp = self.get_clock().now().to_msg()
                        joint_state_msg.name = ['Rear Left', 'Rear Right', 'Front Left', 'Front Right']
                        joint_state_msg.position = encoder_counts
                        self.encoder_pub.publish(joint_state_msg)

                        # Publish ultrasonic reading
                        range_msg = Range()
                        range_msg.header.stamp = self.get_clock().now().to_msg()
                        range_msg.radiation_type = Range.ULTRASOUND
                        range_msg.field_of_view = 0.5  # Adjust as per your sensor
                        range_msg.min_range = 0.02  # Minimum range in meters
                        range_msg.max_range = 4.0   # Maximum range in meters
                        range_msg.range = distance_cm / 100.0  # Convert cm to meters
                        self.ultrasonic_pub.publish(range_msg)
            except Exception as e:
                self.get_logger().error(f'Error reading serial data: {e}')
                
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

def main(args=None):
    rclpy.init(args=args)
    node = EncoderUltrasonicNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
