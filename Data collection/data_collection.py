#!/usr/bin/env python3

import rospy
import csv
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
import time
from math import atan2

class TurtlebotController:
    def __init__(self):
        self.vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        self.odom_sub = rospy.Subscriber('/odom', Odometry, self.odom_callback)
        self.cmd_vel = Twist()
        self.current_state = [0, 0, 0, 0, 0]  # Initialize state with [x, y, theta, v, omega]
        self.start_time = time.time()  # Using Python's time() function to get the real time
        self.file_writer = csv.writer(open('data_3.csv', 'w', newline=''))
        self.file_writer.writerow(['time', 'commanded_linear', 'commanded_angular', 'x_actual', 'y_actual', 'theta_actual', 'v_actual', 'omega_actual'])

    def odom_callback(self, msg):
        # Extract state from the odometry message
        x_actual = msg.pose.pose.position.x
        y_actual = msg.pose.pose.position.y
        theta_actual = 2 * atan2(msg.pose.pose.orientation.z, msg.pose.pose.orientation.w)
        v_actual = msg.twist.twist.linear.x
        omega_actual = msg.twist.twist.angular.z
        self.current_state = [x_actual, y_actual, theta_actual, v_actual, omega_actual]

    def command_velocity(self):
        rate = rospy.Rate(100)  # 100 Hz for more data points
        maneuvers = [(0, 0, 5), (0.26, 1.82, 10), (0, 0, 5), (0.2, 0.5, 10), (0, 1.82, 10), (0, 0, 3), (0.26, -1.4, 5), (0, 0, 3),(0.26,0,5)]
        for vel_linear, vel_angular, duration in maneuvers:
            end_time = time.time() + duration
            while not rospy.is_shutdown() and time.time() < end_time:
                self.cmd_vel.linear.x = vel_linear
                self.cmd_vel.angular.z = vel_angular
                self.vel_pub.publish(self.cmd_vel)
                self.file_writer.writerow([time.time() - self.start_time, self.cmd_vel.linear.x, self.cmd_vel.angular.z, *self.current_state])
                rate.sleep()


        self.cmd_vel.linear.x = 0
        self.cmd_vel.angular.z = 0
        self.vel_pub.publish(self.cmd_vel)

if __name__ == '__main__':
    rospy.init_node('turtlebot_controller')
    controller = TurtlebotController()
    controller.command_velocity()
