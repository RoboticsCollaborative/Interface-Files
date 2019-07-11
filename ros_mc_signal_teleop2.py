#!/usr/bin/env python
# -*- coding: UTF-8 -*-



################################################################################################
################################################################################################
##											      ##
##                    Wrapper call demonstrated:        ai_device.a_in()		      ##
##    											      ##
##       Purpose:                          Reads the user-specified A/D input channels        ##
##    											      ##
##       Demonstration:                    Displays the analog input data for each of	      ##
##                                         the user-specified channels using the first        ##
##                                         supported range and input mode		      ##
##                                      						      ##
##    Steps:										      ##
##    1. Call get_daq_device_inventory() to get the list of available DAQ devices	      ##
##    2. Create a DaqDevice object							      ##
##    3. Call daq_device.get_ai_device() to get the ai_device object for the AI subsystem     ##
##    4. Verify the ai_device object is valid						      ##
##    5. Call daq_device.connect() to establish a UL connection to the DAQ device	      ##
##    6. Call ai_device.a_in() to read a value from an A/D input channel		      ##
##    7. Display the data for each channel						      ##
##    8. Call daq_device.disconnect() and daq_device.release() before exiting the process.    ##
##											      ##
################################################################################################
################################################################################################



#Main imports
from __future__ import print_function
from time import sleep
from os import system
from sys import stdout
#DAQ imports
from uldaq import (get_daq_device_inventory, DaqDevice, InterfaceType, AiInputMode, AInFlag)
#ROS imports
import rospy
from std_msgs.msg import Float32
from std_msgs.msg import Float64MultiArray
#Additional imports
import math

from rdda_interface.msg import JointCommands
from rdda_interface.msg import JointStates



#Instantiate global variables
#previous run
lastFinalOut1 = 0
lastFinalOut2 = 0
#Home reset signal
hTVal = 000
#Start count to void instantiated values of zero
startCnt = 0
#Value outputs of DAQ in volts (0-5 volts) => (0-360 degrees)
#Original value for reference to original frame (keeps reset value logic coherent)
oVal1 = 0
oVal2 = 0
#Output value in volts after adjusted for a custom reference frame (after home reset signal)
val1 = 0
val2 = 0
#Gamma values are the difference between the original home value (oVal) and the new home theta value
#Gamme is used to calculate val1 and val2 from oVal1 and oVal2
gamma1 = 0
gamma2 = 0
#Theta values to be printed in next loop iteration (1 iteration data delay)
thetaVal1 = 0
thetaVal2 = 0






####################################
#    Home Reset Callback Method    #
####################################
def callbackHT(data):
    global hTVal
    hTVal = data.data







######################################
#    Main Data Acquisition Method    #
######################################
def main():
    #Create ROS publisher
    #Initiate node
    #Create rate object for sleep
    pub = rospy.Publisher('daq_pos_ref', Float64MultiArray, queue_size=10)
    rospy.init_node('glovereader', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    #Crate ROS subscriber to catch home reset signals
    rospy.Subscriber('gui_home', Float32, callbackHT)

    joint_pub = rospy.Publisher("rdd/joint_cmds", JointCommands, queue_size=1)
    joint_sub = rospy.Subscriber("rdd/joint_stats", JointStates, callbackHT)

    #Declare global variables as global
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
    global thetaVal1
    global thetaVal2

    #Configure DAQ device
    daq_device = None
    descriptor_index = 0
    range_index = 0
    interface_type = InterfaceType.USB
    low_channel = 0
    high_channel = 3

    #Find and confirm DAQ device
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
	#Confirm DAQ information
        print('\n', descriptor.dev_string, ' ready', sep='')
        print('    Function demonstrated: ai_device.a_in()')
        print('    Channels: ', low_channel, '-', high_channel)
        print('    Input mode: ', input_mode.name)
        print('    Range: ', ranges[range_index].name)
	#Catch enter statement
        try:
            input('\nHit ENTER to continue\n')
        except (NameError, SyntaxError):
            pass
	#Refresh feed
        system('clear')
#######################################################################################
#######################################################################################
#######################################################################################
	#Start data collection
        try:
            while True:
                try:
                    reset_cursor()
                    print('Please enter CTRL + Z to terminate the process\n')
                    # Display data for the specified analog input channels.
                    for channel in range(low_channel, high_channel + 1):
                        data = ai_device.a_in(channel, input_mode, ranges[range_index], AInFlag.DEFAULT)
                        print('Channel(', channel, ') Data: ', '{:.6f}'.format(data), sep='')
			#Store input values
			if(channel == 0):
			    val1 = float('{:.6f}'.format(data))
			if(channel == 1):
			    val2 = float('{:.6f}'.format(data))
		    print('')
		    #Print final theta output from last loop iteration
		    print('The wrist angle is: ', thetaVal1)
		    print('The finger angle is: ', thetaVal2)
		    #ROS sleep
                    rate.sleep()
                except (ValueError, NameError, SyntaxError):
                    break
		#Check for turn counter to make sure variables are instantiated with valid values
		if(startCnt == 0):
		    oVal1 = val1
		    oVal2 = val2
		    gamma1 = val1 - oVal1
		    gamma2 = val2 - oVal2
		    startCnt = 1
		#Check home reset signals
		if(hTVal == 111):
		    gamma1 = val1 - oVal1
		    hTVal = 000
		if(hTVal == 222):
		    gamma2 = val2 - oVal2
		    hTVal = 000
		#Create final variables accounting for reference frames
		finalOut1 = (val1 - gamma1 - oVal1)
		finalOut2 = (val2 - gamma2 - oVal2)
		#Convert final variables to degrees (6.28 = 360degrees * (~0.175 radians/degree)) 
		thetaVal1 = (finalOut1/5) * 6.28
		thetaVal2 = (finalOut2/5) * 6.28
		#Update last values for next loop run
		lastFinalOut1 = finalOut1
		lastFinalOut2 = finalOut2
		#Create multiarray with theta values and publish to ROS
		if(thetaVal1 > 1):
		    thetaVal1 = 1
		if(thetaVal1 < -1):
		    thetaVal1 = -1
		if(thetaVal2 > 1):
		    thetaVal2 = 1
		if(thetaVal2 < -1):
		    thetaVal2 = -1
		thetaVal = Float64MultiArray()
		thetaVal.data = [thetaVal1, thetaVal2]
		pub.publish(thetaVal)		
    #Catch errors on loop intervals
        except KeyboardInterrupt:
            pass
    except Exception as e:
        print('\n', e)
    finally:
        if daq_device:
            if daq_device.is_connected():
                daq_device.disconnect()
            daq_device.release()







#############################
#    Cursor Reset Method    #
#############################
def reset_cursor():
    stdout.write('\033[1;1H')



#####################
#####################
#####    MAIN   #####
#####################
#####################
if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
