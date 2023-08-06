
import numpy as np

class Initializer(object):
    """
    This is an initializer class which can be used to initialize the Optimizer
    
    """
    def __call__(self, shape):
        """
        Returns a numpy array initialized as specified by the initializer.
        
        INPUTS
        =======
        - shape: int, size of the numpy array that will be returned
        """
        raise NotImplementedError()
    
    def get_config(self):
        """
        Returns the configuration of the initializer as a JSON-serializable dict.
        RETURNS
        ========
        A JSON-serializable Python dict.
        """
        return {}

class Zeros(Initializer):
    """
    Initializer which can be used to initialize the Optimizer to zeros.
    
    EXAMPLES
    =========
    >>> import numpy as np
    >>> from WestCoastAD import Initializer
    >>> initializer = Zeros()
    >>> initializer(5)
    array([0., 0., 0., 0., 0.])
    
    """
    def __call__(self, shape):
        """
        Returns a numpy array initialized to 0.
        INPUTS
        =======
        - shape : int, size of the numpy array that will be returned
        """
        return np.zeros(shape)
    
class Ones(Initializer):
    """
    Initializer which can be used to initialize the Optimizer to ones.
    
    EXAMPLES
    =========
    >>> import numpy as np
    >>> from WestCoastAD import Initializer
    >>> initializer = Ones()
    >>> initializer(4)
    array([1., 1., 1., 1.])
    
    """
    def __call__(self, shape):
        """
        Returns a numpy array initialized to 1.
        INPUTS
        =======
        - shape : int, size of the numpy array that will be returned
        """
        return np.ones(shape)

class Constant(Initializer):
    """
    Initializer which can be used to initialize the Optimizer to an input constant.
    
    EXAMPLES
    =========
    >>> import numpy as np
    >>> from WestCoastAD import Initializer
    >>> initializer = Constant(-6.5)
    >>> initializer(10)
    array([-6.5, -6.5, -6.5, -6.5, -6.5, -6.5, -6.5, -6.5, -6.5, -6.5])
    >>> initializer.get_config()
    {'value': -6.5}
    
    """
    def __init__(self, value=0):
        """
        INPUTS
        =======
        - value : a scalar. A value used for initialization.
        
        RETURNS
        ========
        None
        """
        self.value = value
        
    
    def __call__(self, shape):
        """
        Returns a numpy array initialized to a constant.
        INPUTS
        =======
        - shape : int, size of the numpy array that will be returned
        """
        return self.value*np.ones(shape)
    
    def get_config(self):
        """
        Returns the configuration of the initializer as a JSON-serializable dict.
        RETURNS
        ========
        A JSON-serializable Python dict.
        """
        return {'value': self.value}
    
class RandomUniform(Initializer):
    """
    Initializer which can be used to initialize the Optimizer according to a uniform distribution.
    
    EXAMPLES
    =========
    >>> import numpy as np
    >>> from WestCoastAD import Initializer
    >>> np.random.seed(seed=2020)
    >>> initializer = RandomUniform(1,4)
    >>> initializer(5)
    array([3.95883049, 3.62017584, 2.52923657, 1.81550714, 2.01075618])
    >>> initializer.get_config()
    {'min value': 1, 'max value': 4}
    
    """
    def __init__(self, minval, maxval):
        """
        INPUTS
        =======
        - minval : a scalar. Lower bound of the range of random values to generate (inclusive).
        - maxval : a scalar. Upper bound of the range of random values to generate (exclusive).
        
        RETURNS
        ========
        None
        """
        self.minval = minval
        self.maxval = maxval
        
    def __call__(self, shape):
        """
        Returns a numpy array initialized according to a uniform distribution.
        INPUTS
        =======
        - shape : int, number of Variable object
        """
        return np.random.uniform(low=self.minval, high=self.maxval, size=shape)
    
    def get_config(self):  # To support serialization
        """
        Returns the configuration of the initializer as a JSON-serializable dict.
        RETURNS
        ========
        A JSON-serializable Python dict.
        """
        return {"min value": self.minval, "max value": self.maxval}
    
class RandomNormal(Initializer):
    """
    Initializer which can be used to initialize the Optimizer according to a normal distribution.
    
    EXAMPLES
    =========
    >>> import numpy as np
    >>> from WestCoastAD import Initializer
    >>> np.random.seed(seed=2020)
    >>> initializer = RandomNormal(1,0.2)
    >>> initializer(4)
    array([0.64623086, 1.01511045, 0.77387406, 0.86971397])
    >>> initializer.get_config()
    {'mean': 1, 'stddev': 0.2}
    
    """
    def __init__(self, mean, stddev):
        """
        INPUTS
        =======
        - mean : a scalar. Mean of the random values to generate.
        - stddev : a scalar. Standard deviation of the random values to generate.
        
        RETURNS
        ========
        None
        """
        self.mean = mean
        self.stddev = stddev
    
    def __call__(self, shape):
        """
        Returns a numpy array initialized according to a normal distribution.
        
        INPUTS
        =======
        - shape : int, size of the numpy array that will be returned
        
        """
        return np.random.normal(loc=self.mean, scale=self.stddev, size=shape)
    
    def get_config(self):  # To support serialization
        """
        Returns the configuration of the initializer as a JSON-serializable dict.
        RETURNS
        ========
        A JSON-serializable Python dict.
        """
        return {"mean": self.mean, "stddev": self.stddev}

