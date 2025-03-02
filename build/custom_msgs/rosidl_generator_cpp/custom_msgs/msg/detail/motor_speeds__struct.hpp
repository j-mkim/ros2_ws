// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from custom_msgs:msg/MotorSpeeds.idl
// generated code does not contain a copyright notice

#ifndef CUSTOM_MSGS__MSG__DETAIL__MOTOR_SPEEDS__STRUCT_HPP_
#define CUSTOM_MSGS__MSG__DETAIL__MOTOR_SPEEDS__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__custom_msgs__msg__MotorSpeeds __attribute__((deprecated))
#else
# define DEPRECATED__custom_msgs__msg__MotorSpeeds __declspec(deprecated)
#endif

namespace custom_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct MotorSpeeds_
{
  using Type = MotorSpeeds_<ContainerAllocator>;

  explicit MotorSpeeds_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->front_left = 0;
      this->front_right = 0;
      this->rear_left = 0;
      this->rear_right = 0;
    }
  }

  explicit MotorSpeeds_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->front_left = 0;
      this->front_right = 0;
      this->rear_left = 0;
      this->rear_right = 0;
    }
  }

  // field types and members
  using _front_left_type =
    int16_t;
  _front_left_type front_left;
  using _front_right_type =
    int16_t;
  _front_right_type front_right;
  using _rear_left_type =
    int16_t;
  _rear_left_type rear_left;
  using _rear_right_type =
    int16_t;
  _rear_right_type rear_right;

  // setters for named parameter idiom
  Type & set__front_left(
    const int16_t & _arg)
  {
    this->front_left = _arg;
    return *this;
  }
  Type & set__front_right(
    const int16_t & _arg)
  {
    this->front_right = _arg;
    return *this;
  }
  Type & set__rear_left(
    const int16_t & _arg)
  {
    this->rear_left = _arg;
    return *this;
  }
  Type & set__rear_right(
    const int16_t & _arg)
  {
    this->rear_right = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    custom_msgs::msg::MotorSpeeds_<ContainerAllocator> *;
  using ConstRawPtr =
    const custom_msgs::msg::MotorSpeeds_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<custom_msgs::msg::MotorSpeeds_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<custom_msgs::msg::MotorSpeeds_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      custom_msgs::msg::MotorSpeeds_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<custom_msgs::msg::MotorSpeeds_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      custom_msgs::msg::MotorSpeeds_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<custom_msgs::msg::MotorSpeeds_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<custom_msgs::msg::MotorSpeeds_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<custom_msgs::msg::MotorSpeeds_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__custom_msgs__msg__MotorSpeeds
    std::shared_ptr<custom_msgs::msg::MotorSpeeds_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__custom_msgs__msg__MotorSpeeds
    std::shared_ptr<custom_msgs::msg::MotorSpeeds_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const MotorSpeeds_ & other) const
  {
    if (this->front_left != other.front_left) {
      return false;
    }
    if (this->front_right != other.front_right) {
      return false;
    }
    if (this->rear_left != other.rear_left) {
      return false;
    }
    if (this->rear_right != other.rear_right) {
      return false;
    }
    return true;
  }
  bool operator!=(const MotorSpeeds_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct MotorSpeeds_

// alias to use template instance with default allocator
using MotorSpeeds =
  custom_msgs::msg::MotorSpeeds_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace custom_msgs

#endif  // CUSTOM_MSGS__MSG__DETAIL__MOTOR_SPEEDS__STRUCT_HPP_
