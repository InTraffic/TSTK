import unittest
import driver

class DriverTestCase(unittest.TestCase):
    """Tests for the driver module"""
    
    def test_get_driver(self):
        """Test the retrieval of a driver through the get_driver 
        function
        """
        a_driver = driver.get_driver("portal", 1)
        self.assertIsInstance(a_driver, driver.Portal)
        a_driver = driver.get_driver("usbrly08b", 1)
        self.assertIsInstance(a_driver, driver.Usbrly08b)

    

if __name__ == '__main__':
    unittest.main()
        
