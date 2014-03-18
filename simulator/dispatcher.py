import logging
import signal
import socket
import configparser
import importlib.machinery

import zmq

class Dispatcher(object):
    def __init__(self, dispatcher_type, dispatcher_id):
        self.name = name
        self.dispatcher_id = dispatcher_id
        self.call_backs = {}
        self.forwarder = False

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

#------------------------------------------------------------------------------

class TCPDispatcher(Dispatcher):
    def __init__(self, dispatcher_type, dispatcher_id):
        Dispatcher.__init__(self, name, dispatcher_id)
        
        tcp_config = configparser.ConfigParser()
        tcp_config.read('dispatcher.conf')
        tcp_dispatcher_section = ('tcp-dispatcher-{0}-{1}'
                                  .format(dispatcher_type, dispatcher_id))

        if (tcp_dispatcher_section) in tcp_config.sections()):
            entries = tcp_config[tcp_dispatcher_section]
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
            # port to listen on for commands from the player.
            self.command_listen_port = entries['CommandListenPort']
            # port to forward messages to the player.
            self.message_forward_port = entries['MessageForwardPort']
            
            # Is the dispatcher supposed to forward to another system
            # instead of to the scenario player.
            self.forwarder = (entries['Forwarder'].lower() in ['true', '1',
                                                               'yes'])
            if forwarder:
                second_accept_address = entries['SecondAcceptAddress']
                        
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
        self.logger.info("Listening on address " + str(self.accept_address))
        self.logger.info("Listening on port " + str(self.port))
        accept_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        accept_socket.bind((self.accept_address, self.port))        
        # Only handle one connection at a time.
        accept_socket.listen(1)
        
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
        self.call_backs[command_socket]         = (command_socket, 
                                                   self.process_player_command)

        # Not part of the poller
        # Message forwarding link to player
        address = "tcp://*:{0}".format(self.message_forward_port)
        self.logger.info("Publishing on " + address)
        self.repeater_socket = self.context.socket(zmq.PUB)
        self.repeater_socket.bind(address)
        

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
            a_telegram = message.from_message(blob = data)
            self.logger.info('Copying data to player')
            self.repeater_socket.send_pyobj(a_telegram)

    def run():
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
                    if socket_key in self.call_backs:
                        cbp = self.call_backs[socket_key]
                        function =  cbp[1]
                        function(cbp[0])

            self.logger.info("Still alive")

        self.context.term()

#------------------------------------------------------------------------------


class SerialDispatcher(Dispatcher):
    def __init__(self):
        Dispatcher.__init__(self)

    def forward():
        pass
    
    def accept():
        pass

    def run():
        pass

class UDPDispatcher(Dispatcher):
    def __init__(self):
        Dispatcher.__init__(self)

    def forward():
        pass
    
    def accept():
        pass

    def run():
        pass


