from setuptools import setup, find_packages
import os
from glob import glob

package_name = 'segmentation_node'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'),
            glob('launch/*.launch.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='sidharth',
    maintainer_email='sidharth@todo.todo',
    description='Segmentation node',
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
           'distance_color_node = segmentation_node.distance_color_node:main',
        ],
    },
)
