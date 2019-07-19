#!/usr/bin/env python

import rospy
import math
from std_msgs.msg import Float32

handle = 0

sinPub = rospy.Publisher('sinPub', Float32, queue_size=10)
cosPub = rospy.Publisher('cosPub', Float32, queue_size=10)

def callback(data):
    global handle

    #Handler
    if (handle ==0):
	handle = 1
	sinPub.publish(data.data)
    else:
	handle = 0
	cosPub.publish(data.data)


def main():
    rospy.init_node('funcHandle', anonymous=True)
    rospy.Subscriber('daqChannel', Float32, callback)
    rospy.spin()


if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
