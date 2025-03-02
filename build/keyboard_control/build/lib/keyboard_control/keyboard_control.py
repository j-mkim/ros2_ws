import select
import sys
import termios
import tty

# Remove Twist import because we're using a custom message instead.
# from geometry_msgs.msg import Twist

import rclpy
from rclpy.qos import qos_profile_sensor_data

# Import your custom message.
# Replace 'your_package' with the name of your package.
from keyboard_control import MotorCommands

msg = """
Control Your Robot with WASD:
   w: forward
   s: backward
   a: turn left
   d: turn right

   x: STOP

Speed adjustments:
   q: increase speed, 
   z: decrease speed

CTRL-C to quit
"""

# Define WASD move bindings: (x, y, z, th)
moveBindings = {
    'w': (1, 0, 0, 0),    # Forward
    's': (-1, 0, 0, 0),   # Backward
    'a': (0, 0, 0, 1),    # Turn left
    'd': (0, 0, 0, -1),   # Turn right
    'x': (0, 0, 0, 0),    # Stop
}

speedBindings = {
    'q': (1.1, 1.1),
    'z': (0.9, 0.9),
}

def getKey(settings):
    tty.setraw(sys.stdin.fileno())
    select.select([sys.stdin], [], [], 0)
    key = sys.stdin.read(1)
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key

def vels(speed, turn):
    return 'Speed: {} | Turn: {}'.format(speed, turn)

def main():
    settings = termios.tcgetattr(sys.stdin)

    rclpy.init()

    # Create your node and publisher for MotorCommands
    node = rclpy.create_node('keyboard_control')
    pub = node.create_publisher(MotorCommands, '/cmd_vel', qos_profile=qos_profile_sensor_data)

    # Parameters for speed and turning
    speed = 0.5
    turn = 1.0
    x = 0.0
    th = 0.0

    # Define half the track width (meters); adjust as needed for your robot
    half_track = 0.2

    try:
        print(msg)
        print(vels(speed, turn))
        while True:
            key = getKey(settings)
            if key in moveBindings.keys():
                x = moveBindings[key][0]
                th = moveBindings[key][3]
            elif key in speedBindings.keys():
                speed *= speedBindings[key][0]
                turn *= speedBindings[key][1]
                print(vels(speed, turn))
            else:
                x = 0.0
                th = 0.0
                if key == '\x03':  # CTRL-C to quit.
                    break

            # Compute motor speeds from the drive command:
            # v: forward speed; omega: angular speed.
            v = x * speed
            omega = th * turn

            # Differential drive kinematics:
            left_speed = v - omega * half_track
            right_speed = v + omega * half_track

            # Create and publish the MotorCommands message.
            motor_cmd = MotorCommands()
            motor_cmd.fl = left_speed
            motor_cmd.rl = left_speed
            motor_cmd.fr = right_speed
            motor_cmd.rr = right_speed

            pub.publish(motor_cmd)

    except Exception as e:
        print("Exception: ", e)

    finally:
        # Stop motors by sending zeros
        motor_cmd = MotorCommands()
        motor_cmd.fl = 0.0
        motor_cmd.fr = 0.0
        motor_cmd.rl = 0.0
        motor_cmd.rr = 0.0
        pub.publish(motor_cmd)

        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)

if __name__ == '__main__':
    main()
