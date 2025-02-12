// src/serial_comm_node.cpp

#include <rclcpp/rclcpp.hpp>
#include "std_msgs/msg/string.hpp"
#include "sensor_msgs/msg/range.hpp"
#include "geometry_msgs/msg/twist.hpp"
#include <boost/asio.hpp>
#include <thread>

using namespace std::chrono_literals;

class SerialCommNode : public rclcpp::Node {
public:
  SerialCommNode()
  : Node("serial_comm_node"), io_(), serial_(io_) {
    // Parameters
    this->declare_parameter<std::string>("port", "/dev/ttyACM0");
    this->declare_parameter<int>("baudrate", 115200);
    
    std::string port;
    int baudrate;
    this->get_parameter("port", port);
    this->get_parameter("baudrate", baudrate);
    
    // Open serial port
    serial_.open(port);
    serial_.set_option(boost::asio::serial_port_base::baud_rate(baudrate));
    
    // Publishers
    range_pub_ = this->create_publisher<sensor_msgs::msg::Range>("ultrasonic_range", 10);
    
    // Subscribers
    cmd_sub_ = this->create_subscription<geometry_msgs::msg::Twist>(
      "cmd_vel", 10,
      std::bind(&SerialCommNode::cmdVelCallback, this, std::placeholders::_1));
    
    // Start reading thread
    read_thread_ = std::thread(&SerialCommNode::readSerial, this);
  }
  
  ~SerialCommNode() {
    serial_.close();
    if (read_thread_.joinable()) {
      read_thread_.join();
    }
  }
  
private:
  void readSerial() {
    boost::asio::streambuf buf;
    while (rclcpp::ok()) {
      try {
        boost::asio::read_until(serial_, buf, '\n');
        std::istream is(&buf);
        std::string line;
        std::getline(is, line);
        int distance = std::stoi(line);
        
        // Publish Range message
        auto range_msg = sensor_msgs::msg::Range();
        range_msg.header.stamp = this->now();
        range_msg.header.frame_id = "ultrasonic";
        range_msg.radiation_type = sensor_msgs::msg::Range::ULTRASOUND;
        range_msg.field_of_view = 0.5; // Adjust as needed
        range_msg.min_range = 2.0;
        range_msg.max_range = 400.0;
        range_msg.range = static_cast<float>(distance);
        
        range_pub_->publish(range_msg);
        
      } catch (std::exception &e) {
        RCLCPP_ERROR(this->get_logger(), "Error reading serial: %s", e.what());
      }
    }
  }
  
  void cmdVelCallback(const geometry_msgs::msg::Twist::SharedPtr msg) {
    // Convert Twist message to motor commands
    // Example: simple mapping; adjust based on your motor controller logic
    int linear = static_cast<int>(msg->linear.x * 100); // Scale as needed
    int angular = static_cast<int>(msg->angular.z * 100);
    
    std::string command = "FWD," + std::to_string(linear) + "\n"; // Example
    boost::asio::write(serial_, boost::asio::buffer(command));
  }
  
  // Members
  boost::asio::io_service io_;
  boost::asio::serial_port serial_;
  std::thread read_thread_;
  
  rclcpp::Publisher<sensor_msgs::msg::Range>::SharedPtr range_pub_;
  rclcpp::Subscription<geometry_msgs::msg::Twist>::SharedPtr cmd_sub_;
};

int main(int argc, char **argv) {
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<SerialCommNode>());
  rclcpp::shutdown();
  return 0;
}
