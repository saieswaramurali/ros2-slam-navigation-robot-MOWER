import os
from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import Command, LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    # Define the directory for the rover description package
    rover_description_dir = get_package_share_directory('rover_description')

    # Declare model argument for passing the URDF/Xacro file
    model_arg = DeclareLaunchArgument(
        name='model',
        default_value=os.path.join(rover_description_dir, 'urdf', 'rover.urdf.xacro'),
        description='Absolute path to robot URDF file'
    )

    # Define robot_description as a ParameterValue, using xacro to process the URDF
    robot_description = ParameterValue(
        Command(['xacro ', LaunchConfiguration('model')]),
        value_type=str
    )

    # Node for publishing the robot state
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': robot_description}]
    )

    # Node for joint state publisher GUI
    joint_state_publisher_gui_node = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui'
    )

    # Node for launching RViz2 with a specific configuration file
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', os.path.join(rover_description_dir, 'rviz', 'display.rviz')]
    )

    # Launch description with the necessary nodes
    return LaunchDescription([
        model_arg,
        joint_state_publisher_gui_node,
        robot_state_publisher_node,
        rviz_node
    ])
