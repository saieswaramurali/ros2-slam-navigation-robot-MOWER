import os
from ament_index_python.packages import get_package_share_directory, get_package_prefix
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, SetEnvironmentVariable
from launch.substitutions import Command, LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.actions import IncludeLaunchDescription

def generate_launch_description():
    # Define package directories
    rover_description_dir = get_package_share_directory('rover_description')
    gazebo_ros_dir = get_package_share_directory('gazebo_ros')

    # Declare model argument
    model_arg = DeclareLaunchArgument(
        name='model',
        default_value=os.path.join(rover_description_dir, 'urdf', 'rover.urdf.xacro'),
        description='Absolute path to robot URDF file'
    )

    # Set environment variable for Gazebo model path
    model_path = os.path.join(rover_description_dir, 'models')
    model_path += os.pathsep + os.path.join(get_package_prefix('rover_description'), 'share')
    env_var = SetEnvironmentVariable('GAZEBO_MODEL_PATH', model_path)

    # Define robot description parameter
    robot_description = ParameterValue(
        Command(['xacro ', LaunchConfiguration('model')]),
        value_type=str
    )

    # Nodes
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': robot_description}]
    )

    start_gazebo_server = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(gazebo_ros_dir, 'launch', 'gzserver.launch.py')
        )
    )

    start_gazebo_client = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(gazebo_ros_dir, 'launch', 'gzclient.launch.py')
        )
    )

    spawn_robot = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=[
            '-file', LaunchConfiguration('model'),
            '-entity', 'rover',
        ],
        output='screen'
    )

    return LaunchDescription([
        env_var,
        model_arg,
        start_gazebo_server,
        start_gazebo_client,
        robot_state_publisher_node,
        spawn_robot
    ])