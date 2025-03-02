// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from custom_msgs:msg/MotorSpeeds.idl
// generated code does not contain a copyright notice

#ifndef CUSTOM_MSGS__MSG__DETAIL__MOTOR_SPEEDS__STRUCT_H_
#define CUSTOM_MSGS__MSG__DETAIL__MOTOR_SPEEDS__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in msg/MotorSpeeds in the package custom_msgs.
typedef struct custom_msgs__msg__MotorSpeeds
{
  int16_t front_left;
  int16_t front_right;
  int16_t rear_left;
  int16_t rear_right;
} custom_msgs__msg__MotorSpeeds;

// Struct for a sequence of custom_msgs__msg__MotorSpeeds.
typedef struct custom_msgs__msg__MotorSpeeds__Sequence
{
  custom_msgs__msg__MotorSpeeds * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} custom_msgs__msg__MotorSpeeds__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // CUSTOM_MSGS__MSG__DETAIL__MOTOR_SPEEDS__STRUCT_H_
