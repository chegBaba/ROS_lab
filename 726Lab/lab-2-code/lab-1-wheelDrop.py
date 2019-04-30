
import roslib
import rospy
from kobuki_msgs.msg import WheelDropEvent

class lift_detection():

    def __init__(self):
        self.wheelLifted=[0,0]
        rospy.init_node("whell_monitor")
        rospy.Subscriber("/mobile_base/events/wheel_drop", WheelDropEvent, self.WheelDropEventCallback)
        print('I am starting')
        rospy.spin()

    def WheelDropEventCallback(self, data):
        print("Wheel:" + str(data.wheel) )
        print("State:" + str(data.state) )
	    self.wheelLifted[data.wheel]=data.state
        if(int(data.state) == 1):
            print("Where am i ?")
        if( self.wheelLifted[0] == 0 and self.wheelLifted[1] ==0):
            print("I am safe")
        print("------")


if __name__ == '__main__':
    try:
        lift_detection()
    except rospy.ROSInterruptException:
        rospy.loginfo("exception")
