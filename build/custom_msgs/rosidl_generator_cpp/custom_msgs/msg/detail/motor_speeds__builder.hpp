// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from custom_msgs:msg/MotorSpeeds.idl
// generated code does not contain a copyright notice

#ifndef CUSTOM_MSGS__MSG__DETAIL__MOTOR_SPEEDS__BUILDER_HPP_
#define CUSTOM_MSGS__MSG__DETAIL__MOTOR_SPEEDS__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "custom_msgs/msg/detail/motor_speeds__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace custom_msgs
{

namespace msg
{

namespace builder
{

class Init_MotorSpeeds_rear_right
{
public:
  explicit Init_MotorSpeeds_rear_right(::custom_msgs::msg::MotorSpeeds & msg)
  : msg_(msg)
  {}
  ::custom_msgs::msg::MotorSpeeds rear_right(::custom_msgs::msg::MotorSpeeds::_rear_right_type arg)
  {
    msg_.rear_right = std::move(arg);
    return std::move(msg_);
  }

private:
  ::custom_msgs::msg::MotorSpeeds msg_;
};

class Init_MotorSpeeds_rear_left
{
public:
  explicit Init_MotorSpeeds_rear_left(::custom_msgs::msg::MotorSpeeds & msg)
  : msg_(msg)
  {}
  Init_MotorSpeeds_rear_right rear_left(::custom_msgs::msg::MotorSpeeds::_rear_left_type arg)
  {
    msg_.rear_left = std::move(arg);
    return Init_MotorSpeeds_rear_right(msg_);
  }

private:
  ::custom_msgs::msg::MotorSpeeds msg_;
};

class Init_MotorSpeeds_front_right
{
public:
  explicit Init_MotorSpeeds_front_right(::custom_msgs::msg::MotorSpeeds & msg)
  : msg_(msg)
  {}
  Init_MotorSpeeds_rear_left front_right(::custom_msgs::msg::MotorSpeeds::_front_right_type arg)
  {
    msg_.front_right = std::move(arg);
    return Init_MotorSpeeds_rear_left(msg_);
  }

private:
  ::custom_msgs::msg::MotorSpeeds msg_;
};

class Init_MotorSpeeds_front_left
{
public:
  Init_MotorSpeeds_front_left()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_MotorSpeeds_front_right front_left(::custom_msgs::msg::MotorSpeeds::_front_left_type arg)
  {
    msg_.front_left = std::move(arg);
    return Init_MotorSpeeds_front_right(msg_);
  }

private:
  ::custom_msgs::msg::MotorSpeeds msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::custom_msgs::msg::MotorSpeeds>()
{
  return custom_msgs::msg::builder::Init_MotorSpeeds_front_left();
}

}  // namespace custom_msgs

#endif  // CUSTOM_MSGS__MSG__DETAIL__MOTOR_SPEEDS__BUILDER_HPP_
