import rospy
import cv2
from geometry_msgs.msg import Twist, Quaternion
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from nav_msgs.msg import Odometry
from tf.transformations import quaternion_from_euler
from sound_play.libsoundplay import SoundClient
import math
import sys

class PhotoTaker():
    def __init__(self):
        # initiliaze    
        rospy.init_node('PhotoTaker', anonymous=False)
        rospy.on_shutdown(self.shutdown)

        # tell user how to stop TurtleBot
        rospy.loginfo("To stop TurtleBot CTRL + C")

        #Rotation with position update
        # self.odom = rospy.Subscriber('/odom', Odometry, update_pose)
        self.sysInitAngle = 0
        self.targetAngle = 0
        self.isFirstRecord = True

        #Sound setup
        # print 'Sound setup'
        # self.soundhandle = SoundClient()
        # rospy.sleep(1)
        # self.voice = 'voice_kal_diphone'
        # self.volume = 1.0
        # self.s = 'Taking photo'

        #camera setup
        print 'Camera setup'
        self.bridge = CvBridge()
        self.image_received = False   
        self.img_title = rospy.get_param('~image_title', 'lab3Photo.jpg')     
        ## Connect image topic
        img_topic = "/camera/rgb/image_raw"
        self.image_sub = rospy.Subscriber(img_topic, Image, self.camera_callback)
        print 'set done'
        ## Allow up to one second to connection
        rospy.sleep(1)

        # Create a publisher which can "talk" to TurtleBot and tell it to move
        print 'Movement Twist() setup '
        self.cmd_vel = rospy.Publisher('/cmd_vel_mux/input/navi', Twist, queue_size=10)
        self.move_cmd = Twist()
        self.r = rospy.Rate(10)
        count = 0

        # tell user how to stop TurtleBot
        rospy.loginfo("To stop TurtleBot CTRL + C")
        count = 0

        # loop ten times, or until the user presses Ctrl-C
        while count < 10 and not rospy.is_shutdown():
            count += 1
            print 'Performing loop %d' % (count, )
            self.move_forward()

            # Wait for the robot to move into the correct position
            rospy.sleep(5)  
            self.make_sound()
            self.take_photo()
            if not rospy.is_shutdown():
                self.move_backwards()
                # Wait for the robot to move into the correct position
                rospy.sleep(5)  
                self.take_photo()

        rospy.loginfo('All done')

    def update_pose(self,msg):
        self.myAngle = msg.pose.pose.orientation.z
        if (isFirstRecord):
            self.sysInitAngle = self.myAngle
            isFirstRecord = False
        print 'current angle = %s'%self.myAngle

    def move_forward(self):
        print 'Moving forward'
        self.move_cmd.linear.x = 0.1
        self.move_cmd.angular.z = 0
        for i in range (1,10):
            self.r.sleep()
            self.cmd_vel.publish(self.move_cmd)

    def move_backwards(self):
        print 'Moving backwards'
        self.rotate_180Degree()
        self.move_cmd.linear.x = 0.1
        self.move_cmd.angular.z = 0
        for i in range (1,10):
            self.r.sleep()
            self.cmd_vel.publish(self.move_cmd)

    def rotate_180Degree(self):
        print 'Rotate 180 degree'
        # target_rad = target * math.pi /180
        self.move_cmd.linear.x = 0
        self.move_cmd.angular.z = 2
        for i in range (1,10):
            self.r.sleep()
            self.cmd_vel.publish(self.move_cmd)

    def make_sound(self):
        soundhandle = SoundClient()
        rospy.sleep(1)
        voice = 'voice_kal_diphone'
        volume = 1.0
        s = 'cheese'
        print 'Saying: %s' % s
        print 'Voice: %s' % voice
        print 'Volume: %s' % volume
        soundhandle.say(s, voice, volume)
        rospy.sleep(1)

    def take_photo(self):
        print 'Taking photo'
        if self.image_received:
            print 'image received'
            # Save an image
            cv2.imwrite(self.img_title, self.image)
            print 'image saved'
            return True
        else:
            return False

    def camera_callback(self, data):
        # Convert image to OpenCV format
        try:
            cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            print(e)
        self.image_received = True
        self.image = cv_image
        
                        
    def shutdown(self):
        # stop turtlebot
        rospy.loginfo("Stop TurtleBot")
	    
        # sleep just makes sure TurtleBot receives the stop command prior to shutting down the script
        rospy.sleep(1)
 
if __name__ == '__main__':
    try:
        PhotoTaker()
    except:
        rospy.loginfo("PhotoTaker node terminated.")
