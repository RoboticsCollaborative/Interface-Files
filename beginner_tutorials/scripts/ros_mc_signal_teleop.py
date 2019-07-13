#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from __future__ import print_function
from time import sleep
from os import system
from sys import stdout

from uldaq import (get_daq_device_inventory, DaqDevice, AInScanFlag, ScanStatus,
                   ScanOption, create_float_buffer, InterfaceType, AiInputMode, AOutFlag)

#ROS IMPORTS
import rospy
from std_msgs.msg import Float32

import math



vOutVal = 1
hTVal = 000
startCnt = 0
oVal1 = 0
oVal2 = 0
#gamma values are the difference between the original home value (oVal) and the new home theta value
gamma1 = 0
gamma2 = 0



def callbackVOut(data):
    global vOutVal
    vOutVal = data.data

def callbackHT(data):
    global hTVal
    hTVal = data.data
    


def main():
    #ROS
    pub = rospy.Publisher('daqChannel', Float32, queue_size=10)
    rospy.init_node('daqSinGenRead', anonymous=True)
    rate = rospy.Rate(10) # 10hz

    rospy.Subscriber('daqVOut', Float32, callbackVOut)
    rospy.Subscriber('daqHT', Float32, callbackHT)


    global startCnt
    global oVal1
    global oVal2
    global gamma1
    global gamma2



    interface_type = InterfaceType.USB
    output_channel0 = 0
    output_channel1 = 1
    daq_device = None
    ai_device = None
    status = ScanStatus.IDLE

    descriptor_index = 0
    range_index = 0
    interface_type = InterfaceType.USB
    low_channel = 0
    high_channel = 3
    samples_per_channel = 10000
    rate = 1000
    scan_options = ScanOption.CONTINUOUS
    flags = AInScanFlag.DEFAULT

    try:
        # Get descriptors for all of the available DAQ devices.
        devices = get_daq_device_inventory(interface_type)
        number_of_devices = len(devices)

        ## Verify at least one DAQ device is detected.
        if number_of_devices == 0:
            raise Exception('Error: No DAQ device is detected')
        print('Found', number_of_devices, 'DAQ device(s):')
        for i in range(number_of_devices):
            print('    ', devices[i].product_name, ' (', devices[i].unique_id, ')', sep='')

        # Create the DAQ device object associated with the specified descriptor index.
        daq_device = DaqDevice(devices[descriptor_index])
        ao_device = daq_device.get_ao_device()

        # Get the AiDevice object and verify that it is valid.
        ai_device = daq_device.get_ai_device()
        if ai_device is None:
            raise Exception('Error: The DAQ device does not support analog input')
        # Verify that the specified device supports hardware pacing for analog input.
        ai_info = ai_device.get_info()
        if not ai_info.has_pacer():
            raise Exception('\nError: The specified DAQ device does not support hardware paced analog input')

	##
	ao_info = ao_device.get_info()
        output_range = ao_info.get_ranges()[0]  # Select the first supported range.



        ## Verify the specified DAQ device supports analog output.
        if ao_device is None:
            raise Exception('Error: The DAQ device does not support analog output')

        ### Establish a connection to the DAQ device.
        descriptor = daq_device.get_descriptor()
        print('\nConnecting to', descriptor.dev_string, '- please wait...')
        daq_device.connect()

        # The default input mode is SINGLE_ENDED.
        input_mode = AiInputMode.SINGLE_ENDED
        # If SINGLE_ENDED input mode is not supported, set to DIFFERENTIAL.
        if ai_info.get_num_chans_by_mode(AiInputMode.SINGLE_ENDED) <= 0:
            input_mode = AiInputMode.DIFFERENTIAL

        # Get the number of channels and validate the high channel number.
        number_of_channels = ai_info.get_num_chans_by_mode(input_mode)
        if high_channel >= number_of_channels:
            high_channel = number_of_channels - 1
        channel_count = high_channel - low_channel + 1

        # Get a list of supported ranges and validate the range index.
        ranges = ai_info.get_ranges(input_mode)
        if range_index >= len(ranges):
            range_index = len(ranges) - 1

        # Allocate a buffer to receive the data.
        data = create_float_buffer(channel_count, samples_per_channel)


	##
	print('\n', descriptor.dev_string, 'ready')
        print('    Function demonstrated: AoDevice.a_out')
        print('    Channel:', output_channel0)
        print('    Range:', output_range.name)

	#
        print('\n', descriptor.dev_string, ' ready', sep='')
        print('    Function demonstrated: ai_device.a_in_scan()')
        print('    Channels: ', low_channel, '-', high_channel)
        print('    Input mode: ', input_mode.name)
        print('    Range: ', ranges[range_index - 1].name)
        print('    Samples per channel: ', samples_per_channel)
        print('    Rate: ', rate, 'Hz')
        print('    Scan options:', display_scan_options(scan_options))
        try:
            input('\nHit ENTER to continue\n')
        except (NameError, SyntaxError):
            pass

        system('clear')

	# Start the acquisition.
        rate = ai_device.a_in_scan(low_channel, high_channel, input_mode, ranges[range_index], samples_per_channel, rate, scan_options, flags, data)

        try:
            while True:
                try:
		    #(ampVal/10) current amplitude to maximum amplitude
                    out_val0 = (2.5*(math.sin(t)+1))*(ampVal/10)
		    out_val1 = (2.5*(math.cos(t)+1))*(ampVal/10)
                    ao_device.a_out(output_channel0, output_range, AOutFlag.DEFAULT, float(out_val0))
                    ao_device.a_out(output_channel1, output_range, AOutFlag.DEFAULT, float(out_val1))

 		    # Get the status of the background operation
                    status, transfer_status = ai_device.get_scan_status()

                    reset_cursor()
                    print('Please enter CTRL + Z to kill\n')

                    print('actual scan rate = ', '{:.6f}'.format(rate), 'Hz\n')

                    index = transfer_status.current_index
                    print('currentTotalCount = ',  transfer_status.current_total_count)
                    print('currentScanCount = ',  transfer_status.current_scan_count)
                    print('currentIndex = ',  index, '\n')

                    # Display the data.
                    for i in range(channel_count):
                        clear_eol()
                        print('chan =',
                          i + low_channel, ': ',
                          '{:.6f}'.format(data[index + i]))
		    if(startCnt == 0):
			oVal1 = data[index]
			oVal2 = data[index + 1]
			startCnt = 1
		    if(hTVal == 111):
		        gamma1 = data[index] - oVal1
			hTVal = 000
		    if(hTVal == 222):
			gamma2 = data[index + 1] - oVal2
			hTVal = 000
		    newVal1 = data[index] + gamma1
		    newVal2 = data[index + 1] + gamma2
		    pub.publish(data[index] + gamma1)
		    pub.publish(data[index + 1] + gamma2)
                    sleep(0.05)
                except (ValueError, NameError, SyntaxError):
                    break
        except KeyboardInterrupt:
            pass

    except Exception as e:
        print('\n', e)


    finally:
        if daq_device:
            # Stop the acquisition if it is still running.
            if status == ScanStatus.RUNNING:
                ai_device.scan_stop()
            if daq_device.is_connected():
                daq_device.disconnect()
            daq_device.release()


def display_scan_options(bit_mask):
    options = []
    if bit_mask == ScanOption.DEFAULTIO:
        options.append(ScanOption.DEFAULTIO.name)
    for so in ScanOption:
        if so & bit_mask:
            options.append(so.name)
    return ', '.join(options)


def reset_cursor():
    stdout.write('\033[1;1H')


def clear_eol():
    stdout.write('\x1b[2K')


if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
