import rclpy
from rclpy.node import Node
from nav_msgs.msg import OccupancyGrid
from std_msgs.msg import Header
import numpy as np

class SimpleOccupancyMapPublisher(Node):
    def __init__(self):
        super().__init__('simple_occupancy_map_publisher')
        self.publisher_ = self.create_publisher(OccupancyGrid, 'map', 10)
        timer_period = 2.0  # Publish every 2 seconds
        self.timer = self.create_timer(timer_period, self.publish_occupancy_grid)

    def publish_occupancy_grid(self):
        # Create a simple 10x10 grid map
        map_msg = OccupancyGrid()
        map_msg.header = Header()
        map_msg.header.stamp = self.get_clock().now().to_msg()
        map_msg.header.frame_id = "map"

        map_msg.info.resolution = 0.1  # 10cm per grid cell
        map_msg.info.width = 10
        map_msg.info.height = 10
        map_msg.info.origin.position.x = 0.0
        map_msg.info.origin.position.y = 0.0
        map_msg.info.origin.position.z = 0.0

        # Fill the grid with random occupancy values (0 for free, 100 for occupied)
        grid_data = np.random.choice([0, 100], size=(100,)).tolist()
        map_msg.data = grid_data

        self.publisher_.publish(map_msg)
        self.get_logger().info('Publishing occupancy grid')

def main(args=None):
    rclpy.init(args=args)
    node = SimpleOccupancyMapPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
