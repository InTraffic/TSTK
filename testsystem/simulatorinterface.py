import logging
import zmq
import copy

class SimulatorInterface(object):
    """ Simulator interface for communication with the corresponding
    simulator.
    """
    
    def __init__(self, name, sim_id, zmq_context):
        """
        """
        self.logger = logging.getLogger('simulatorinterface.{0}{1}'
                                        .format(name, str(sim_id)))
        self.message_link = zmq_context.socket(zmq.SUB)
        self.message_link.connect("tcp://localhost:{0}"
                                  .format(message_port))
        self.message_link.setsockopt(zmq.SUBSCRIBE, "")

        self.command_link = zmq_context.socket(zmq.PUB)
        self.command_link.connect("tcp://localhost:{0}"
                                  .format(command_port))

        self.callbacks = {}

    def on_message(self, scenario_player):
        pass
    
    def do_callbacks(self, message):
        pass
    
    def set_callback(self, message_id, function):
        pass
    
    def send(self, message):
        pass
