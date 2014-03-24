import sys
import connectionfactory

"""Simulator starter.

Usage
    ./start_simulator <command>  <id>
    command :== <start|restart|stop>
    type    :== <TCP|UDP|Serial>
    id      :== <0|1>

Initializes and starts the a simulator.
Writes all logging data to /tmp/type_simulator_<id>.log
"""
if __name__ == "__main__":
    if len(sys.argv) == 4:
        # Retrieve a factory for the specified type of simulator.
        factory = (connectionfactory.ConnectionFactory().
                   get_connection(sys.argv[2]))
        # Let the factory create the daemon to use.
        daemon = factory.get_daemon(factory.get_dispatcher(sys.argv[2],
                                                           sys.argv[3]),
                                    '{0}-simulator'.format(sys.argv[2]),
                                    sys.argv[3])
        # Start the daemon and pass dispatcher to use.
        daemon.startup()
    else:
        print "Usage: %s start|stop|restart|version <type> <id>" % sys.argv[0]
        sys.exit(2)
