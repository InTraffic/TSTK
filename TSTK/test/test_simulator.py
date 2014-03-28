import unittest
import connectionfactory

class TestSystemTestCase(unittest.TestCase):
    """Tests for the testsystem module"""

    def setUp(self):
        self.connection = connectionfactory.ConnectionFactory()

    def tearDown(self):
        self.connection = None

    def test_get_connection(self):
        """ Test if a the connection can be retrieved correctly"""
        self.assertIsInstance(self.connection.get_connection("TCP"),
                              connectionfactory.TCPConnectionFactory)
        self.assertIsInstance(self.connection.get_connection("UDP"),
                              connectionfactory.UDPConnectionFactory)
        self.assertIsInstance(self.connection.get_connection("Serial"),
                              connectionfactory.SerialConnectionFactory)
        self.assertIsInstance(self.connection.get_connection("HTTP"),
                              connectionfactory.HttpConnectionFactory)
        self.assertIsInstance(self.connection.get_connection("tcp"),
                              connectionfactory.TCPConnectionFactory)


if __name__ == '__main__':
    unittest.main()
