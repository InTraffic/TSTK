# vi: spell spl=en
#

"""
Classes and functions to interact with a serial interface
"""

import serial
import os

class Usbrly08b(object):
    """This class is an interface to the USB-RLY08 serial device.
    
    This class can be use directly through the open_relay and close_relay 
    methods. It is recommended to use this class as a superclass for an 
    implementation of a more descriptive subclass in a project. This'll allow 
    for the addition of logging and better understandable methods and/or
    functions.

    """

    def __init__( self, eventstore, train_id, debug=False ):
        device = '/dev/usbrly08_%d' % train_id
        self.debug = debug
        self.eventstore = eventstore
        self.dev_id = train_id
        
        if not self.debug :
            self.serial = serial.Serial( device, 19200, parity='N',
                    stopbits=2, timeout=None, xonxoff=0, rtscts=0)

    def open_relay( self, relay_number ):
        """Open relay ``relay_number``
        """
        if not self.debug :
            command = 110
            command = command + relay_number
            self.serial.write( chr( command ) )

    def close_relay( self, relay_number ):
        """Close relay ``relay_number``
        """
        if not self.debug :
            command = 100
            command = command + relay_number
            self.serial.write( chr( command ) )

