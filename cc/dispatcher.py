#!/usr/bin/env python
# vi: spell spl=en

"""Message dispatcher.

This starts two threads that listen on two interfaces.  One to process
requests from OBIS, the other to process requests from the OTIS player.
"""

import zmq
import logging
import signal
import seriall
from message import request_factory

default_timeout = 60000

class Dispatcher( object ):

    """Forward messages between OBIS and the player.
    """
    def __init__( self ):
        self.go_on  = True
        self.logger = logging.getLogger( 'cc_simulator.dispatcher' )

        # ZeroMQ always needs a context
        self.context = zmq.Context(1)

        self.repeater_socket = None
        self.poller          = None
        self.call_backs      = {}
        self.obis_handle     = None
        self.timeout         = default_timeout

        # In the process of getting a message from OBIS
        self.receiving       = False
        self.blob            = ""


    def control_c_handler( self, unused1, unused2 ):
        """Controlled shutdown so we can cleanup.
        """
        self.go_on = False


    def create_sockets_and_handles( self, cc_id, debug ):
        """Create all sockets for communication between CC, OBIS and
        Player.
        """
        # We talk with OBIS over a serial link
        cc_id = int( cc_id )
        if debug :
            self.logger.info( 'running in debug mode' )
            self.logger.info( 
                    'will NOT read or write data from/to serial port' )
        else :
            device = '/dev/ccser%d' % cc_id
            self.logger.info( 'opening serial device ' + device )
            # According to the spec 57.6 baud, 8 data bits, 1 stopbit, no
            # parity
            self.obis_handle = serial.Serial( 
                    device, 57600, 
                    parity=serial.PARITY_NONE,
                    bytesize=8,
                    stopbits=serial.STOPBITS_ONE
                    )
            # Make it non blocking so we can use select (poll) on it.
            # self.obis_handle.nonblocking()


        # Command link from player
        address = "tcp://*:910%d" % cc_id
        self.logger.info( "Command subscription on " + address )
        command_socket  = self.context.socket( zmq.SUB )
        command_socket.bind( address )
        command_socket.setsockopt( zmq.SUBSCRIBE, "" )

        self.poller = zmq.Poller()
        if ( self.obis_handle ) :
            self.poller.register( self.obis_handle,  zmq.POLLIN )
            # Register the call backs.
            self.call_backs[ self.obis_handle.fileno() ] = ( 
                    self.obis_handle, self.read_obis_message )
        self.poller.register( command_socket, zmq.POLLIN )

        # Register the call backs.
        self.call_backs[ command_socket ]         = ( 
                command_socket, self.process_player_command )

        # Not part of the poller
        # Message forwarding link to player
        # Command link from player
        address = "tcp://*:910%d" % ( cc_id + 1 )
        self.logger.info( "Publishing on "  + address )
        self.repeater_socket = self.context.socket( zmq.PUB )
        self.repeater_socket.bind( address )


    def read_obis_message( self, handle ):
        """Read one or more bytes from OBIS
        """
        # We do not know beforehand how big the blob is and data might come in
        # parts, mostly one character at a time, sometimes a few more.
        blob = handle.read()
        self.blob += blob
        # Set timeout to a low value.  We should receive a new byte within
        # this period otherwise we assume it is the end of the message.  If we
        # make this too high, there will be a delay in processing the message.
        # The baud rate is 57600 so a single character takes
        # 8/57600 == 0.000138 seconds == 0.138 milliseconds
        # So 10ms should be enough.
        self.timeout = 10    # in ms
        self.receiving = True

    def process_obis_message( self ):
        """Receive and forward a message from OBIS.
        """
        self.logger.info( 'Received a full message from OBIS' )
        self.logger.info( ",".join( map( lambda x: hex(ord(x)), self.blob ) ) )
        message = request_factory( self.blob )
        self.logger.info( 'Copying data to player' )
        self.repeater_socket.send_pyobj( message )

        self.blob = ""


    def process_player_command( self, socket ):
        """Process message from the player.
        """
        message = socket.recv_pyobj()
        self.logger.info( 'Received message from player' + str(type(message)) )
        blob = message.to_blob() 
        self.logger.info( ",".join( map( lambda x: hex(ord(x)), blob ) ) )
        self.obis_handle.write( blob )

    def run( self, cc_id, debug=False ):
        """Start the CC and command interface and wait for termination.

        This is an infinite loop that passes messages back and forth
        between OBIS and the player.
        The messages are handled by call-back functions.
        """
        # Catch any Control-C
        signal.signal( signal.SIGINT, self.control_c_handler )

        self.create_sockets_and_handles( cc_id, debug )

        while self.go_on :
            # Note that poller uses fileno() as the key for non-zmq sockets.
            socks = dict( self.poller.poll( self.timeout ) ) # Timeout in ms
            for socket_key in self.call_backs.copy() : 
                    # Need a copy here cause we might modify the call_backs
                    # while in the call back functions.
                if socket_key in socks and socks[ socket_key ] == zmq.POLLIN:
                    cbp = self.call_backs[ socket_key ]
                    function = cbp[1]
                    function( cbp[0] )

            if len( socks ) == 0 and self.receiving :
                # We were in the process of receiving data from OBIS.
                # We did not receive any new bytes, so we assume it's
                # the end of the message.
                self.process_obis_message()
                self.receiving = False

                # Set timeout back to a high value, so we not waste CPU
                # cycles.
                self.timeout = default_timeout
                self.blob = "" # Reset the message buffer
            elif len( socks ) == 0 and self.timeout == default_timeout :
                self.logger.info( "Nothing happened for a long time." )
            else :
                pass

        self.logger.info( 'Stopping' )
        self.context.term()


#-----------------------------------------------------------------------------
if __name__ == '__main__':
    logger = logging.getLogger( 'cc_simulator' )
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

