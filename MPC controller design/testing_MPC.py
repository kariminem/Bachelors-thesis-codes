#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from gazebo_msgs.srv import SetModelState, SetModelStateRequest
from MPC import mpc_controller
import numpy as np


rospy.init_node('turtlebot3_mpc', anonymous=True)


pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)


x_current = np.zeros(5)

def state_callback(msg):
    global x_current
    x_current[0] = msg.pose.pose.position.x
    x_current[1] = msg.pose.pose.position.y
    x_current[2] = 2 * np.arctan2(msg.pose.pose.orientation.z, msg.pose.pose.orientation.w)  # Convert quaternion to euler
    x_current[3] = msg.twist.twist.linear.x
    x_current[4] = msg.twist.twist.angular.z

# Subscriber for the current state of the robot
rospy.Subscriber('/odom', Odometry, state_callback)


rospy.wait_for_service('/gazebo/set_model_state')


try:
    rate = rospy.Rate(10)  # 10 Hz
    while not rospy.is_shutdown():
        # Calculate control command
        u = mpc_controller(x_current)


        cmd = Twist()
        cmd.linear.x = u[0]
        cmd.angular.z = u[1]

        # Publish command
        pub.publish(cmd)

        rate.sleep()

except rospy.ROSInterruptException:
    pass

except KeyboardInterrupt:
    # Stop the robot
    cmd = Twist()
    pub.publish(cmd)
