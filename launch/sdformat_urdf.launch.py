from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='gazebo_ros',
            executable='spawn_entity.py',
            output='screen',
            arguments=[
                '-file', '/home/orin/ros2_ws/launch',   # Path to your SDF file
                '-entity', 'my_robot',                # Name of your robot entity
                '-plugin', 'sdformat_urdf'           # Use the sdformat_urdf plugin
                # '-ros2_control_plugin', 'gazebo_ros2_control'  # Optional: if you need ros2_control
            ],
        ),
    ])
