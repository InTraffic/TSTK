import daemon
import dispatcher


class TCPConnectionFactory():
    
    def get_daemon(self, dispatcher, name, simulator_id):
        return daemon.TCPDaemon(get_dispatcher(name, simulator_id), name, 
                                simulator_id)
    
    def get_dispatcher(self, name, simulator_id):
        return dispatcher.TCPDispatcher(name, simulator_id)

class SerialConnectionFactory():

    def get_daemon(self, dispatcher, name, connection_id):
        return daemon.SerialDaemon(get_dispatcher(name, simulator_id), name, 
                                   simulator_id)
    
    def get_dispatcher(self, name, simulator_id):
        return dispatcher.SerialDispatcher(name, simulator_id)

class UDPConnectionFactory():

    def get_daemon(self, dispatcher, name, connection_id):
        return daemon.UDPDaemon(get_dispatcher(name, simulator_id), name, 
                                simulator_id))
    
    def get_dispatcher(self, name, simulator_id):
        return dispatcher.UDPDispatcher(name, simulator_id)

class ConnectionFactory(object):
    """ This connection factory will return the Dispatcher and Daemon of the
    requested type. This is the class to use if you want to create and add a new
    connection to the testsystem.
    
    Attributes:
    connection_types - This is a dictionary containing the known connection 
                       types as the key and the corresponding conrete
                       connection factory as the value.
    """
    
    # This dictionary contains all the known connection factories.
    connection_types = {"TCP":TCPConnectionFactory(),
                        "UDP":UDPConnectionFactory(),
                        "Serial":SerialConnectionFactory()}

    def get_connection(self, connection_type):
        # return the correct connection type and get the daemon and dispatcher
        # for this specific connection.
        return self.connection_types.get(connection_type)


