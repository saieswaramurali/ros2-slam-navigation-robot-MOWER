#!/usr/bin/env python3
import math
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Joy
from geometry_msgs.msg import Vector3  
from std_msgs.msg import Float32MultiArray


class JoystickMapper(Node):
    def __init__(self):
        super().__init__('joystick_mapper')
        self.subscription = self.create_subscription(
            Joy,
            '/joystick/joy',  # Joystick topic
            self.joy_callback,
            10)
        self.publisher = self.create_publisher(Float32MultiArray, 'motor_speeds', 10)
        self.get_logger().info("Joystick Mapper Node Initialized")

    def joy_callback(self, msg: Joy):
        left_x = msg.axes[0]  
        left_y = msg.axes[1]  

        left_magnitude = min(1.0, math.sqrt(left_x**2 + left_y**2))  
        left_direction = (math.atan2(left_y, -left_x) * 180.0 / math.pi) % 360.0

        dir1 = 0.0 
        dir2 = 0.0 
        pwm1 = 0.0
        pwm2 = 0.0 

        if left_direction >= 0 and left_direction <= 180 : 
            dir1 = 1.0 
            dir2 = 1.0
        else : 
            dir1 = 0.0
            dir2 = 0.0 

        max_throttle = int(left_magnitude * 255) 

        if left_direction < 90 or left_direction > 270 : 
            pwm1 = max_throttle 
            pwm2 = max_throttle * left_magnitude
        else : 
            pwm1 = max_throttle * left_magnitude
            pwm2 = max_throttle 

        self.get_logger().info(f"Left Stick - Magnitude: {left_magnitude:.2f}, Direction: {left_direction:.2f}°")
        self.get_logger().info(f"Motor Speeds - dir1: {dir1}, dir2: {dir2}, pwm1: {pwm1}, pwm2: {pwm2}")

        output = Float32MultiArray()
        output.data = [float(dir1), float(dir2), float(pwm1), float(pwm2)]  
        self.publisher.publish(output)


def main(args=None):
    rclpy.init(args=args)
    node = JoystickMapper()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
