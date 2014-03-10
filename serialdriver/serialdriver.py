# vi: spell spl=en
#

"""
Classes and functions for the train interface
"""

import serial
import logging
import os

class Train(object):
    """This class implements the interface to the relay driver
    used to signal the different train status signals.

    Each of the methods in this class can be used as a step
    in a test scenario.

    This class uses interface USB-RLY08 
    """

    def __init__(self, eventstore, train_id, debug=False ):
        device = '/dev/usbrly08_%d' % train_id
        self.debug = debug or os.environ.has_key('OTIS_DEBUG')
        self.eventstore = eventstore
        self.dev_id = train_id
        self.logger = logging.getLogger( 'otis_player.train%d' % train_id  )
        if not self.debug :
            self.serial = serial.Serial( device, 19200, parity='N',
                    stopbits=2, timeout=None, xonxoff=0, rtscts=0)

    def open_relay( self, relay_number ):
        """Open relay ``relay_number``
        """
        self.logger.info( 'open relay ' + str( relay_number ) )
        if not self.debug :
            command = 110
            command = command + relay_number
            self.serial.write( chr( command ) )

    def close_relay( self, relay_number ):
        """Close relay ``relay_number``
        """
        self.logger.info( 'close relay ' + str( relay_number ) )
        if not self.debug :
            command = 100
            command = command + relay_number
            self.serial.write( chr( command ) )

    def speed_over_5( self ):
        """Indicate the speed of the train is over 5km/h
        """
        self.open_relay( 4 )
        self.eventstore.store_status( self.dev_id, "speed", "moving" )

    def speed_under_5( self ):
        """Indicate the speed of the train is under 5km/h
        """
        self.close_relay( 4 )
        self.eventstore.store_status( self.dev_id, "speed", "stationary" )

    def left_door_enabled( self ):
        """Indicate the left doors are enabled
        """
        self.close_relay( 3 )
        self.eventstore.store_status( self.dev_id, "left door", "enabled" )

    def left_door_disabled( self ):
        """Indicate the left doors are disabled
        """
        self.open_relay( 3 )
        self.eventstore.store_status( self.dev_id, "left door", "disabled" )

    def right_door_enabled( self ):
        """Indicate the right doors are enabled
        """
        self.close_relay( 2 )
        self.eventstore.store_status( self.dev_id, "right door", "enabled" )

    def right_door_disabled( self ):
        """Indicate the right doors are disabled
        """
        self.open_relay( 2 )
        self.eventstore.store_status( self.dev_id, "right door", "disabled" )

    def pa_active( self ):
        """Indicate the PA system is active.
        """
        self.close_relay( 1 )
        self.eventstore.store_status( self.dev_id, "PA", "active" )

    def pa_inactive( self ):
        """Indicate the PA system is inactive.
        """
        self.open_relay( 1)
        self.eventstore.store_status( self.dev_id, "PA", "inactive" )


