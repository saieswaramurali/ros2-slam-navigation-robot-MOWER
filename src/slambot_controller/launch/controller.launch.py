from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import ExecuteProcess

def generate_launch_description():
    joy_node = Node(
        package='joy',
        namespace='joystick',
        executable='joy_node',
        name='sai_joystick',
        output='screen'
    )

    joystick_mapper_node = Node(
        package='slambot_controller',  # Replace with your package name
        executable='joystick_mapper',  # Replace with your node executable name
        name='joystick_mapper',
        output='screen'
    )

    serial_transmitter = Node(
        package='slambot_controller',  # Replace with your package name
        executable='serial_transmitter',  # Replace with your node executable name
        name='serial_transmitter',
        output='screen'
    )

    return LaunchDescription([
        ExecuteProcess(
            cmd=['sudo', 'chmod', '666', '/dev/ttyUSB0'],
            shell=True,
            output='screen',
            name='set_permissions'
        ),
        joy_node,
        joystick_mapper_node,
        serial_transmitter, 
    ])