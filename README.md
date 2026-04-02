## 3D Voxel Mapping with OCTA_Server for Autonomous navigation 

> multimodal semantic perception and autonomous navigation system for hospital robots.

![ROS2](https://img.shields.io/badge/ROS2-Humble-blue)
![Ubuntu](https://img.shields.io/badge/Ubuntu-22.04-orange)
![Python](https://img.shields.io/badge/Python-3.10-yellow)
![License](https://img.shields.io/badge/License-Apache%202.0-lightgrey)

---

## 📌 Overview

This ROS2 workspace implements **3D mapping** for an autonomous hospital robot. It combines:

- **RTAB-Map** RGB-D SLAM for real-time mapping and loop closure
- **OctoMap** for 3D occupancy voxel grid generation
- **DistanceColorNode** — a custom ROS2 node that colorizes the OctoMap point cloud by proximity (red=close, green=mid, purple=far) for intuitive visualization

---

## 🤖 Hardware/software

| Component | Spec |
|-----------|------|
| Robot | TurtleBot4 |
| Depth Camera | Intel RealSense D435i (replaces default OAK-D) |
| Host OS | Ubuntu 22.04 LTS |
| ROS2 | Humble |

---

## 📁 Repository Structure

```
semantic_slam_ws/
└── src/
    └── segmentation_node/          ← ROS2 Python package
        ├── segmentation_node/
        │   ├── __init__.py
        │   └── distance_color_node.py   ← Custom proximity colorizer node
        ├── launch/
        │   └── semantic_slam.launch.py  ← RTAB-Map + OctoMap launch
        ├── worlds/
        │   └── hospital.sdf             ← Custom Gazebo hospital world
        ├── test/
        ├── package.xml
        ├── setup.py
        └── setup.cfg
```

---

## 🚀 Quick Start

### 1. Build the workspace

```bash
cd ~/semantic_slam_ws
colcon build --symlink-install
source install/setup.bash
```

### 2. Launch RealSense camera

```bash
ros2 launch realsense2_camera rs_launch.py \
  depth_module.profile:=640x480x30 \
  pointcloud.enable:=true \
  align_depth.enable:=true
```

### 3. Launch RTAB-Map + OctoMap

```bash
ros2 launch segmentation_node semantic_slam.launch.py
```

### 4. Run Distance Color Node

```bash
ros2 run segmentation_node distance_color_node
```

Visualize `/octomap_distance_colored` in RViz2 as a PointCloud2 with RGB coloring.

---

## 🧠 DistanceColorNode

Subscribes to `/octomap_point_cloud_centers` (from OctoMap server) and publishes a distance-colored point cloud on `/octomap_distance_colored`.

**Color scheme:**
| Color | Meaning |
|-------|---------|
| 🔴 Red | Close obstacle (< ~0m) |
| 🟢 Green | Mid-range (~1m) |
| 🟣 Purple | Far / open space (~2m+) |

Uses **scipy cKDTree** for nearest-neighbor distance computation per point.

---

## 🌍 Hospital World (Gazebo)

A custom `hospital.sdf` Gazebo world is provided in `worlds/` for simulation testing. Features:
- Outer walls enclosing a hospital floor plan
- Directional sun lighting
- Ground plane

Load it in Gazebo:
```bash
gazebo src/segmentation_node/worlds/hospital.sdf
```

---

## ⚠️ Camera Topic Note

The launch file uses OAK-D topic remappings by default (`/oakd/rgb/preview/...`). If using **Intel RealSense D435i**, update the remappings in `semantic_slam.launch.py`:

```python
# Replace:
('rgb/image', '/oakd/rgb/preview/image_raw'),
# With:
('rgb/image', '/camera/camera/color/image_raw'),

# Replace:
('depth/image', '/oakd/rgb/preview/depth'),
# With:
('depth/image', '/camera/camera/depth/image_rect_raw'),
```

The `/camera/camera/` double namespace is expected behavior for the RealSense ROS2 wrapper.

---

## 👥 Team

| Role | Name |
|------|------|
| Developer | Sidharth Raj KR |
| Developer | Parwathe |


---

## 📄 License

Apache License 2.0
