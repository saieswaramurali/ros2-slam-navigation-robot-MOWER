#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32MultiArray
import serial


class SerialTransmitter(Node):
    def __init__(self):
        super().__init__('serial_transmitter')

        # Declare and get serial port parameters
        self.declare_parameter("port", "/dev/ttyUSB0")
        self.declare_parameter("baudrate", 115200)

        port = self.get_parameter("port").value
        baudrate = self.get_parameter("baudrate").value

        try:
            self.serial_port = serial.Serial(port, baudrate, timeout=0.1)
            self.get_logger().info(f"Serial port {port} opened successfully.")
        except serial.SerialException as e:
            self.get_logger().error(f"Could not open serial port {port}: {str(e)}")
            self.serial_port = None

        # Subscriber for motor speeds (expects a vector of length 4)
        self.subscription = self.create_subscription(
            Float32MultiArray,
            'motor_speeds',
            self.motor_speed_callback,
            10
        )

    def motor_speed_callback(self, msg: Float32MultiArray):
        if self.serial_port and self.serial_port.is_open:
            try:
                # Ensure exactly 4 elements in the received message
                if len(msg.data) != 4:
                    self.get_logger().error(f"Received {len(msg.data)} elements, expected 4.")
                    return

                # Format the values as a comma-separated string
                data_string = f"{msg.data[0]:.2f},{msg.data[1]:.2f},{msg.data[2]:.2f},{msg.data[3]:.2f}\n"

                # Send data to the ESP32 via serial
                self.serial_port.write(data_string.encode("utf-8"))
                self.serial_port.flush()

                self.get_logger().info(f"Sent: {data_string.strip()}")
            except serial.SerialException as e:
                self.get_logger().error(f"Serial transmission error: {str(e)}")


def main(args=None):
    rclpy.init(args=args)
    node = SerialTransmitter()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        if node.serial_port and node.serial_port.is_open:
            node.serial_port.close()
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
