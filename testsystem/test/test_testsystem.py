import unittest
import testsystem
import scenarioplayer

class TestSystemTestCase(unittest.TestCase):
    """Tests for the scenarioplayer in the testsystem module"""
    
    def setUp(self):
        self.test_system = testsystem.TestSystem("unittest")
        self.test_system.add_scenario_player()

    def tearDown(self):
        self.test_system = None

    @unittest.skip("Haven't figured out yet how to test the adding of a" 
                   " driver if the toolkit packages haven't been "
                   "installed yet in the development environment.")
    def test_add_driver(self):
        """ Test if a driver can be added to the testsystem"""
        self.test_system.add_driver("foo", "portal", 8)
        self.assertIn("foo", test_case.drivers)

    def test_add_simulator_interface(self):
        """ Test the adding of a simulator interface to the testsystem
        """
        self.test_system.add_simulator_interface("unittest", 0, "default")
        self.assertIn("unittest", self.test_system.simulator_interfaces)

if __name__ == '__main__':
    unittest.main()
