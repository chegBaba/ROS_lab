import rospy
import sys
import cv2
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry

z = 0
def callback(msg):
    z= msg.pose.pose.orientation.z
    print z
    rospy.sleep(1)
    if z<=0.8
        rospy.spin()

# def init()
#     initAngle = 
rospy.init_node('check_odometry')
odom_sub = rospy.Subscriber('/odom', Odometry, callback)
while z <= 0.8:
    r=rospy.sleep(5)
    rospy.spin()