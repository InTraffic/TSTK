import socket
import logging
import copy
import zmq


class SoapNotification(object):
    """
    Handle message from the Soap Driver
    """
    def __init__(self, eventstore, zmq_context):
        self.eventstore = eventstore
        self.logger = logging.getLogger('otis_player.soap_notif')
        address = 'tcp://localhost:9500'
        self.message_link = zmq_context.socket( zmq.SUB )
        self.message_link.connect(address)
        self.message_link.setsockopt(zmq.SUBSCRIBE, "")
        self.logger.info("Subscribing to " + address)
        self.callbacks = {}

    def on_message(self, a_socket, scenario_player):
        a_message = self.message_link.recv_pyobj()
        self.logger.info(
                "Received a message (type {}) from Otis_soap".format( 
                    a_message.msg_type))
        self.do_callbacks( a_message )


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
        message_id is received.  The function should take a single parameter,
        when called it will contain the message received.
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


