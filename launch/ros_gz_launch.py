import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.substitutions import LaunchConfiguration
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
    # Path to the Gazebo world file
    world_file = os.path.join(
        get_package_share_directory('diff_bot'),
        'worlds',
        'test.sdf'
    )

    # Gazebo Sim (Harmonic)
    gazebo_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [os.path.join(
                get_package_share_directory('ros_gz_sim'),
                'launch',
                'gz_sim.launch.py'
            )]
        ),
        launch_arguments={
            'gz_args': f'-r {world_file}'
        }.items(),
    )

    return LaunchDescription([
        DeclareLaunchArgument(
            'world',
            default_value=world_file,
            description='world/test.sdf'
        ),
        gazebo_sim,
    ])
