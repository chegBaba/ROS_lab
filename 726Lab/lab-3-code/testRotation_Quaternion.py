
import sys
import rospy
import cv2
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Quaternion
from tf.transformations import quaternion_from_euler
from sound_play.libsoundplay import SoundClient
import math

target = 180


class MakeRotation():
    def __init__(self):
        print 'INIT'
        self.firstRecord = True
        # rospy.on_shutdown(self.shutdown)
        print 'subscriber'
        self.odom = rospy.Subscriber('/odom',Odometry, self.update_pose)
        rospy.sleep(1)

        # Create a publisher which can "talk" to TurtleBot and tell it to move
        print 'Movement Twist() setup '
        self.cmd_vel = rospy.Publisher('/cmd_vel_mux/input/navi', Twist, queue_size=10)
        self.move_cmd = Twist()
        self.r = rospy.Rate(10)

        # self.target_rd = target *math.pi /180  
        angular_spd = 2
        # print 'target_rd:%s' %self.target_rd
        while round(self.myAngle,2) != self.target_rd:
            self.move_cmd.angular.z = angular_spd
            self.cmd_vel.publish(self.move_cmd)
            self.r.sleep()
        move_cmd.angular.z = 0
        cmd_vel.publish(move_cmd)

        
        rospy.loginfo("To stop TurtleBot CTRL + C")

        rospy.sleep(1)


    def update_pose(self, msg):
        # print 'update_pose\n'
        print '----------update_pose----------'
        myPosition = msg.pose.pose.position
        myOrientation = msg.pose.pose.orientation
        self.myAngle = myOrientation.z
        if self.firstRecord:
            self.target_rd = round((self.myAngle + target *math.pi /180  ),2)
            self.firstRecord = False
            print 'set target_rd to %s' %self.target_rd
        # print 'Odom read: %s'  %myPose
        # print 'my position:%s' %myPosition
        print 'my orientation:%s' %myOrientation
        print 'my angle:%s' %self.myAngle
        print '--------------------------------'

if __name__ == '__main__':
    rospy.init_node('MakeRotation',anonymous = False)
    rotation = MakeRotation()
    try:
        MakeRotation()
    except:
        rospy.loginfo("MakeRotation node terminiated.")