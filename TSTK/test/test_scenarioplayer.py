import unittest
import testsystem
import scenarioplayer

class Track(object):
    def __init__(self):
        self.count = [0, 1, 2, 3 , 4]
        self.i = 0

    def zero(self, dummy):
        self.count[self.i] = 0
        self.i = self.i + 1

    def one(self, dummy):
        self.count[self.i] = 1
        self.i = self.i + 1

    def two(self, dummy):
        self.count[self.i] = 2
        self.i = self.i + 1

    def three(self, dummy):
        self.count[self.i] = 3
        self.i = self.i + 1

    def three_special(self, dummy):
        self.count[self.i] = 3
        self.i = self.i + 1
        dummy.add_step(0.1, self.four)

    def four(self, dummy):
        self.count[self.i] = 4
        self.i = self.i + 1

    def check(self):
        status = True
        i = 0
        for x in self.count:
            if x != i:
                print("Check failed: {0} {1}".format(x, i))
                status = False
            i = i + 1
        return status

class ScenarioPlayerTestCase(unittest.TestCase):
    """Tests for the scenarioplayer in the testsystem module"""
    
    def setUp(self):
        self.test_system = testsystem.TestSystem("Foo")
        self.test_system.add_scenario_player()
        self.scenario_player = self.test_system.scenario_player

    def tearDown(self):
        self.scenario_player = None
        self.test_system = None

    def test_add_step(self):
        """Test adding steps in order.

        Adds a number of steps and checks if the are executed in
        the same order.
        """
        s = self.test_system
        track = Track()
        s.add_step(0.1, track.zero)
        s.add_step(0.2, track.one)
        s.add_step(0.21, track.two)
        s.add_step(0.3, track.three)
        s.add_step(0.4, track.four)
        s.play()
        self.assertTrue(track.check())
    

if __name__ == '__main__':
    unittest.main()
        
