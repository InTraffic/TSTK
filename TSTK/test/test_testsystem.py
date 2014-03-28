import unittest
import testsystem
import scenarioplayer
import driver
import simulatorinterface

class TestSystemTestCase(unittest.TestCase):
    """Tests for the scenarioplayer in the testsystem module"""

    def tearDown(self):
        self.test_system = None

    def test_add_driver(self):
        """ Test if a driver can be added to the testsystem"""
        self.test_system = testsystem.TestSystem("drivertest")
        self.test_system.add_scenario_player()
        self.test_system.add_driver("foo", "portal", 8)
        self.assertIn("foo", self.test_system.drivers)
        self.assertIsInstance(self.test_system.drivers.get("foo"),
                              driver.Portal)

    def test_add_simulator_interface(self):
        """ Test the adding of a simulator interface to the testsystem
        """
        self.test_system = testsystem.TestSystem("simulatorinterfacetest")
        self.test_system.add_scenario_player()
        self.test_system.add_simulator_interface("unittest", 0, "default")
        self.assertIn("unittest", self.test_system.simulator_interfaces)


if __name__ == '__main__':
    unittest.main()
