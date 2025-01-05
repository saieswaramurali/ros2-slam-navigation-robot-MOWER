import launch
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch_ros.actions import Node
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    return LaunchDescription([
        # Declare the launch arguments for each parameter
        DeclareLaunchArgument('enable_gyro', default_value='true', description='Enable Gyroscope'),
        DeclareLaunchArgument('enable_accel', default_value='true', description='Enable Accelerometer'),
        DeclareLaunchArgument('enable_imu_unite', default_value='true', description='Enable IMU Unite'),
        DeclareLaunchArgument('unite_imu_method', default_value='2', description='[0-None, 1-copy, 2-linear_interpolation]'),

        # Include the realsense2_camera rs_launch.py launch file
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([
                FindPackageShare('realsense2_camera'), '/launch/rs_launch.py'
            ]),
            launch_arguments={
                'enable_gyro': launch.substitutions.LaunchConfiguration('enable_gyro'),
                'enable_accel': launch.substitutions.LaunchConfiguration('enable_accel'),
                'enable_imu_unite': launch.substitutions.LaunchConfiguration('enable_imu_unite'),
                'unite_imu_method': launch.substitutions.LaunchConfiguration('unite_imu_method'),
            }.items()
        ),

        Node(
            package='imu_filter_madgwick', executable='imu_filter_madgwick_node', output='screen',
            parameters=[{'use_mag': False, 
                         'world_frame':'enu', 
                         'publish_tf':False}],
            remappings=[('imu/data_raw', '/camera/camera/imu')]),

        Node(
            package='hexapod_step_detection',  # Replace with your package name
            executable='publish_gyro',  # Replace with your node name
            name='publish_gyro',
            output='screen',
            emulate_tty=True
        )  , 


    ])