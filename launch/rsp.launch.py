from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import Command, PathJoinSubstitution, LaunchConfiguration
from launch_ros.substitutions import FindPackageShare
from launch.actions import DeclareLaunchArgument

def generate_launch_description():
    # 1. 声明 sim time 参数
    use_sim_time = LaunchConfiguration('use_sim_time')
    use_sim_time_arg = DeclareLaunchArgument(
        'use_sim_time',
        default_value='false',
        description='Use sim time if true'
    )

    # 2. 正确获取 xacro 文件路径
    pkg_name = 'my_bot'
    xacro_path = PathJoinSubstitution([
        FindPackageShare(pkg_name),
        'description',
        'robot_core.xacro'
    ])

    # 3. 用 Command 方式解析 xacro，避免格式问题
    robot_description = Command(['xacro ', xacro_path])

    # 4. 创建 robot_state_publisher 节点
    params = {
        'robot_description': robot_description,
        'use_sim_time': use_sim_time
    }
    rsp_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[params]
    )

    return LaunchDescription([
        use_sim_time_arg,
        rsp_node
    ])