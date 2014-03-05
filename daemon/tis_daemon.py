"""Baseclass for all OTIS daemons"""

from daemonbase import Daemon
import sys
import os
import version
import logging

class TISDaemon( Daemon ):

    """OTIS version of Daemon class
    Contains the default parameter handling and logging handling.
    """
    def __init__( self, name, daemon_id ):
        errorlogfile = ('/%s_%s.err' % ( name, daemon_id ) )
        pidfile      = '/tmp/%s_%s.pid' % ( name, daemon_id )
        Daemon.__init__( self, pidfile, stderr=errorlogfile )
        self.name = name
        self.daemon_id = daemon_id
        self.logger = None

    def setup_logging( self ):
        """Setup the default logging based on the name of this daemon"""
        self.logger = logging.getLogger( self.name )
        self.logger.setLevel( logging.INFO )
        logfile = ('/%s_%s.log' % ( self.name, self.daemon_id ) )
        filehandler = logging.FileHandler( logfile )
        filehandler.setLevel( logging.INFO )
        formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        filehandler.setFormatter( formatter )
        self.logger.addHandler( filehandler )


    def startup( self ):
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
            print version.get_version()
        else:
            print "Unknown command"
            sys.exit(2)


