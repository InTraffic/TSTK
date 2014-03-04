#!/usr/bin/env python
# vi: spell spl=en

"""Message dispatcher.

This starts two threads that listen on two interfaces.
One to process requests from OBIS, the other to process
requests from the OTIS player.
"""

import zmq
import logging
import signal
import socket
import telegram


class Dispatcher( object ):

    """Dispatcher copies telegram back and forth between OBIS and the player,
    emulating the FOCON (PIAES) interface.
    """
    def __init__( self,  port=3020 ):
        self.go_on  = True
        self.logger = logging.getLogger( 'focon_simulator.dispatcher' )
        self.logger.info( "Dispatcher Started." )

        # ZeroMQ always needs a context
        self.context = zmq.Context(1)

        self.repeater_socket = None
        self.port            = port
        self.poller          = None
        self.call_backs      = {}
        self.old             = None
        self.obis_socket     = None


    def control_c_handler( self, unused1, unused2 ):
        """Controlled shutdown so we can cleanup.
        """
        self.go_on = False
        return False


    def create_sockets( self, focon_id ):
        """Create all sockets for communication between FOCON, OBIS and
        Player.
        """

        self.logger.info( "FOCON id " + str( focon_id ) )
        if focon_id == "0":
            accept_address = '192.168.6.10'
        else:
            accept_address = '172.31.6.10'

        # Open a tcp socket to listen for new connections from OBIS
        self.logger.info( "Listening on address " + str( accept_address ) )
        self.logger.info( "Listening on port "    + str( self.port ) )
        accept_socket = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
        accept_socket.bind( ( accept_address, self.port ) )
        # Only handle one connection at a time.
        accept_socket.listen(1)

        focon_id = int( focon_id )
        address = "tcp://*:900%d" % focon_id
        self.logger.info( "Command subscription at %s" % address )
        command_socket  = self.context.socket( zmq.SUB )
        command_socket.bind( address )
        command_socket.setsockopt( zmq.SUBSCRIBE, "" )

        self.poller = zmq.Poller()
        self.poller.register( accept_socket,  zmq.POLLIN )
        self.poller.register( command_socket, zmq.POLLIN )

        # Register the call backs.
        self.call_backs[ accept_socket.fileno() ] = ( 
                accept_socket, self.accept_connection )
        self.call_backs[ command_socket ]         = ( 
                command_socket, self.process_player_command )

        # Not part of the poller
        # Message forwarding link to player
        address = "tcp://*:900%d" % (focon_id + 1)
        self.logger.info( "Publishing on " + address )
        self.repeater_socket = self.context.socket( zmq.PUB )
        self.repeater_socket.bind( address )


    def accept_connection( self, a_socket ):
        """Accept an connection from OBIS.
        """
        obis_socket, address = a_socket.accept()
        self.logger.info( 'Connection from ' + str( address ) )
        # Register this socket too so we look for incoming data
        self.poller.register( obis_socket, zmq.POLLIN )
        self.call_backs[ obis_socket.fileno() ] = ( 
                obis_socket, self.process_obis_telegram )
        self.obis_socket = obis_socket


    def process_obis_telegram( self, a_socket ):
        """Receive and forward a telegram from OBIS.
        """
        self.logger.info( 'Data from OBIS' )
        # We do not know beforehand how big the blob is.
        data = a_socket.recv( 2048 )
        if data == "" :
            # Connection was closed, so unregister and close the socket.
            self.poller.unregister( a_socket )
            del self.call_backs[ a_socket.fileno() ]
            a_socket.close()
            self.obis_socket = None
        else :
            a_telegram = telegram.factory( blob = data )
            self.logger.info( 'Copying data to player' )
            self.repeater_socket.send_pyobj( a_telegram )


    def process_player_command( self, a_socket ):
        """Process a command or message from the player.
        """
        a_telegram = a_socket.recv_pyobj()
        self.obis_socket.send( a_telegram.to_blob() )


    def run( self, focon_id ):
        """Start the PIAES and command interface and wait for termination.

        """
        # Catch any Control-C
        self.old = signal.signal( signal.SIGINT, 
                                  self.control_c_handler )

        self.create_sockets( focon_id )
        while self.go_on :
            # Note that poller uses fileno() as the key for non-zmq sockets.
            socks = dict( self.poller.poll( 60000 ) ) # Timeout in ms, 1 minute
            for socket_key in self.call_backs.copy() : 
                    # Need copy here cause we might modify the call_backs
                    # while in the call back functions.
                if socket_key in socks and socks[ socket_key ] == zmq.POLLIN:
                    cbp = self.call_backs[ socket_key ]
                    function =  cbp[1]
                    function( cbp[0] )

            self.logger.info( "Still alive" )

        self.context.term()


#-----------------------------------------------------------------------------
if __name__ == '__main__':
    logger = logging.getLogger( 'focon_simulator' )
    logger.setLevel( logging.INFO )
    logfile = '/tmp/test.log'
    filehandler = logging.FileHandler( logfile )
    filehandler.setLevel( logging.INFO )
    formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    filehandler.setFormatter( formatter )
    logger.addHandler( filehandler )
    dispatcher = Dispatcher()
    dispatcher.run( '0' )

