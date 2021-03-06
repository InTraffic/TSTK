import logging
import zmq
import copy
import simulator

class SimulatorInterface(object):
    """ A generic simulator interface for communication with the 
    corresponding simulator.
    """
    
    def __init__(self, name, sim_id, zmq_context):
        self.logger = logging.getLogger('simulatorinterface.{0}{1}'
                                        .format(name, str(sim_id)))
        self.message_port = 9001
        self.command_port = 9000
        self.message_link = zmq_context.socket(zmq.SUB)
        self.message_link.connect("tcp://localhost:{0}"
                                  .format(self.message_port))
        self.message_link.setsockopt_string(zmq.SUBSCRIBE, "")

        self.command_link = zmq_context.socket(zmq.PUB)
        self.command_link.connect("tcp://localhost:{0}"
                                  .format(self.command_port))

        self.callbacks = {}

    def on_message(self, scenario_player):
        """ Receive a message from the simulator

        :param scenario_player: unused
        """
        message = self.message_link.recv_pyobj()
        self.do_callbacks(message)
    
    def do_callbacks(self, message):
        """ Call the callbacks for the message
        
        :param message: the message from the simulator to do the 
                        callbacks for
        """
        if message.message_id in self.callbacks:
            # Have to operate on a copy because the callback functions
            # can modify the callback list.
            for function in copy.copy(self.callbacks[message.message_id]):
                function(message)
    
    def set_callback(self, message_id, function):
        """ Add a callback function for a message

        :param message_id: the message id
        :param function: the function to add
        """
        if message_id in self.callbacks:
            self.callbacks[message_id].append(function)
        else:
            self.callbacks[message_id] = [function]
    
    def send(self, message):
        """ Send a message to the simulator

        :param message: The message to send to the simulator
        """
        self.command_link.send_pyobj(message)


def get_simulator_interface(sim_interface_type):
    """ Function to get a specific type of simulator interface.

    :param sim_interface_type: The type of simulatorinterface to return.
    :returns: The class for the specified simulatorinterface type.
    """
    simulator_interfaces = {"default":SimulatorInterface}
    sim_interface = simulator_interfaces.get(sim_interface_type)
    return sim_interface



