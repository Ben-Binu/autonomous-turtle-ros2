#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import sys, termios, tty

# Key mapping
key_mapping = {
    'w': (1.0, 0.0),
    's': (-1.0, 0.0),
    'a': (0.0, 1.0),
    'd': (0.0, -1.0)
}

def get_key():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        key = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return key

class TurtleKeyboard(Node):
    def __init__(self):
        super().__init__('turtle_keyboard')
        self.pub = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)

    def run(self):
        print("Use W A S D keys to move the turtle. Press Ctrl+C to exit.")
        try:
            while rclpy.ok():
                key = get_key()
                if key in key_mapping:
                    linear, angular = key_mapping[key]
                    msg = Twist()
                    msg.linear.x = linear
                    msg.angular.z = angular
                    self.pub.publish(msg)
                elif key == '\x03':  # Ctrl+C
                    break
        except KeyboardInterrupt:
            pass

def main():
    rclpy.init()
    node = TurtleKeyboard()
    node.run()
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

