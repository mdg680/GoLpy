import unittest
from grid import Grid as g
from lifes import Lifes as l

class Test(unittest.TestCase):
    """
    Test-class
    """

    def test_grid_dim(self):
        a = g((41, 32))
        self.assertEqual(a.get_width(), 32)
        self.assertEqual(a.get_height(), 41)
    def test_grid_spec(self):
        a = g(l.block)
        self.assertEqual(a.get_array(), [[0,0,0,0], 
                                         [0,1,1,0], 
                                         [0,1,1,0],
                                         [0,0,0,0]])
        a = g(l.blinker)
        self.assertEqual(a.get_array(), [[0,0,0,0,0], 
                                         [0,0,0,0,0], 
                                         [0,1,1,1,0], 
                                         [0,0,0,0,0], 
                                         [0,0,0,0,0]])
    def test_grid_iter(self):
        a = g(l.blinker)
        self.assertEqual(a.get_array(), [[0,0,0,0,0], 
                                         [0,0,0,0,0], 
                                         [0,1,1,1,0], 
                                         [0,0,0,0,0], 
                                         [0,0,0,0,0]])

        # make an iteration and check the resulting grid for first oscillation step
        a.iterate()
        res_test = [[0,0,0,0,0], 
                    [0,0,1,0,0], 
                    [0,0,1,0,0], 
                    [0,0,1,0,0], 
                    [0,0,0,0,0]]
                    
        self.assertEqual((a.get_array() == res_test).all(), True)
    
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(Test)
    unittest.TextTestRunner(verbosity=2).run(suite)