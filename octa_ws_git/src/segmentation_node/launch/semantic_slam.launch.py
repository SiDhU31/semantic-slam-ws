from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='rtabmap_slam',
            executable='rtabmap',
            name='rtabmap',
            output='screen',
            parameters=[{
                'subscribe_depth': True,
                'subscribe_rgb': True,
                'subscribe_scan': False,
                'use_sim_time': True,
                'approx_sync': True,
                'approx_sync_max_interval': 1.0,
                'topic_queue_size': 30,
                'sync_queue_size': 30,
                'Grid/3D': 'True',
                'Grid/CellSize': '0.05',
                'filter_speckles': True,
                'occupancy_min_z': 0.1,
                'Grid/RangeMax': '5.0',
                'frame_id': 'base_link',
                'odom_frame_id': 'odom',
            }],
            remappings=[
                ('rgb/image', '/oakd/rgb/preview/image_raw'),
                ('rgb/camera_info', '/oakd/rgb/preview/camera_info'),
                ('depth/image', '/oakd/rgb/preview/depth'),
                ('odom', '/odom'),
            ]
        ),
        Node(
            package='octomap_server',
            executable='octomap_server_node',
            name='octomap_server',
            output='screen',
            parameters=[{
                'resolution': 0.05,
                'frame_id': 'map',
                'use_sim_time': True,
            }],
            remappings=[
                ('cloud_in', '/oakd/rgb/preview/depth/points'),
            ]
        ),
    ])
