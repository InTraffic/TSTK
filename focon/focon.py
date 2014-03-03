# vi: spell spl=en

"""Classes that implement the driver for the FOCON Simulator
"""

import logging
import zmq
import copy
# from focon_simulator.telegram import Telegram

class FOCON( object ):
    """Interface to the FOCON simulator
    """
    def __init__( self, event_store, zmq_context ):
        self.event_store = event_store
        self.logger = logging.getLogger( 'otis_player.focon' )
        self.message_link = zmq_context.socket( zmq.SUB )
        self.message_link.connect( "tcp://localhost:9002" )
        self.message_link.setsockopt( zmq.SUBSCRIBE, "" )

        self.command_link = zmq_context.socket( zmq.PUB )
        self.command_link.connect( "tcp://localhost:9001" )

        # Hash that maps a telegram ID to an array of callback
        # functions.
        self.callbacks = {}


    # The unused variable is scenario_player, needed because on_message
    # is a callback function with fixed parameters.
    # pylint: disable=W0613
    def on_message( self, scenario_player):
        """Receive a telegram from OBIS.
        """
        telegram = self.message_link.recv_pyobj()
        self.do_callbacks( telegram )


    def do_callbacks( self, telegram ):
        """Call all callbacks for this message.
        """
        if telegram.id_message in self.callbacks :
            # Have to operate on a copy because the callback functions
            # can modify the callback list.
            for function in copy.copy( self.callbacks[telegram.id_message] ):
                function( telegram )



    def set_callback( self, telegram_id, function ):
        """Install a callback function for a particular telegram.
        """
        if telegram_id in self.callbacks :
            self.callbacks[ telegram_id ].append( function )
        else:
            self.callbacks[ telegram_id ] = [ function ]


    def send( self, telegram ):
        """Send a telegram to OBIS.
        """
        self.command_link.send_pyobj( telegram )


#-----------------------------------------------------------------------

