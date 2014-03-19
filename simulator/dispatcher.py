import logging
import signal
import socket
import configparser
import importlib.machinery
import serial

import zmq

class Dispatcher(object):
    def __init__(self, dispatcher_type, dispatcher_id):
        self.name = name
        self.dispatcher_id = dispatcher_id
        self.call_backs = {}
        self.forwarder = False
        self.go_on = True

        logger = logging.getLogger('{0}_simulator'
                                        .format(dispatcher_type))
        logger.setLevel(logging.INFO)
        logfile = '/tmp/test.log'
        filehandler = logging.FileHandler(logfile)
        filehandler.setLevel(logging.INFO)
        formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        filehandler.setFormatter(formatter)
        logger.addHandler(filehandler)
        self.logger = logger
        
        self.context = zmq.Context(1)

    def control_c_handler():
        """Controlled shutdown so we can cleanup."""
        self.go_on = False
        return False

    def create_sockets(self):
        # Open a socket to listen for commands from the scenario player
        address = "tcp://*:{0}".format(self.command_listen_port)
        self.logger.info( "Command subscription at {0}".format(address)
        command_socket  = self.context.socket(zmq.SUB)
        command_socket.bind(address)
        command_socket.setsockopt(zmq.SUBSCRIBE, "")
        
        # Add the sockets to the zmq poller.
        self.poller = zmq.Poller()
        self.poller.register(accept_socket,  zmq.POLLIN)
        self.poller.register(command_socket, zmq.POLLIN)

        # Register the call backs.
        self.call_backs[accept_socket.fileno()] = (accept_socket, self.accept)
        self.call_backs[command_socket] = (command_socket, 
                                           self.process_player_command)

        # Not part of the poller
        # Message forwarding link to player
        address = "tcp://*:{0}".format(self.message_forward_port)
        self.logger.info("Publishing on " + address)
        self.repeater_socket = self.context.socket(zmq.PUB)
        self.repeater_socket.bind(address)
    
    def accept(self, a_socket):
        """Accept a connection from the system.
        """
        system_socket, address = a_socket.accept()
        self.logger.info('Connection from ' + str(address))
        # Register this socket too so we look for incoming data
        self.poller.register(system_socket, zmq.POLLIN)
        self.call_backs[system_socket.fileno()] = (
                system_socket, self.process_message)
        self.system_socket = system_socket

    def process_player_command(self, a_socket):
        """ Process a command from the scenario player.
        """
        # receive the command
        command = a_socket.recv_pyobj()
        self.logger.info('received command from scenario player: {0}'
                         .format(type(command)))
        self.system_socket.send(self.message.to_message(command))
    
    def process_message(self, a_socket):
        """ Receive and forward a message from the system """
        self.logger.info( 'Data from the system' )
        # We do not know beforehand how big the blob is.
        data = a_socket.recv( 2048 )
        if data == "" :
            # Connection was closed, so unregister and close the socket.
            self.poller.unregister(a_socket)
            del self.call_backs[a_socket.fileno()]
            a_socket.close()
            self.system_socket = None
        else :
            a_message = message.from_message(blob = data)
            self.logger.info('Copying data to player')
            self.repeater_socket.send_pyobj(a_message)
    
    def run(self):
        # Catch any Control-C
        signal.signal(signal.SIGINT, self.control_c_handler)
        self.create_sockets()
        
        while self.go_on :
            # Note that poller uses fileno() as the key for non-zmq sockets.
            socks = dict(self.poller.poll(60000)) # Timeout in ms, 1 minute
            for socket_key in self.call_backs.copy() : 
                    # Need copy here cause we might modify the call_backs
                    # while in the call back functions.
                if socket_key in socks and socks[socket_key] == zmq.POLLIN:
                    if socket_key in self.call_backs: #TODO The forwarder stuff could fit here as extra if statement.
                        cbp = self.call_backs[socket_key]
                        function =  cbp[1]
                        function(cbp[0])

            self.logger.info("Still alive")
            self.run(socks)
        self.logger.info("Stopping")
        self.context.term()

#------------------------------------------------------------------------------

class TCPDispatcher(Dispatcher):
    def __init__(self, dispatcher_type, dispatcher_id):
        Dispatcher.__init__(self, name, dispatcher_id)
        
        config = configparser.ConfigParser()
        config.read('dispatcher.conf')
        dispatcher_section = ('dispatcher-{0}-{1}'
                                  .format(dispatcher_type, dispatcher_id))

        if (dispatcher_section) in config.sections()):
            entries = config[dispatcher_section]
            # path to the message class
            self.message_path = entries['MessagePath']
            if message_path is not None:
                loader = importlib.machinery.SourceFileLoader('message',
                                                              message_path)
                message_module = loader.exec_module('message')
                message = message_module.Message()
            # address and port to listen on for messages from the system
            self.accept_address = entries['AcceptAddress']
            self.listen_port = entries['ListenPort']
            
            # Is the dispatcher supposed to forward to another system
            # instead of to the scenario player.
            self.forwarder = (entries['Forwarder'].lower() in ['true', '1',
                                                               'yes'])
            # check to see if messages should be forwarded to another 
            # system
            if forwarder:
                self.second_accept_address = entries['SecondAcceptAddress']
            else:
                # port to listen on for commands from the player.
                self.command_listen_port = entries['CommandListenPort']
                # port to forward messages to the player.
                self.message_forward_port = entries['MessageForwardPort']
                        
        else:
            self.logger.critical('no valid tcp section found in config file')
            
    def create_sockets(self):
        """ Create the TCP sockets between the system and the 
            Scenario player
        """
        self.logger.info('Creating sockets for {0} {1}'
                         .format(self.name, self.dispatcher_id))
        # Open a tcp socket to listen for new connections 
        # from the system.
        self.logger.info("Listening on address {0}"
                         .format(str(self.accept_address)))
        self.logger.info("Listening on port {0}".format(str(self.listen_port)))
        accept_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        accept_socket.bind((self.accept_address, self.port))        
        # Only handle one connection at a time.
        accept_socket.listen(1)

        # Let the superclass finish the creation of the rest of the 
        # sockets, because it is the same.
        Dispatcher.create_sockets(self)

    def run(self):
        # TCP dispatcher has no extra steps to add to the default loop.
        # We will just exit this method.
        pass

#------------------------------------------------------------------------------


class SerialDispatcher(Dispatcher):
    SERIAL_PARITY = {'none':serial.PARITY_NONE , 'even':serial.PARITY_EVEN ,
                     'odd':serial.PARITY_ODD , 'mark':serial.PARITY_MARK , 
                     'space':serial.PARITY_SPACE}
    SERIAL_STOPBITS= {'one':serial.STOPBITS_ONE , 
                      'onePointFive': serial.STOPBITS_ONE_POINT_FIVE, 
                      'two':serial.STOPBITS_TWO }
    default_timeout = 60000

    def __init__(self, dispatcher_type, dispatcher_id):
        Dispatcher.__init__(self, dispatcher_type, dispatcher_id)
        
        self.repeater_socket = None
        self.poller = None
        self.call_backs = None
        self.serial_link = None
        self.timeout = default_timeout
        
        self.receiving = False
        self.blob = ""
        
        config = configparser.ConfigParser()
        config.read('dispatcher.conf')
        dispatcher_section = ('dispatcher-{0}-{1}'
                                  .format(dispatcher_type, dispatcher_id))

        if (dispatcher_section) in config.sections()):
            entries = config[dispatcher_section]
            # path to the message class
            self.message_path = entries['MessagePath']
            if message_path is not None:
                loader = importlib.machinery.SourceFileLoader('message',
                                                              message_path)
                message_module = loader.exec_module('message')
                message = message_module.Message()
            # Settings for the serial link to the system.
            self.serial_device = entries['Device']
            self.serial_baudrate = int(entries['BaudRate'])
            self.serial_bytesize = int(entries['ByteSize']) 
            self.serial_parity = SERIAL_PARITY.get(entries['Parity'])
            self.serial_stopbits = SERIAL_STOPBITS.get(entries['StopBits'])

            # port to listen on for commands from the player.
            self.command_listen_port = entries['CommandListenPort']
            # port to forward messages to the player.
            self.message_forward_port = entries['MessageForwardPort']
                        
        else:
            self.logger.critical('no valid serial section '
                                 'found in config file')

    def create_sockets(self):
        """ Create the socket to the scenario player and set up the
            serial link to the system
        """
        self.logger.info('Creating sockets for {0} {1}'
                         .format(self.name, self.dispatcher_id))
        # Setup a serial link to listen to the system 
        self.logger.info("Opening serial device {0} ".format(serial_device))
        self.serial_link = serial.Serial(serial_device, serial_baudrate,
                                         serial_parity, serial_bytesize,
                                         serial_stopbits)
        
        # Open a socket to listen for commands from the scenario player
        address = "tcp://*:{0}".format(self.command_listen_port)
        self.logger.info( "Command subscription at {0}".format(address)
        command_socket  = self.context.socket(zmq.SUB)
        command_socket.bind(address)
        command_socket.setsockopt(zmq.SUBSCRIBE, "")
        
        # Add the sockets to the zmq poller.
        self.poller = zmq.Poller()

        if(self.serial_link):
            self.poller.register(self.serial_link, zmq_POLLIN)
            # Register callback
            self.call_backs[self.serial_link.fileno()] = (self.serial_link, 
                                                          self.read_message)
        self.poller.register(command_socket, zmq.POLLIN)

        # Register the call backs.
        self.call_backs[command_socket] = (command_socket, 
                                           self.process_player_command)

        # Not part of the poller
        # Message forwarding link to player
        address = "tcp://*:{0}".format(self.message_forward_port)
        self.logger.info("Publishing on " + address)
        self.repeater_socket = self.context.socket(zmq.PUB)
        self.repeater_socket.bind(address)

    def read_message(self, link):
        """Read one or more bytes from the system
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
    
    def process_message(self):
        """Receive and forward a message from the system.
        """
        self.logger.info('Received a full message from the system')
        self.logger.info(",".join(map(lambda x: hex(ord(x)), self.blob)))
        a_message = self.message.from_message( self.blob )
        self.logger.info('Copying data to player')
        self.repeater_socket.send_pyobj(a_message)

        self.blob = ""
    
    def process_player_command(self, a_socket):
        """ Process a command from the scenario player.
        """
        # receive the command
        command = a_socket.recv_pyobj()
        self.logger.info('received command from scenario player: {0}'
                         .format(type(command)))
        self.serial_link.write(self.message.to_message(command))

    def run(self, socks):
        if len(socks) == 0 and self.receiving :
                # We were in the process of receiving data from OBIS.
                # We did not receive any new bytes, so we assume it's
                # the end of the message.
                self.process_message()
                self.receiving = False

                # Set timeout back to a high value, so we not waste CPU
                # cycles.
                self.timeout = default_timeout
                self.blob = "" # Reset the message buffer
        elif len(socks) == 0 and self.timeout == default_timeout :
                self.logger.info("Nothing happened for a long time.")
        else:
            pass

        self.logger.info('Stopping')
        self.context.term()

#------------------------------------------------------------------------------

class UDPDispatcher(Dispatcher):
    def __init__(self, dispatcher_type, dispatcher_id):
        Dispatcher.__init__(self, dispatcher_type, dispatcher_id)
        
        config = configparser.ConfigParser()
        config.read('dispatcher.conf')
        dispatcher_section = ('dispatcher-{0}-{1}'
                                  .format(dispatcher_type, dispatcher_id))

        if (dispatcher_section) in config.sections()):
            entries = config[dispatcher_section]
            # path to the message class
            self.message_path = entries['MessagePath']
            if message_path is not None:
                loader = importlib.machinery.SourceFileLoader('message',
                                                              message_path)
                message_module = loader.exec_module('message')
                message = message_module.Message()
            # address and port to listen on for messages from the system
            self.accept_address = entries['AcceptAddress']
            self.listen_port = entries['ListenPort']
            
            # Is the dispatcher supposed to forward to another system
            # instead of to the scenario player.
            self.forwarder = (entries['Forwarder'].lower() in ['true', '1',
                                                               'yes'])
            # check to see if messages should be forwarded to another 
            # system
            if forwarder:
                self.second_accept_address = entries['SecondAcceptAddress']
            else:
                # port to listen on for commands from the player.
                self.command_listen_port = entries['CommandListenPort']
                # port to forward messages to the player.
                self.message_forward_port = entries['MessageForwardPort']
                        
        else:
            self.logger.critical('no valid udp section found in config file')

    def create_sockets(self):
        """ Create the UDP sockets between the system and the 
            Scenario player
        """
        self.logger.info('Creating sockets for {0} {1}'
                         .format(self.name, self.dispatcher_id))
        # Open an UDP socket to listen for new connections 
        # from the system.
        self.logger.info("Listening on address {0}"
                         .format(str(self.accept_address)))
        self.logger.info("Listening on port {0}".format(str(self.listen_port)))
        address = "udp://{0}:{1}".format(accept_address, listen_port)
        accept_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        accept_socket.bind((self.accept_address, self.listen_port))
        # Let the superclass finish the creation of the rest of the 
        # sockets, because it is the same.
        Dispatcher.create_sockets(self)

    def run(self):
        pass



