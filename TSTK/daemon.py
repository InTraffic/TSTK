from daemonbase import Daemon
import sys
import os
import logging

class TISDaemon(Daemon):
    """Baseclass for all TIS daemons
    Contains the default parameter and logging handling.
    """

    def __init__(self, dispatcher, name, daemon_id):
        errorlogfile = '/{0}_{1}.err'.format(name, daemon_id)
        pidfile = '/tmp/{0}_{1}.pid'.format(name, daemon_id)
        Daemon.__init__(self, pidfile, stderr=errorlogfile)
        self.dispatcher = dispatcher
        self.name = name
        self.daemon_id = daemon_id
        self.logger = None

    def setup_logging( self ):
        """Setup the default logging based on the name of this daemon"""
        self.logger = logging.getLogger(self.name)
        self.logger.setLevel(logging.INFO)
        logfile = ('/{0}_{1}.log'.format(self.name, self.daemon_id))
        filehandler = logging.FileHandler(logfile)
        filehandler.setLevel(logging.INFO)
        formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        filehandler.setFormatter(formatter)
        self.logger.addHandler(filehandler)


    def startup(self):
        """Default parameter handling to start or stop the daemon"""
        if 'start' == sys.argv[1]:
            self.start()
        elif 'stop' == sys.argv[1]:
            self.stop()
        elif 'restart' == sys.argv[1]:
            self.restart()
        elif 'run' == sys.argv[1]:
            self.run()
        elif 'status' == sys.argv[1]:
            self.status()
        elif 'version' == sys.argv[1]:
            pass
        else:
            print("Unknown command")
            sys.exit(2)


class TCPDaemon(TISDaemon):
    """Class to turn TCP simulator into a server that runs in the
    background.
    """
    def __init__(self, daemon, name, daemon_id):
        TISDaemon.__init__(self, daemon, name, daemon_id)

    def run(self):
        """Start the dispatcher
        """
        # If we run, we want logging...
        self.setup_logging()
        # Start simulator
        self.logger.info('Starting TCP simulator')
        # All the actual work is done by the dispatcher.
        self.dispatcher.run(self.daemon_id)

class SerialDaemon(TISDaemon):
    """Class to turn Serial simulator into a server that runs in the
    background.
    """
    def __init__(self, daemon, name, daemon_id):
        TISDaemon.__init__(self, daemon, name, daemon_id)

    def run(self):
        """Start the dispatcher
        """
        # If we run, we want logging...
        self.setup_logging()
        # Start simulator
        self.logger.info('Starting Serial simulator')
        # All the actual work is done by the dispatcher.
        self.dispatcher.run(self.daemon_id)

class UDPDaemon(TISDaemon):
    """Class to turn UDP simulator into a server that runs in the
    background.
    """
    def __init__(self, daemon, name, daemon_id):
        TISDaemon.__init__(self, daemon, name, daemon_id)

    def run(self):
        """Start the dispatcher
        """
        # If we run, we want logging...
        self.setup_logging()
        # Start simulator
        self.logger.info('Starting UDP simulator')
        # All the actual work is done by the dispatcher.
        self.dispatcher.run(self.daemon_id)

class HttpDaemon(TISDaemon):
    """Class to turn Http simulator into a server that runs in the
    background.
    """
    def __init__(self, daemon, name, daemon_id):
        TISDaemon.__init__(self, daemon, name, daemon_id)

    def run(self):
        """Start the dispatcher
        """
        # If we run, we want logging...
        self.setup_logging()
        # Start simulator
        self.logger.info('Starting Http simulator')
        # All the actual work is done by the dispatcher.
        self.dispatcher.run(self.daemon_id)







