#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
    UL call demonstrated:             AoDevice.a_out()

    Purpose:                          Writes to a D/A output channel

    Demonstration:                    Outputs a user-specified voltage
                                      on analog output channel 0

    Steps:
    1. Call get_daq_device_inventory() to get the list of available DAQ devices
    2. Call DaqDevice() to create a DaqDevice object
    3. Call DaqDevice.get_ao_device() to get the AoDevice object for the analog output subsystem
    4. Verify the AoDevice object is valid
    5. Call DaqDevice.connect() to connect to the device
    6. Enter a value to output for the D/A channel
    7. Call AoDevice.a_out() to write a value to a D/A output channel
    8. Call DaqDevice.disconnect() and DaqDevice.release() before exiting the process
"""
from __future__ import print_function
from sys import stdout
from os import system

from uldaq import get_daq_device_inventory, DaqDevice, InterfaceType, AOutFlag

# Constants
CURSOR_UP = '\x1b[1A'
ERASE_LINE = '\x1b[2K'


def main():
    interface_type = InterfaceType.USB
    output_channel = 0
    daq_device = None

    try:
        # Get descriptors for all of the available DAQ devices.
        devices = get_daq_device_inventory(interface_type)
        number_of_devices = len(devices)

        # Verify at least one DAQ device is detected.
        if number_of_devices == 0:
            raise Exception('Error: No DAQ device is detected')

        print('Found', number_of_devices, 'DAQ device(s):')
        for i in range(number_of_devices):
            print('    ', devices[i].product_name, ' (', devices[i].unique_id, ')', sep='')

        # Create a DaqDevice object from the first descriptor.
        daq_device = DaqDevice(devices[0])
        ao_device = daq_device.get_ao_device()

        # Verify the specified DAQ device supports analog output.
        if ao_device is None:
            raise Exception('Error: The DAQ device does not support analog output')

        descriptor = daq_device.get_descriptor()
        print('\nConnecting to', descriptor.dev_string, '- please wait...')
        # Establish a connection to the device.
        daq_device.connect()

        ao_info = ao_device.get_info()
        output_range = ao_info.get_ranges()[0]  # Select the first supported range.

        print('\n', descriptor.dev_string, 'ready')
        print('    Function demonstrated: AoDevice.a_out')
        print('    Channel:', output_channel)
        print('    Range:', output_range.name)
        try:
            input('\nHit ENTER to continue')
        except (NameError, SyntaxError):
            pass

        system('clear')
        print('\n*Enter non-numeric value to exit')
        try:
            while True:
                try:
                    # Get and set a user specified output value.
                    out_val = input('    Enter output value (V): ')
                    ao_device.a_out(output_channel, output_range, AOutFlag.DEFAULT, float(out_val))
                    # Clear the previous input request before the next input request.
                    stdout.write(CURSOR_UP + ERASE_LINE)
                except (ValueError, NameError, SyntaxError):
                    break
        except KeyboardInterrupt:
            pass

    except Exception as e:
        print('\n', e)

    finally:
        if daq_device:
            # Disconnect from the DAQ device.
            if daq_device.is_connected():
                daq_device.disconnect()
            # Release the DAQ device resource.
            daq_device.release()


if __name__ == '__main__':
    main()
