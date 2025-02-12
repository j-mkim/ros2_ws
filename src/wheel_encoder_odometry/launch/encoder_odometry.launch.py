from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='wheel_encoder_odometry',
            executable='encoder_odometry_node',
            name='encoder_odometry_node',
            output='screen',
            parameters=[{
                'serial_port': '/dev/ttyACM0',
                'baud_rate': 115200,
                'wheel_radius': 0.05,
                'wheel_base': 0.3,
                'wheel_track': 0.4,
                'encoder_resolution': 4096,
            }]
        ),
    ])
