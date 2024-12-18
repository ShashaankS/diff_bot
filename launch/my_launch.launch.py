import os
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, ExecuteProcess
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch.conditions import IfCondition
from ament_index_python.packages import get_package_share_directory
from launch_ros.actions import Node 

def generate_launch_description():
    
    pkg_name="diff_bot"
    world_name="test.sdf"
    
    # Path to robot description (URDF/Xacro)
    robot_description_file = os.path.join(
        get_package_share_directory(pkg_name),
        'description',
        'robot.urdf.xacro'
    )
    
    # Path to robot description (sdf)
    robot_description_sdf = os.path.join(
        get_package_share_directory(pkg_name),
        'description',
        'robot.sdf'
    )
    
    # Path to Gazebo world file
    world_file = os.path.join(
        get_package_share_directory(pkg_name),
        'worlds',
        world_name
    )

    # Node to publish the robot description to the parameter server
    rsp = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory(pkg_name),'launch','rsp.launch.py'
                )]), launch_arguments={'use_sim_time': 'true'}.items()
    )
    
    # Command to spawn the robot in Gazebo
    spawn_robot = ExecuteProcess(
        cmd=[
            'ros2', 'run', 'ros_gz_sim', 'create',
            '-world', 'default',
            '-name', 'diff_bot',
            '-file', robot_description_sdf,
        ],
        output='screen',
    )

    # Launch Gazebo Harmonic with the specified world
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory('ros_gz_sim'),
                'launch',
                'gz_sim.launch.py'
            )
        ),
        launch_arguments={'gz_args': f'-r {world_file}'}.items(),
    )
    
    rviz = Node(
       package='rviz2',
       executable='rviz2',
       arguments=['-d', os.path.join(get_package_share_directory(pkg_name), 'config', 'view_bot.rviz')],
    )
    
    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        parameters=[{
            'config_file': os.path.join(get_package_share_directory(pkg_name), 'config', 'bridge.yaml'),
            # 'qos_overrides./tf_static.publisher.durability': 'transient_local',
        }],
        output='screen'
    )

    return LaunchDescription([
        gazebo,
        rsp,
        spawn_robot,
        rviz,
        bridge
    ])
