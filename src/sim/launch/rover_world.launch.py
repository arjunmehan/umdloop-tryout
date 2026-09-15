import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, SetEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import EnvironmentVariable

from launch_ros.actions import Node


def generate_launch_description():
    sim_share = get_package_share_directory('sim')
    ros_gz_sim_share = get_package_share_directory('ros_gz_sim')
    models_path = os.path.join(sim_share, 'models')
    world_path = os.path.join(models_path, 'world.sdf')
    bridge_config = os.path.join(sim_share, 'config', 'bridge.yaml')

    resource_path = SetEnvironmentVariable(
        name='GZ_SIM_RESOURCE_PATH',
        value=[
            models_path,
            os.pathsep,
            EnvironmentVariable('GZ_SIM_RESOURCE_PATH', default_value=''),
        ],
    )

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(ros_gz_sim_share, 'launch', 'gz_sim.launch.py')
        ),
        launch_arguments={'gz_args': ['-r ', world_path]}.items(),
    )

    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        name='ros_gz_bridge',
        output='screen',
        parameters=[{'config_file': bridge_config}],
    )

    return LaunchDescription([
        resource_path,
        gazebo,
        bridge,
    ])
