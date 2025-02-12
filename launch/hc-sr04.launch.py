import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

def generate_launch_description():
    #pkg_ros_gz_sim_demos = get_package_share_directory('ros_gz_sim_demos')
    
    return LaunchDescription([
        Node(
            package='hc_sr04_publisher',
            namespace='hc_sr04_publisher',
            executable='hc_sr04_publisher',
            name='ultrasonic_sensor'
        ),
        Node(
            package='hc_sr04_publisher',
            namespace='hc_sr04_subscriber',
            executable='hc_sr04_subscriber',
            name='ultrasonic_sensor'
        ),        
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(pkg_ros_gz_sim_demos, 'launch', 'imu.launch.py')),
        )        
    ])