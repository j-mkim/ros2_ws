import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/orin/ros2_ws/src/encoder_ultrasonic_package/install/encoder_ultrasonic_package'
