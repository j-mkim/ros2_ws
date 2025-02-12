cmake_minimum_required(VERSION 3.8)
project(wheel_encoder_odometry)

# Default to C++17
if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 17)
endif()

# Add compiler warnings
if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# Find dependencies
find_package(ament_cmake REQUIRED)
find_package(ament_cmake_python REQUIRED)
find_package(rclcpp REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(tf2 REQUIRED)
find_package(tf2_ros REQUIRED)
find_package(tf2_geometry_msgs REQUIRED)
# Install Python modules
ament_python_install_package(${PROJECT_NAME})


# Install scripts (if any)
install(PROGRAMS
  wheel_encoder_odometry/encoder_odometry_node.py
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()
