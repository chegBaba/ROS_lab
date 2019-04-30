"""
robot will keep going forward until it's bumper has been pressed
Then the robot will start rotate untill the bumper is released
"""


import rospy
from geometry_msgs.msg import Twist
#import bumper event
from kobuki_msgs.msg import BumperEvent



class GoForward():
    def __init__(self):
        # initiliaze
        rospy.init_node('Run_Hit', anonymous=False)

        #Store the bumper press status
        self.keepGoing = True
        #Subscribe to bumper press event
        print("Now subscribe")
        rospy.Subscriber("/mobile_base/events/bumper", BumperEvent, self.BumperPressedEventCallback)
        # tell user how to stop TurtleBot
        rospy.loginfo("To stop TurtleBot CTRL + C")

        # What function to call when you ctrl + c    
        rospy.on_shutdown(self.shutdown)
        
	    # Create a publisher which can "talk" to TurtleBot and tell it to move
        self.cmd_vel = rospy.Publisher('/cmd_vel_mux/input/navi', Twist, queue_size=10)
     
	    #TurtleBot will stop if we don't keep telling it to move.  How often should we tell it to move? 10 HZ
        r = rospy.Rate(10);

        # Twist is a datatype for velocity
        move_cmd = Twist()

	    # let's go forward at 0.2 m/s
        move_cmd.linear.x = 0.1

        # as long as you haven't ctrl + c keeping doing...
        while not rospy.is_shutdown():
            move_cmd.linear.x = 0 if not self.keepGoing else 0.1
            #make robot turn if bumper pressed
            move_cmd.angular.z = 0.8 if not self.keepGoing else 0

            # publish the velocity
            self.cmd_vel.publish(move_cmd)
            # wait for 0.1 seconds (10 HZ) and publish again
            r.sleep()
                        
    # PauseForward():
    def BumperPressedEventCallback(self, data):
            print("Bumper:" + str(data.bumper) + "State:" + str(data.state) )
            self.keepGoing = False if data.state else True


    def shutdown(self):
        # stop turtlebot
        rospy.loginfo("Stop TurtleBot")
	    # a default Twist has linear.x of 0 and angular.z of 0.  So it'll stop TurtleBot
        self.cmd_vel.publish(Twist())
	    # sleep just makes sure TurtleBot receives the stop command prior to shutting down the script
        rospy.sleep(1)
 
if __name__ == '__main__':
    try:
        GoForward()
    except:
        rospy.loginfo("GoForward node terminated.")
