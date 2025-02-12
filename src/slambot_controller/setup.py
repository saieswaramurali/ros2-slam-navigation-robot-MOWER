import os
import glob
from setuptools import find_packages, setup

package_name = 'slambot_controller'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob.glob('launch/*.launch.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='saieswaram',
    maintainer_email='saieswaram@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'joystick_mapper = slambot_controller.joystick_controller:main',
            'serial_transmitter = slambot_controller.serial_transmitter:main',
        ],
    },
)
