#-----------------------------------------------------------
from event_store       import EventStore
from scenarioplayer    import ScenarioPlayer
import versionmanager
'''
from gps_sim           import GPSSim
from train             import Train
from portal            import Portal
from trees2rita        import Trees2Rita
from rita_notification import RitaNotification
from timespec          import parse_timespec
from otis_player.focon import FOCON
from otis_player.cc    import CC
from soap_notification import SoapNotification
#-----------------------------------------------------------

import otis_version
#-----------------------------------------------------------

'''

class TestCase_Exception(Exception):
    """Base class for TestCase exceptions."""
    pass

class TestCase_Too_Many_Drivers(TestCase_Exception):
    """Thrown when more than two drivers of the same type are added to a
    testcase.
    """
    pass

# We really need this many attributes.  Every driver has two attributes
# and there are many drivers.  Putting them in some container would make
# the test scripts far less readable.
# pylint: disable=R0902
class TestCase(object):
    """TestCase building block

    Creates most of the common objects needed to execute a test case.

    Attributes:

    * gps -- the GPS driver,
    * logger -- the logger,
    * event_store -- the event store,
    * trees2rita -- the trees2rita driver,
    * rita2trees -- the rita2trees driver,
    * train -- the train status driver,
    * player -- the scenario player,
    * portal -- the Portal driver,
    * focon -- the FOCON driver.
    """
    def __init__( self, name, test_system_name, debug=False ):
	"""Parameters:
	name -- The name given to the testcase
	test_system_name -- The name of the system which is being tested
	"""
	
        self.kill_previous_script(test_system_name)
        # Setup logging
        logger = logging.getLogger( test_system_name )
        logger.setLevel( logging.INFO )
        logfile = '{0}'.format(test_system_name)
        filehandler = logging.FileHandler( logfile )
        filehandler.setLevel( logging.INFO )
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        filehandler.setFormatter( formatter )
        logger.addHandler( filehandler )
        self.logger      = logger
        self.logger.info( versionmanager.get_version() ) 
        self.logger.info('Starting testcase ' + name)

        script_name = sys.argv[0]
        parameters  = sys.argv[1:]
        self.logger.info('From testscript ' + script_name )
        if len( parameters ) > 0 :
            self.logger.info( 'With parameters ' + ' '.join( parameters ) )
        else :
            self.logger.info( 'With no parameters' )
        #-------------------
        self.event_store = EventStore( title=name, debug=debug )
        self.player      = ScenarioPlayer( self.event_store, self )

'''
        # Easy access to the first instance of each type of driver.
        # Also needed for backwards compatibility.
        #
        self.gps         = None
        self.trees2rita  = None
        self.rita2trees  = None
        self.train       = None
        self.portal      = None
        self.focon       = None
        # It is really called cc.
        # pylint: disable=C0103
        self.cc          = None
        self.soap        = None

        # It's possible to have more than one of the same driver.
        # These are stored and access through an array.
        self.gps_a        = []
        self.trees2rita_a = []
        self.rita2trees_a = []
        self.train_a      = []
        self.portal_a     = []
        self.focon_a      = []
        self.cc_a         = []
        self.soap_a       = []
'''
    def kill_previous_script( self, test_system_name ):
        """Kill an already running test script. Can't have to 
        scripts running at the same time.
        """

        lock_name = 'log/{0}.lock'.format(test_system_name)
        if os.path.exists( lock_name ):
            # Find the process that has lock_name open.
            subp = subprocess.Popen(['lsof', '-t', lock_name],
                                  shell=False,
                                  stdout=subprocess.PIPE)

            # pylint: disable=W0612
            (pids, errors) = subp.communicate()
            if subp.returncode == 0 and (len(pids)>0):
                # It's not a list, it is really a string
                # pylint: disable=E1103
                for pid in pids.split():
                    # And kill it.
                    subp = subprocess.Popen(['kill', '-9', pid.rstrip()])
                    subp.communicate()
                    if subp.returncode != 0 :
                        print "Can't kill previous test script"
                        exit( 1 )
                # Give it some time
                time.sleep(1)
        # Now open a file and keep it open, so the next
        # script can kill us.
        self.lock = open( lock_name, 'w' )

    def close( self ):
        """Clean up the lock so we can properly run unittest"""
        if self.lock is None :
            pass
        else :
            print 'closing lock'
            self.lock.close()
            self.lock = None
		
'''
    def add_cc( self ):
        """Add the CC driver to the test case

        Will be available through TestCase.cc and TestCase.cc_a[]
        """
        self.logger.info('Adding CC driver')

        # Path to the CC simulator
        cc_path = 'bin/cc_daemon'
        cc = CC( self.event_store, self.player.context )
        if self.cc is None :
            cc_id = 0
            self.cc = cc
        elif len( self.cc_a ) == 1 :
            cc_id = 1
        else :
            raise TestCase_Too_Many_Drivers( 
                    "Only two CC drivers are allowed." )

        cc.dev_id = cc_id
        self.cc_a.append( cc )
        # Start CC simulator if not already started.
        subprocess.Popen(
              [PYTHON3_PATH, cc_path, "restart", str( cc_id ) ]).wait()
        self.player.add_socket( cc.message_link,
                                 cc.on_message )

    def add_focon( self ):
        """Add the FOCON driver to the test case

        Will be available through TestCase.focon, and TestCase.focon_a[].
        """
        self.logger.info('Adding FOCON driver')

        focon_path = ( 'bin/focon_daemon' )
        focon = FOCON( self.event_store, self.player.context )
        if self.focon is None :
            focon_id = 0
            self.focon = focon
        elif len( self.focon_a ) == 1 :
            focon_id = 1
        else :
            raise TestCase_Too_Many_Drivers( 
                    "Only two FOCON drivers are allowed." )

        self.focon_a.append( focon )
        # Start FOCON simulator if not already started.
        subprocess.Popen([PYTHON3_PATH, focon_path, 
            "restart", str( focon_id ) ]).wait()
        self.player.add_socket( focon.message_link,
                                focon.on_message )



    def add_gps( self ):
        """Add the gps driver to the test case

        Will be available through TestCase.gps, and TestCase.gps_a[].
        """
        self.logger.info('Adding gps driver')

        gps_path = 'bin/gps_daemon'

        gps = GPSSim( self.event_store )
        if self.gps is None :
            gps_id = 0
            self.gps = gps
        elif len( self.gps_a ) == 1 :
            gps_id = 1
        else :
            raise TestCase_Too_Many_Drivers( 
                    "Only two GPS drivers are allowed." )

        gps.dev_id = gps_id
        self.gps_a.append( gps )
        # Start GPS simulator if not already started.
        subprocess.Popen([PYTHON3_PATH, gps_path, 
            "restart", str( gps_id ) ]).wait()


    def add_rita2trees( self ):
        """Add the rita2trees driver to the testcase.

        Will be available through TestCase.rita2trees.
        """
        self.logger.info('Adding rita2trees driver')

        if len( self.rita2trees_a ) > 1 :
            raise TestCase_Too_Many_Drivers( 
                     "Only two rita2trees drivers are allowed." )
        else :
            if self.rita2trees is None :
                r2t_id = 0
            else :
                r2t_id = 1

            # First construct rita2trees object.
            # If we first start rita2trees the socket will be locked
            # the next time we run OTIS.   (Don't know why!)
            rita2trees  = RitaNotification( self.event_store, 
                                            port=32040+r2t_id,
                                            dev_id=r2t_id )
            self.player.add_socket( rita2trees.server_socket, 
                                    rita2trees.accept )

            if self.rita2trees is None :
                self.rita2trees = rita2trees
            # Also add it to the array.
            self.rita2trees_a.append( rita2trees )

            # Start rita2trees if not already started.
            r2t_path = 'bin/rita2trees.py'
            subprocess.Popen([PYTHON2_PATH, r2t_path, l
                "restart", str( r2t_id ) ]).wait()

    def add_soap(self):
        self.logger.info('Adding SOAP driver')

        soap_path = 'bin/otis_soap'
        soap = SoapNotification(self.event_store, self.player.context)
        if self.soap  is None :
            soap_id = 0
            self.soap = soap
        else :
            raise TestCase_Too_Many_Drivers(
                    "Only one SOAP drivers is allowed.")

        soap.dev_id = soap_id
        self.soap_a.append(soap)
        # Start Soap Drive if not already started.
        subprocess.Popen(
              [PYTHON2_PATH, soap_path, "restart" ]).wait()
        self.player.add_socket(soap.message_link, soap.on_message)


    def add_trees2rita( self ):
        """Add the trees2rita driver to the testcase.

        Will be available through TestCase.trees2rita and TestCase.trees2rita_a[].
        """
        if self.trees2rita is None :
            t2r_id = '0'
            self.logger.info('Adding trees2rita driver')
        elif len( self.trees2rita_a ) == 1 :
            t2r_id = '1'
            self.logger.info('Adding additional trees2rita driver')
        else :
            raise TestCase_Too_Many_Drivers( 
                    "Too many trees2rita drivers" )

        trees2rita  = Trees2Rita( self.event_store, t2r_id )
        if self.trees2rita is None :
            self.trees2rita = trees2rita
        self.trees2rita_a.append( trees2rita )


    def add_train( self, debug = False ):
        """Add train status driver to the test case.

        Will be available through TestCase.train and TestCase.train_a[].
        """

        if self.train is None :
            train_id = 0
            self.logger.info('Adding train status driver.')
        elif len ( self.train_a ) == 1 :
            train_id = 1
            self.logger.info('Adding second train status driver.')
        else :
            raise TestCase_Too_Many_Drivers( 
                    "Too many train drivers" )

        train = Train( self.event_store, train_id = train_id, debug = debug )
        if self.train is None :
            self.train = train
        self.train_a.append( train )

    def add_portal( self ):
        """Add portal driver to the test case.

        Will be available through TestCase.portal and TestCase.portal_a[].
        """

        self.logger.info('Adding portal driver')
        if self.portal is None:
            self.portal = Portal( portal_id = 0 )
            self.portal_a.append( self.portal )
        elif len( self.portal_a ) == 1:
            self.portal_a.append( Portal( portal_id = 1 ) )
        else :
            raise TestCase_Too_Many_Drivers( 
                       "Too many portal drivers" )
'''

    def add_step( self, when, step, show=True, question=None ):
        """ See :`meth:ScenarioPlayer.add_step`"""
        self.player.add_step( when, step, show, question )

    def play( self ) :
        """ See :`meth:ScenarioPlayer.play`"""
        self.player.play()

    def wait_for_answers( self ):
        """Wait until all test steps with questions are answered"""
        self.player.wait_for_answers()

    def stop( self ) :
        """ See :`meth:ScenarioPlayer.stop`"""
        self.player.stop( )

