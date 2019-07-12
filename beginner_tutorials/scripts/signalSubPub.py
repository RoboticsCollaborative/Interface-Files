#!/usr/bin/env python

import rospy
import math
from std_msgs.msg import Float32

signalOut = 0
pub = rospy.Publisher('/funcOut', Float32, queue_size=10)
rate = rospy.Rate(10) # 10hz

def callback(data):
    global signalOut
    global rate
    rospy.loginfo(data.data)

    if (data.data == 001):
        while not rospy.is_shutdown():
		t = rospy.get_time()
		signalOut = math.sin(t)
		rospy.loginfo(signalOut)
		pub.publish(signalOut)
		rate.sleep()


def checker():
    rospy.init_node('signalSubPub', anonymous=True)
    rospy.Subscriber('/signalTopic', Float32, callback)
    # Initial movement.
    pub.publish(Float32(signalOut))
    rospy.spin()


if __name__ == '__main__':
    try:
        checker()
    except rospy.ROSInterruptException:
        pass
