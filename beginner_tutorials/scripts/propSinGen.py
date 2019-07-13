#!/usr/bin/env python

import rospy
import math
from std_msgs.msg import Float32

def propSinGen():
    pub = rospy.Publisher('chatter', Float32, queue_size=10)
    rospy.init_node('propSinGen', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
	t = rospy.get_time()
        datOut = math.sin(t)
        rospy.loginfo(datOut)
        pub.publish(datOut)
        rate.sleep()

if __name__ == '__main__':
    try:
        propSinGen()
    except rospy.ROSInterruptException:
        pass
