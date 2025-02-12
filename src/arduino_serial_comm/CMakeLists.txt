cmake_minimum_required(VERSION 3.5)
project(arduino_serial_comm)

# Default to C++17
if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 17)
endif()

# Find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)
find_package(sensor_msgs REQUIRED)

# For Boost.Asio
find_package(Boost REQUIRED COMPONENTS system)

# Add executable
add_executable(serial_comm_node src/serial_comm_node.cpp)

# Specify include directories
target_include_directories(serial_comm_node PRIVATE
  ${Boost_INCLUDE_DIRS}
)

# Link dependencies
ament_target_dependencies(serial_comm_node
  rclcpp
  std_msgs
  sensor_msgs
)

# Link Boost libraries
target_link_libraries(serial_comm_node
  ${Boost_LIBRARIES}
)

# Install targets
install(TARGETS
  serial_comm_node
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()
