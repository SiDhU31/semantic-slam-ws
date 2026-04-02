import rclpy
from rclpy.node import Node
from sensor_msgs.msg import PointCloud2, PointField
import sensor_msgs_py.point_cloud2 as pc2
import numpy as np

class DistanceColorNode(Node):
    def __init__(self):
        super().__init__('distance_color_node')
        self.sub = self.create_subscription(
            PointCloud2,
            '/octomap_point_cloud_centers',
            self.callback, 10)
        self.pub = self.create_publisher(
            PointCloud2,
            '/octomap_distance_colored',
            10)
        self.get_logger().info('Distance Color Node Started!')

    def callback(self, msg):
        points = list(pc2.read_points(msg, field_names=('x','y','z'), skip_nans=True))
        if not points:
            return

        pts = np.array(points, dtype=np.float32)
        if len(pts) == 0:
            return

        # Compute distance from each point to nearest neighbor
        from scipy.spatial import cKDTree
        tree = cKDTree(pts)
        distances, _ = tree.query(pts, k=2)
        dist = distances[:, 1]

        # Normalize distances
        max_dist = 2.0
        dist_norm = np.clip(dist / max_dist, 0, 1)

        # Color: purple=far, green=mid, red=close
        r = (dist_norm * 255).astype(np.uint8)
        g = ((1 - abs(dist_norm - 0.5) * 2) * 255).astype(np.uint8)
        b = ((1 - dist_norm) * 255).astype(np.uint8)
        rgb = (r.astype(np.uint32) << 16 |
               g.astype(np.uint32) << 8 |
               b.astype(np.uint32))
        rgb_float = rgb.view(np.float32)

        colored_points = np.column_stack([pts, rgb_float])

        fields = [
            PointField(name='x', offset=0, datatype=PointField.FLOAT32, count=1),
            PointField(name='y', offset=4, datatype=PointField.FLOAT32, count=1),
            PointField(name='z', offset=8, datatype=PointField.FLOAT32, count=1),
            PointField(name='rgb', offset=12, datatype=PointField.FLOAT32, count=1),
        ]

        out_msg = pc2.create_cloud(msg.header, fields, colored_points)
        self.pub.publish(out_msg)

def main(args=None):
    rclpy.init(args=args)
    node = DistanceColorNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
