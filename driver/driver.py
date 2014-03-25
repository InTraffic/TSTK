import urllib  # This does all the heavy lifting.
import logging


class Portal(object):
    """Interface to a web portal
    
    """

    def __init__(self, portal_id = None,):
        self.logger     = logging.getLogger('portal-driver-{0}'
                                            .format(portal_id))
        self.portal_url = None

    def fetch(self, portal_url=None):
        """Fetch the current version of the web portal.

        :param portal_url: the url to fetch, this url will be remembered
                           untill the next call with a portal_url 
                           specified.
        :type portal_url: string
        :returns: The fetched web portal if an url is known or specified
        :returns: 1 if no url is known or specified

        """
        if portal_url is not None:
            self.portal_url = portal_url
        elif self.portal_url is not None:
            url_file = urllib.urlopen(self.portal_url)
            content = url_file.read()
            url_file.close()
            self.logger.info("fetched page " + content)
            return content
        else:
            self.logger.error("no portal_url given (yet)")
            return 1

#------------------------------------------------------------------------------
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

    def open_relay(self, relay_number):
        """Open relay 

        :param relay_number: The number of the relay to open
        :type relay_number: int
        """
        if not self.debug :
            command = 110
            command = command + relay_number
            self.serial.write( chr( command ) )

    def close_relay(self, relay_number):
        """Close relay 

        :param relay_number: The number of the relay to close
        :type relay_number: int
        """
        if not self.debug :
            command = 100
            command = command + relay_number
            self.serial.write( chr( command ) )
#------------------------------------------------------------------------------

def get_driver(name, driver_id):
    """ function to get the desired driver object from this module.

    :param name: name of the driver (eg. portal or usbrly08b)
    :type name: string
    :param driver_id: The id for the driver
    :type driver_id: int
    """
    drivers = {"portal":Portal, "usbrly08b":Usbrly08b} 
    a_driver = drivers.get(name)(driver_id)
    return a_driver



