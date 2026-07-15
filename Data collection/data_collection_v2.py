#!/usr/bin/env python3

import rospy
import csv
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
import time

class TurtlebotController:
    def __init__(self):
        self.vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        self.odom_sub = rospy.Subscriber('/odom', Odometry, self.odom_callback)
        self.cmd_vel = Twist()
        self.current_vel = [0, 0]
        self.start_time = time.time() # Using Python's time() function to get the real time
        self.file_writer = csv.writer(open('vnew_data.csv', 'w', newline=''))
        self.file_writer.writerow(['time', 'commanded_linear', 'commanded_angular', 'actual_linear', 'actual_angular'])

    def odom_callback(self, msg):
        # Extract linear velocity from the odometry message
        actual_linear = msg.twist.twist.linear.x
        actual_angular = msg.twist.twist.angular.z
        self.current_vel = [actual_linear, actual_angular]

    def command_velocity(self):
        rate = rospy.Rate(10)  # 10 Hz
        maneuvers = [(0, 0, 3),(0.26, 1.82, 7), (0, 0, 3), (0.2, 0.5, 8), (0, 1.82, 6), (0, 0, 2), (0.26, -1.4, 7), (0, 0, 2),(0.26, 0, 6),(0,0,2)]
        for vel_linear, vel_angular, duration in maneuvers:
            end_time = time.time() + duration # Using Python's time() function to get the real time
            while not rospy.is_shutdown() and time.time() < end_time:
                self.cmd_vel.linear.x = vel_linear
                self.cmd_vel.angular.z = vel_angular
                self.vel_pub.publish(self.cmd_vel)
                self.file_writer.writerow([time.time() - self.start_time, self.cmd_vel.linear.x, self.cmd_vel.angular.z, *self.current_vel])
                rate.sleep()

        # Stop the robot after all maneuvers are done
        self.cmd_vel.linear.x = 0
        self.cmd_vel.angular.z = 0
        self.vel_pub.publish(self.cmd_vel)

if __name__ == '__main__':
    rospy.init_node('turtlebot_controller')
    controller = TurtlebotController()
    controller.command_velocity()
