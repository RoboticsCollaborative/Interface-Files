#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
    Wrapper call demonstrated:        ai_device.a_in()
    
    Purpose:                          Reads the user-specified A/D input channels
    
    Demonstration:                    Displays the analog input data for each of
                                      the user-specified channels using the first
                                      supported range and input mode
                                      
    Steps:
    1. Call get_daq_device_inventory() to get the list of available DAQ devices
    2. Create a DaqDevice object
    3. Call daq_device.get_ai_device() to get the ai_device object for the AI subsystem
    4. Verify the ai_device object is valid
    5. Call daq_device.connect() to establish a UL connection to the DAQ device
    6. Call ai_device.a_in() to read a value from an A/D input channel
    7. Display the data for each channel
    8. Call daq_device.disconnect() and daq_device.release() before exiting the process.
"""
from __future__ import print_function
from time import sleep
from os import system
from sys import stdout

from uldaq import (get_daq_device_inventory, DaqDevice, InterfaceType,
                   AiInputMode, AInFlag)

#ROS IMPORTS
import rospy
from std_msgs.msg import Float32
from std_msgs.msg import Float64MultiArray

import math



lastFinalOut1 = 0
lastFinalOut2 = 0


hTVal = 000
startCnt = 0
oVal1 = 0
oVal2 = 0
#gamma values are the difference between the original home value (oVal) and the new home theta value
gamma1 = 0
gamma2 = 0
val1 = 0
val2 = 0


def callbackHT(data):
    global hTVal
    hTVal = data.data
    print('New home value for theta set, signal id: ', hTVal)



def main():
    #ROS
    pub = rospy.Publisher('daq_pos_ref', Float64MultiArray, queue_size=10)
    rospy.init_node('glovereader', anonymous=True)
    rate = rospy.Rate(10) # 10hz

    rospy.Subscriber('gui_home', Float32, callbackHT)



    global lastFinalOut1
    global lastFinalOut2

    global hTVal
    global startCnt
    global oVal1
    global oVal2
    global gamma1
    global gamma2
    global val1
    global val2
    global finalOut1
    global finalOut2




    daq_device = None

    descriptor_index = 0
    range_index = 0
    interface_type = InterfaceType.USB
    low_channel = 0
    high_channel = 3

    try:
        # Get descriptors for all of the available DAQ devices.
        devices = get_daq_device_inventory(interface_type)
        number_of_devices = len(devices)
        if number_of_devices == 0:
            raise Exception('Error: No DAQ devices found')

        print('Found', number_of_devices, 'DAQ device(s):')
        for i in range(number_of_devices):
            print('  ', devices[i].product_name, ' (', devices[i].unique_id, ')', sep='')

        # Create the DAQ device object associated with the specified descriptor index.
        daq_device = DaqDevice(devices[descriptor_index])

        # Get the AiDevice object and verify that it is valid.
        ai_device = daq_device.get_ai_device()
        if ai_device is None:
            raise Exception('Error: The DAQ device does not support analog input')

        # Establish a connection to the DAQ device.
        descriptor = daq_device.get_descriptor()
        print('\nConnecting to', descriptor.dev_string, '- please wait...')
        daq_device.connect()

        ai_info = ai_device.get_info()

        # The default input mode is SINGLE_ENDED.
        input_mode = AiInputMode.SINGLE_ENDED
        # If SINGLE_ENDED input mode is not supported, set to DIFFERENTIAL.
        if ai_info.get_num_chans_by_mode(AiInputMode.SINGLE_ENDED) <= 0:
            input_mode = AiInputMode.DIFFERENTIAL

        # Get the number of channels and validate the high channel number.
        number_of_channels = ai_info.get_num_chans_by_mode(input_mode)
        if high_channel >= number_of_channels:
            high_channel = number_of_channels - 1

        # Get a list of supported ranges and validate the range index.
        ranges = ai_info.get_ranges(input_mode)
        if range_index >= len(ranges):
            range_index = len(ranges) - 1

        print('\n', descriptor.dev_string, ' ready', sep='')
        print('    Function demonstrated: ai_device.a_in()')
        print('    Channels: ', low_channel, '-', high_channel)
        print('    Input mode: ', input_mode.name)
        print('    Range: ', ranges[range_index].name)
        try:
            input('\nHit ENTER to continue\n')
        except (NameError, SyntaxError):
            pass

        system('clear')

        try:
            while True:
                try:
                    reset_cursor()
                    print('Please enter CTRL + Z to terminate the process\n')
                    # Display data for the specified analog input channels.
                    for channel in range(low_channel, high_channel + 1):
                        data = ai_device.a_in(channel, input_mode, ranges[range_index], AInFlag.DEFAULT)
                        print('Channel(', channel, ') Data: ', '{:.6f}'.format(data), sep='')
			if(channel == 0):
			    val1 = float('{:.6f}'.format(data))
			if(channel == 1):
			    val2 = float('{:.6f}'.format(data))
                    sleep(0.05)
                except (ValueError, NameError, SyntaxError):
                    break
		if(startCnt == 0):
		    oVal1 = val1
		    oVal2 = val2
		    startCnt = 1
		if(hTVal == 111):
		    gamma1 = val1 - oVal1
		    hTVal = 000
		    print('Reset theta 1 successfully')
		if(hTVal == 222):
		    gamma2 = val2 - oVal2
		    hTVal = 000
		    print('Reset theta 2 successfully')
		finalOut1 = (val1 - gamma1 - oVal1)
		finalOut2 = (val2 - gamma2 - oVal2)
		thetaVal1 = (finalOut1/5) * 360
		thetaVal2 = (finalOut2/5) * 360

		thetaVal = Float64MultiArray()
		thetaVal.data = [thetaVal1, thetaVal2]
		pub.publish(thetaVal)


		

		#Update values
		lastFinalOut1 = finalOut1
		lastFinalOut2 = finalOut2		

		print('The wrist angle is: ', thetaVal1)
		print('The finger angle is: ', thetaVal2)
        except KeyboardInterrupt:
            pass

    except Exception as e:
        print('\n', e)

    finally:
        if daq_device:
            if daq_device.is_connected():
                daq_device.disconnect()
            daq_device.release()


def reset_cursor():
    stdout.write('\033[1;1H')


if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
