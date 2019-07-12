#!/usr/bin/env python

import rospy
import math
from std_msgs.msg import Float32

handle = 0

theta0Pub = rospy.Publisher('theta0Pub', Float32, queue_size=10)
theta1Pub = rospy.Publisher('theta1Pub', Float32, queue_size=10)

def callback(data):
    global handle

    #Handler
    if (handle ==0):
	handle = 1
	theta0Pub.publish(data.data)
    else:
	handle = 0
	theta1Pub.publish(data.data)


def main():
    rospy.init_node('funcHandle', anonymous=True)
    rospy.Subscriber('daqChannel', Float32, callback)
    rospy.spin()


if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
