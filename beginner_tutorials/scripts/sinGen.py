#!/usr/bin/env python

import rospy
from std_msgs.msg import Float32

def sinGen():
    pub = rospy.Publisher('chatter', Float32, queue_size=10)
    rospy.init_node('sinGen', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    sinStart = 0.00
    cntr = 0.01
    while not rospy.is_shutdown():
        datOut = sinStart
	sinStart = sinStart + cntr
	if(sinStart > 1.00):
		cntr = -0.01
	if(sinStart < -1.00):
		cntr = 0.01
        rospy.loginfo(datOut)
        pub.publish(datOut)
        rate.sleep()

if __name__ == '__main__':
    try:
        sinGen()
    except rospy.ROSInterruptException:
        pass
