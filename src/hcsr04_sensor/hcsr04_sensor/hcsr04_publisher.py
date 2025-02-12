#!/usr/bin/env python3
import serial
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Range

class HCSR04Publisher(Node):
    def __init__(self):
        super().__init__('hcsr04_publisher')

        # Initialize the serial port once
        try:
            self.serial_port = serial.Serial(
                port="/dev/ttyACM0",  # Adjust the port as necessary
                baudrate=9600,
                timeout=1  # Timeout in seconds
            )
            self.get_logger().info("Serial port is open and ready.")
        except serial.SerialException as e:
            self.get_logger().error(f"Failed to open serial port: {e}")
            exit(1)

        # Create a publisher for the Range message
        self.publisher_ = self.create_publisher(Range, 'ultrasonic_range', 10)
        
        # Create a timer that calls timer_callback every 0.1 seconds
        self.timer = self.create_timer(0.1, self.timer_callback)

    def timer_callback(self):
        try:
            # Read data from the serial port
            line = self.serial_port.readline().decode('utf-8').rstrip()
            if line:
                # Parse the distance measurement
                try:
                    distance_cm = float(line)
                    self.get_logger().info(f"Received distance: {distance_cm} cm")
                except ValueError:
                    self.get_logger().error(f"Invalid data received: '{line}'")
                    return

                # Create and populate the Range message
                msg = Range()
                msg.header.stamp = self.get_clock().now().to_msg()
                msg.header.frame_id = 'ultrasonic_sensor'
                msg.radiation_type = Range.ULTRASOUND
                msg.field_of_view = 0.05  # Adjust as needed
                msg.min_range = 0.02  # Minimum range of HC-SR04 in meters
                msg.max_range = 4.0   # Maximum range of HC-SR04 in meters
                msg.range = distance_cm / 100.0  # Convert cm to meters

                # Publish the message
                self.publisher_.publish(msg)
                self.get_logger().info(f"Published range: {msg.range:.4f} m")
            else:
                self.get_logger().warning("No data received from serial port.")
        except serial.SerialException as e:
            self.get_logger().error(f"Serial port error: {e}")
        except Exception as e:
            self.get_logger().error(f"Unexpected error: {e}")

    def destroy_node(self):
        # Close the serial port when the node is destroyed
        if self.serial_port.is_open:
            self.serial_port.close()
            self.get_logger().info("Serial port closed.")
        super().destroy_node()

def main(args=None):
    rclpy.init(args=args)
    node = HCSR04Publisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
