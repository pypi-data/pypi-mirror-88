import unittest
import numpy as np


np.random.seed(seed=2020)

import unittest
import numpy as np

from WestCoastAD import Initializer
from WestCoastAD import Zeros
from WestCoastAD import Ones
from WestCoastAD import Constant
from WestCoastAD import RandomUniform
from WestCoastAD import RandomNormal
np.random.seed(seed=2020)

class InitializerUnitTest(unittest.TestCase):
    
    def test_Initializer(self):
        initializer = Initializer()

        with self.assertRaises(NotImplementedError):
            var_int = initializer(5)
      
    def test_Zeros(self):
        initializer = Zeros()
        var_init = initializer(5)
        
        self.assertEqual(np.zeros(5).all(), var_init.all())
   
    def test_Ones(self):
        initializer = Ones()
        var_init = initializer(10)
        
        self.assertEqual(np.ones(10).all(), var_init.all())
          
    def test_Constant(self):
        value = -1.33
        initializer = Constant(value)
        var_init = initializer(10)
        
        self.assertEqual((value*np.ones(10)).all(), var_init.all())
        self.assertEqual({'value': value}, initializer.get_config())
        
    def test_RandomUniform(self):
        maxval = 5
        minval = 2.5
        initializer = RandomUniform(minval, maxval)
        var_init = initializer(7)
        
        self.assertEqual(np.random.uniform(2.5,5,7).all(), var_init.all())
        self.assertEqual({"min value": minval, "max value": maxval}, initializer.get_config())
        
    def test_RandomNormal(self):
        mean = 1
        stddev = 0.25
        initializer = RandomNormal(mean, stddev)
        var_init = initializer(100)
        
        self.assertEqual(np.random.normal(1, 0.25, 100).all(), var_init.all())
        self.assertEqual({"mean": mean, "stddev": stddev}, initializer.get_config())
   
if __name__ == '__main__':
    unittest.main()