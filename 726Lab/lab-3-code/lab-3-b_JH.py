import rospy
import cv2
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Quaternion
from tf.transformations import quaternion_from_euler
from sound_play.libsoundplay import SoundClient
# from nav_msgs.msg import Odometry
import math
target = 180



class PhotoTaker():
    def __init__(self):
        # initiliaze
        rospy.init_node('PhotoTaker', anonymous=False)
        rospy.on_shutdown(self.shutdown)
        
        #Pose setup
        self.odom = rospy.Subscriber('/odom', Odometry, update_pose)
        #Sound setup
        print 'Sound setup'
        self.soundhandle = SoundClient()
        rospy.sleep(5)
        self.voice = 'voice_kal_diphone'
        self.volume = 0.8
        self.s = 'Taking photo'

        #camera setup
        print 'Camera setup'
        self.bridge = CvBridge()
        self.image_received = False        
        ## Connect image topic
        img_topic = "/camera/rgb/image_raw"
        
        self.image_sub = rospy.Subscriber(img_topic, Image, self.camera_callback)
        ## Allow up to one second to connection
        rospy.sleep(1)

        # Create a publisher which can "talk" to TurtleBot and tell it to move
        print 'Movement Twist() setup '
        self.cmd_vel = rospy.Publisher('/cmd_vel_mux/input/navi', Twist, queue_size=10)
        self.move_cmd = Twist()
        self.r = rospy.Rate(10)

        #prepare for rotation with quaternion
        #rotation 180 degree on z axis
        self.target_rotation = quaternion_from_euler(0, 0, math.pi)
        
        # tell user how to stop TurtleBot
        rospy.loginfo("To stop TurtleBot CTRL + C")
        count = 0

        # loop ten times, or until the user presses Ctrl-C
        while count < 10 and not rospy.is_shutdown():
            print 'Performing loop %d' % (count, )
            count += 1
            self.move_forward()

            # Wait for the robot to move into the correct position
            rospy.sleep(5)
            self.take_photo()
            self.rotate_180Degree()
            if not rospy.is_shutdown():
                # Wait for the robot to move into the correct position
                rospy.sleep(2)
                self.move_forward() # self.move_backwards()
                rospy.sleep(2)
                self.take_photo()

        rospy.loginfo('All done')

    def move_forward(self):
        r = rospy.Rate(10)
        # print 'Moving forward'
        print 'set moving forward,reset angular '
        self.move_cmd.linear.x = 0.2
        self.move_cmd.angular.z = 0
        for i in range (1,50):
            self.r.sleep()
            self.cmd_vel.publish(self.move_cmd)

    def take_photo(self, img_title):
        make_sound()
        print 'Taking photo'
        if self.image_received:
            print 'image received'
            # Save an image
            cv2.imwrite(img_title, self.image)
            print 'image saved'
            return True
        else:
            return False

    def rotate_180Degree(self):
        print 'Rotate 180 degree'
        target_rad = target * math.pi /180
        angular_spd = 2
        self.move_cmd.linear.x = 0
        self.move_cmd.angular.z = angular_spd
        #while the desired pose is not achieved, keep spin
        # while self.myPose.[]:
            # rospy.spin()
       
       
        # for i in range(1,20):
        #     self.r.sleep()
        #     self.cmd_vel.publish(self.move_cmd)

    def camera_callback(self, data):
        # Convert image to OpenCV format
        try:
            cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            print(e)
        self.image_received = True
        self.image = cv_image

    def make_sound(self):
        print 'Saying: %s' %self.s 
        print 'Voice: ' %self.voice 
        print 'Volume:%s' %self.volume
        soundhandle.say(s,voice,volume)
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
            print 'my angle=%s'%self.myAngle
            print 'target_rd=%s'%self.target_rd
        # print 'Odom read: %s'  %myPose
        # print 'my position:%s' %myPosition
        # print 'my orientation:%s' %myOrientation
        # print 'my angle:%s' %self.myAngle
        print '--------------------------------'
            
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
