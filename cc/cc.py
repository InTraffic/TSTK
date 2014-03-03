# vi: spell spl=en

"""Classes for the driver for the CC Simulator
"""

import logging
import copy
import zmq
from cc_simulator.message import message_type_string


class CC( object ):
    """Interface to the CC Simulator
    """
    def __init__( self, event_store, zmq_context ):
        self.event_store = event_store
        self.logger = logging.getLogger( 'otis_player.cc' )

        # TODO should depend on driver id
        self.message_link = zmq_context.socket( zmq.SUB )
        address = "tcp://localhost:9101"
        self.message_link.connect( address )
        self.message_link.setsockopt( zmq.SUBSCRIBE, "" )
        self.logger.info( 'Subscribing to ' + address )

        address = "tcp://localhost:9100"
        self.command_link = zmq_context.socket( zmq.PUB )
        # TODO should depend on driver id
        self.command_link.connect( address )
        self.logger.info( 'Publishing on ' + address )

        # Hash that maps a message ID to an array of callback
        # functions.
        self.callbacks = {}
        self.dev_id    = None

    # The unused variable is scenario_player, needed because on_message
    # is a callback function with fixed parameters.
    # pylint: disable=W0613
    def on_message( self, a_socket, scenario_player):
        """Receive a message from OBIS
        """
        a_message = self.message_link.recv_pyobj()
        self.logger.info( 
                "Received a message (type %d) from OBIS" % a_message.msg_type )
        self.do_callbacks( a_message )
        self.event_store.store_cc( self.dev_id, 'in', 
                message_type_string[ a_message.msg_type ] )

    def do_callbacks( self, a_message ):
        """Call all callbacks for this message.
        """
        if a_message.msg_type in self.callbacks :
            # Have to operate on a copy because the callback functions
            # can modify the callback list.
            for function in copy.copy( self.callbacks[ a_message.msg_type ] ) :
                self.logger.info( "Executing callback" )
                function( a_message )
        else :
            self.logger.info( "No callbacks for this message" )

    def set_callback( self, message_id, function ):
        """Install a callback function for a particular message.

        The given function is called as soon as a message with the given
        message_id is received.
        The function should take a single parameter, when called
        it will contain the message received.
        """
        if message_id in self.callbacks :
            self.callbacks[ message_id ].append( function )
        else:
            self.callbacks[ message_id ] = [ function ]

    def remove_callback( self, message_id, function ):
        """Remove an already installed callback function.
        """
        if message_id in self.callbacks :
            self.callbacks[ message_id ].remove( function )

    def send( self, a_message ):
        """Send a message to OBIS
        """
        self.command_link.send_pyobj( a_message )
        self.event_store.store_cc( self.dev_id, 'out', 
                message_type_string[ a_message.msg_type ] )



