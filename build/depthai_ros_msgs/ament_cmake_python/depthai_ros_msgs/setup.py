from setuptools import find_packages
from setuptools import setup

setup(
    name='depthai_ros_msgs',
    version='2.10.4',
    packages=find_packages(
        include=('depthai_ros_msgs', 'depthai_ros_msgs.*')),
)
