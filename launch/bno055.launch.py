import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

def generate_launch_description():
    pkg_ros_gz_sim_demos = get_package_share_directory('ros_gz_sim_demos')
    pkg_sdformat_urdf = get_package_share_directory('launch')

    return LaunchDescription([
        Node(
            package='bno055_publisher',
            namespace='bno055_publisher',
            executable='bno055_publisher',
            name='imu'
        ),
        Node(
            package='bno055_publisher',
            namespace='bno055_subscriber',
            executable='bno055_subscriber',
            name='imu'
        ),   

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
        )
        # IncludeLaunchDescription(
        #     PythonLaunchDescriptionSource(
        #         os.path.join(pkg_ros_gz_sim_demos, 'launch', 'imu.launch.py')),
        # )        
    ])