
"""Classes and functions to get pages from a web portal.
"""

import urllib2  # This does all the heavy lifting.
import logging


class Portal(object):
    """Interface to a Webportal
    """

    def __init__(self, portal_id = None,):
        config = configparser.ConfigParser()
        config.read('driver.conf')
        portal_section = ('driver-portal-{1}'.format(portal_id))
        self.portal_url = portal_section['portalUrl']
        self.logger     = logging.getLogger('portal-driver-{0}'
                                            .format(portal_id))

    def fetch(self):
        """Fetch the current version of the portal page"""
        url_file = urllib2.urlopen(self.portal_url)
        content = url_file.read()
        url_file.close()
        self.logger.info("fetched page " + content)
        return content

#------------------------------------------------------------------------------
import configparser
import serial
import os

class Usbrly08b(object):
    """This class is an interface to the USB-RLY08 serial device.
    
    This class can be use directly through the open_relay and 
    close_relay methods. It is recommended to use this class as a 
    superclass for an implementation of a more descriptive subclass in 
    a project. This'll allow for the addition of logging and better 
    understandable methods and/or functions.

    Attributes:
    device_id -- the id of the usbrly08b board to communicate with.
    debug -- whether or not this module is to run in a debugging mode.
    """

    def __init__( self, device_id, debug=False ):
        """ Initialize the usbrly08b class.
        
        Arguments: 
        device_id -- Used to specify which usbrly device should be 
                     interacted with, because more than one can be 
                     attached to a system at a time.
        debug -- Use to specify if it should be run in debug mode. The 
                 serial interface will not be initialized and the 
                 methods will not try to send commands if debug mode is
                 activated.

        The '/dev/usbrly08' in the device variable is a link created by
        a udev rule.       
        """
        device = '/dev/usbrly08_{0}'.format(device_id)
        self.debug = debug
        self.dev_id = device_id
        
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
#------------------------------------------------------------------------------

def get_driver(name, driver_id):
    drivers = {"portal":Portal, "usbrly08b":Usbrly08b} 
    a_driver = drivers.get(name)(driver_id)
    return a_driver



