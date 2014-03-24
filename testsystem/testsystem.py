import logging

from scenarioplayer import ScenarioPlayer
from testcase import TestCase
from simulatorinterface import SimulatorInterface
from driver import driver as drivers

import zmq

class TestSystem(object):
    """ Starting point when creating a test system for a specific
    system. 
    
    Attributes:
        context: This will be the zmq context.
        test_case: The testcase associated with this testsystem.
        scenario_player: The scenario player which will play the steps.
        simulator_interfaces: The simulator_interfaces used by this 
                              test system.
        drivers: The drivers used by the testsystem.
        logger: The logger.

    Use this class by creating a subclass, so you can also add your own
    simulator interfaces.
    """
    context = None
    scenario_player = None
    simulator_interfaces = {}
    drivers = {}
    logger = None

    def __init__(self, test_system_name):
        """
        """
        self.kill_previous_script(test_system_name)
        #Setup logging.
        logger = logging.getLogger('Testsystem')
        logger.setLevel(logging.DEBUG)
        logfile = 'Testsystem.log'
        filehandler = logging.FileHandler(logfile)
        filehandler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s'
                                      ' - %(message)s')
        filehandler.setFormatter(formatter)
        logger.addHandler(filehandler)
        self.logger = logger
        
        
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

    def add_scenario_player(self):
        """ Set the scenario player for the testsystem
        """
        self.scenario_player = ScenarioPlayer(self)
    
    def add_step(self, when, step):
        """ See :func:`ScenarioPlayer.add_step` """
        self.scenario_player.add_step(when, step)

    def add_simulator_interface(self, name, sim_interface):
        """Add a new simulator interface to the list of 
        simulator_interfaces and also add a socket to the scenario
        player.
        
        :param name: The simulator name.
        :type name: string
        :param sim_interface: The kind of simulator interface.
        :type sim_interface: string
        """
        simulator_interface = SimulatorInterface(sim_interface)
        self.simulator_interfaces.append(name:simulator_interface)
        self.scenario_player.add_socket(simulator_interface.message_link, 
                                        simulator_interface.on_message)

    def add_driver(self, name, driver, driver_id):
        """ Add a driver to the test system. The configuration of the
        driver is done with a configuration file. It wil add a driver 
        to the list with the name as key and the specific driver as 
        the value.
        
        :param name: The driver name.
        :type name: string
        :param driver: The kind of driver.
        :type driver: string
        """
        a_driver = drivers.get_driver(driver, driver_id)
        self.drivers.append(name:a_driver)
        
    def play(self):
        """ See :func:`ScenarioPlayer.play` """
        self.scenario_player.play()

    def stop(self):
        """ See :func:`ScenarioPlayer.stop` """
        self.scenario_player.stop()





