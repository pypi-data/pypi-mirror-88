""" 
This file defines the WestCoastAD Variable class which is the core of the automatic 
differentiation package used in WestCoastAD's optimizers.
"""

import numbers
import numpy as np 

class Variable:
    """
    This is a custom variable class with elementary function and operation overloading
    to perform forward mode automatic differentiation for scalar functions of one or more
    variables.

    EXAMPLES
    =========

    # Derivative computation for a univariate scalar functions
    >>> x = Variable(4, 1)
    >>> f = 3*x**2 + 3
    >>> f.value
    51
    >>> f.derivative
    24

    # Derivative computation for a multivariate scalar function
    >>> import numpy as np
    >>> x = Variable(4, np.array([1, 0]))
    >>> y = Variable(1, np.array([0, 1]))
    >>> f = x**2*y + np.sin(x-y)
    >>> f.value
    16.14112000805987
    >>> f.derivative
    array([ 7.0100075, 16.9899925])

    """

    def __init__(self, value, derivative_seed):
        """ 
        constructor for the Variable class

        INPUTS
        =======
        value: An int or float giving the value of the variable
        derivative_seed: An int or float giving a seed value for the variable derivative
        """

        self.value = value
        self.derivative = derivative_seed
    
    
    def __repr__(self):
        """
        Operator overloading for Variable object representation

        INPUTS
        =======
        None

        RETURNS
        ========
        the value attribute of the Variable object
        """

        return "Variable(value={}, derivative={})".format(self.value, self.derivative)


    @property
    def value(self):
        """ 
        getter method for getting the value attribute of the Variable object

        INPUTS
        =======
        None

        RETURNS
        ========
        the value attribute of the Variable object
        
        EXAMPLES
        =========

        # get the value attribute of a variable with scalar derivative
        >>> x = Variable(2, 1)
        >>> print(x.value)
        2
        
        # get the value attribute of a variable with vector derivative
        >>> import numpy as np 
        >>> x = Variable(5, np.array([1, 1]))
        >>> print(x.value)
        5
<<<<<<< HEAD

=======
        
>>>>>>> origin
        """
        return self._value
    

    @property
    def derivative(self):
        """ 
        getter method for getting the derivative attribute of the Variable object

        INPUTS
        =======
        None

        RETURNS
        ========
        the derivative attribute of the Variable object
        
        EXAMPLES
        =========

        # get the derivative attribute of a variable with scalar derivative
        >>> x = Variable(2, 1)
        >>> print(x.derivative)
        1
                
        # get the derivative attribute of a variable with vector derivative
        >>> import numpy as np 
        >>> x = Variable(3, np.array([2, 1.1]))
        >>> print(x.derivative)
        [2.  1.1]

        """
        return self._derivative
   

    @value.setter
    def value(self, value):
        """ 
        setter method for setting the value attribute of Variable object

        INPUTS
        =======
        value: A real number giving the value of the variable

        RETURNS
        ========
        None
        
        EXAMPLES
        =========
        # set the value attribute of a variable with scalar derivative
        >>> x = Variable(2, 1)
        >>> print(x)
        Variable(value=2, derivative=1)
        >>> x.value = 3
        >>> print(x)
        Variable(value=3, derivative=1)
                
        # set the value attribute of a variable with vector derivative to a scalar
        >>> import numpy as np 
        >>> x = Variable(3, np.array([2, 1.1]))
        >>> print(x)
        Variable(value=3, derivative=[2.  1.1])
        >>> x.value = 55
        >>> print(x)
        Variable(value=55, derivative=[2.  1.1])
        
        """
        if not isinstance(value, numbers.Number):
            raise TypeError('Input value should be an int or float.')
        else:
            self._value = value


    @derivative.setter
    def derivative(self,derivative_seed):
        """ 
        setter method for setting the derivative attribute of Variable object

        INPUTS
        =======
        derivative_seed: A real number or 1D array of real numbers giving a seed value for the variable derivative

        RETURNS
        ========
        None
        
        EXAMPLES
        =========

        # set the derivative attribute of a variable with scalar derivative to another scalar
        >>> x = Variable(2, 1)
        >>> print(x)
        Variable(value=2, derivative=1)
        >>> x.derivative = 5.5
        >>> print(x)
        Variable(value=2, derivative=5.5)
        
        # set the derivative attribute of a variable with scalar derivative to a vector 
        >>> x = Variable(2, 1)
        >>> print(x)
        Variable(value=2, derivative=1)
        >>> x.derivative = np.array([2, 1.1])
        >>> print(x)
        Variable(value=2, derivative=[2.  1.1])
                
        # set the derivative attribute of a variable with vector derivative to a scalar 
        >>> import numpy as np 
        >>> x = Variable(2.1, np.array([2.3, 1.1]))
        >>> print(x)
        Variable(value=2.1, derivative=[2.3 1.1])
        >>> x.derivative = 4
        >>> print(x)
        Variable(value=2.1, derivative=4)
        
        # set the derivative attribute of a variable with vector derivative to an vector 
        >>> import numpy as np 
        >>> x = Variable(2.1, np.array([2.3, 1.1]))
        >>> print(x)
        Variable(value=2.1, derivative=[2.3 1.1])
        >>> x.derivative = np.array([6 , 5])
        >>> print(x)
        Variable(value=2.1, derivative=[6. 5.])

        """
        
        if isinstance(derivative_seed, numbers.Number):
            self._derivative = derivative_seed
            self._dimensionality = 1
        elif isinstance(derivative_seed, np.ndarray) and len(derivative_seed.shape) == 1:
            try:
                derivative_seed = derivative_seed.astype(float)
            except ValueError:
                raise TypeError('Input derivative seed array contains non int/float values')
            self._derivative = derivative_seed   
            self._dimensionality = len(derivative_seed)
        else:
            raise TypeError('Input derivative seed should be an int, float, or a 1D numpy array of ints/floats.')



    def __add__(self, other):
        """ 
        Dunder method for overloading the "+" operator. 
        Computes the value and the derivative of the summation operation
        
        INPUTS
        =======
        other: a Variable object, an int, or a float

        RETURNS
        ========
        a Variable object with the derivative and value of the summation operation.

        NOTES
        =====
        POST:
         - self is not changed by this function

        EXAMPLES
        =========

        # add two variables
        >>> x = Variable(4, 1)
        >>> y = Variable(4, 2)
        >>> print(x + y)
        Variable(value=8, derivative=3)
        
        # add a variable and a constant
        >>> x = Variable(2.1, 3.1)
        >>> print(x + 1)
        Variable(value=3.1, derivative=3.1)

        # add two variables with vector derivatives
        >>> import numpy as np
        >>> x = Variable(4, np.array([1, 3]))
        >>> y = Variable(4, np.array([2, 1]))
        >>> print(x + y)
        Variable(value=8, derivative=[3. 4.])
<<<<<<< HEAD

=======
        
>>>>>>> origin
        """
        try:
            val = self.value + other.value
            der = self.derivative + other.derivative
        except AttributeError:
            val = self.value + other
            der = self.derivative
        
        return Variable(val, der)


    def __radd__(self, other):
        """ 
        Dunder method for overloading the "+" operator. 
        Computes the value and derivative of the summation operation

        INPUTS
        =======
        other: a Variable object, an int, or a float

        RETURNS
        ========
        a Variable object with the derivative and value of the summation operation.

        NOTES
        =====
        POST:
         - self is not changed by this function
        
        EXAMPLES
        =========

        # add a constant and a variable
        >>> x = Variable(2.1, 3.1)
        >>> print(1 + x)
        Variable(value=3.1, derivative=3.1)

        # add a constant and a variable with vector derivative
        >>> import numpy as np
        >>> x = Variable(2.1, np.array([1, 0]))
        >>> print(1 + x)
        Variable(value=3.1, derivative=[1. 0.])

        """
        return self.__add__(other)


    def __mul__(self, other):
        """ 
        Dunder method for overloading the "*" operator. 
        Computes the value and derivative of the multiplication operation

        INPUTS
        =======
        other: a Variable object, an int, or a float

        RETURNS
        ========
        a Variable object with the derivative and value of the multiplication operation.

        NOTES
        =====
        POST:
         - self is not changed by this function

        EXAMPLES
        =========

        # multiply two variables
        >>> x = Variable(15, 1)
        >>> y = Variable(3, 1)
        >>> print(x * y)
        Variable(value=45, derivative=18)
        
        # multiply a variable and a constant
        >>> x = Variable(5.25, 3)
        >>> print(x * 4)
        Variable(value=21.0, derivative=12.0)
        
        # multiply two variables with vector derivatives
        >>> import numpy as np
        >>> x = Variable(3, np.array([1, 6]))
        >>> y = Variable(3, np.array([4, 1]))
        >>> print(x * y)
        Variable(value=9, derivative=[15. 21.])

        # multiply a variable with vector derivatives and a constant
        >>> import numpy as np
        >>> x = Variable(3, np.array([4, 1]))
        >>> print(x * 3)
        Variable(value=9, derivative=[12.  3.])

        """
        try:
            return Variable(self.value * other.value, self.value * other.derivative + other.value * self.derivative)
        except AttributeError:
            other = Variable(other, 0)
            return Variable(self.value * other.value, self.value * other.derivative + other.value * self.derivative)
    

    def __rmul__(self, other):
        """ 
        Dunder method for overloading the "*" operator. 
        Computes the value and derivative of the multiplication operation

        INPUTS
        =======
        other: a Variable object, an int, or a float

        RETURNS
        ========
        a Variable object with the derivative and value of the multiplication operation.

        NOTES
        =====
        POST:
         - self is not changed by this function
        
        EXAMPLES
        =========

        # multiply a constant and a variable
        >>> x = Variable(5.25, 3)
        >>> print(4 * x)
        Variable(value=21.0, derivative=12.0)

        # multiply a constant and a variable with vector derivatives
        >>> import numpy as np
        >>> x = Variable(3, np.array([4, 1]))
        >>> print(3 * x)
        Variable(value=9, derivative=[12.  3.])

        """
        return self.__mul__(other)


    def __sub__(self, other):
        """ 
        Dunder method for overloading the "-" operator. 
        Computes the value and derivative of the substraction operation

        INPUTS
        =======
        other: a Variable object, an int, or a float

        RETURNS
        ========
        a Variable object with the derivative and value of the substraction operation.

        NOTES
        =====
        POST:
         - self is not changed by this function
         
        EXAMPLES
        =========

        # substract two variables with scalar derivatives
        >>> x = Variable(2, 3)
        >>> y = Variable(4, 5)
        >>> print(x - y)
        Variable(value=-2, derivative=-2)
        
        # substract a variable with scalar derivative from a constant
        >>> x = Variable(5.2, 2.6)
        >>> print(x - 6.2)
        Variable(value=-1.0, derivative=2.6)
        
        # substract two variables with vector derivatives
        >>> import numpy as np
        >>> x = Variable(2, np.array([1, 3]))
        >>> y = Variable(4, np.array([6, 1]))
        >>> print(x - y)
        Variable(value=-2, derivative=[-5.  2.])
        
        # substract a constant from variable with vector derivatives
        >>> import numpy as np
        >>> x = Variable(2, np.array([6, 1]))
        >>> print(x - 3)
        Variable(value=-1, derivative=[6. 1.])

        """
        return self + (-other)
    

    def __rsub__(self, other):
        """ 
        Dunder method for overloading the "-" operator. 
        Computes the value and derivative of the substraction operation

        INPUTS
        =======
        other: a Variable object, an int, or a float

        RETURNS
        ========
        a Variable object with the derivative and value of the substraction operation.

        NOTES
        =====
        POST:
         - self is not changed by this function
         
        EXAMPLES
        =========

        # substract two variables with scalar derivatives
        >>> x = Variable(3, 3)
        >>> y = Variable(1, 5)
        >>> print(y - x)
        Variable(value=-2, derivative=2)
        
        # substract a variable with scalar derivative from a constant
        >>> x = Variable(2.1, 3.2)
        >>> print(-1.1 - x)
        Variable(value=-3.2, derivative=-3.2)
        
        # substract two variables with vector derivatives
        >>> import numpy as np
        >>> x = Variable(3, np.array([2, 3]))
        >>> y = Variable(1, np.array([-3, 1]))
        >>> print(y - x)
        Variable(value=-2, derivative=[-5. -2.])
        
        # substract a variable with vector derivatives from a constant
        >>> import numpy as np
        >>> x = Variable(1.5, np.array([1.3, 1]))
        >>> print(3.5 - x)
        Variable(value=2.0, derivative=[-1.3 -1. ])
        
        """
        return (-self) + other
    

    def __truediv__(self, other):
        """ 
        Dunder method for overloading the "/" operator. 
        Computes the value and derivative of the divison operation

        INPUTS
        =======
        other: a Variable object, an int, or a float

        RETURNS
        ========
        a Variable object with the derivative and value of the divison operation.

        NOTES
        =====
        PRE:
         -  other cannot be Zero a ZeroDivisionError will be raised.
        POST:
         - self is not changed by this function
        
        EXAMPLES
        =========

        # Divide two variables
        >>> x = Variable(15, 1)
        >>> y = Variable(3, 1)
        >>> print(x / y)
        Variable(value=5.0, derivative=-1.3333333333333333)
        
        # Divide a variable by a constant
        >>> x = Variable(20.0, 3)
        >>> print(x / 4)
        Variable(value=5.0, derivative=0.75)

        # Divide two variables with vector derivatives
        >>> import numpy as np
        >>> x = Variable(3, np.array([1, 6]))
        >>> y = Variable(3, np.array([4, 1]))
        >>> print(x / y)
        Variable(value=1.0, derivative=[-1.          1.66666667])

        # Divide a variable with vector derivatives by a constant
        >>> import numpy as np
        >>> x = Variable(3, np.array([4, 1]))
        >>> print(x / 3)
        Variable(value=1.0, derivative=[1.33333333 0.33333333])

        # ZeroDivisionError will be raised when constant is zero
        >>> x = Variable(3, 1)
        >>> x / 0
        Traceback (most recent call last):
            ...
        ZeroDivisionError: Division by zero encountered

        # ZeroDivisionError will be raised when variable is zero
        >>> x = Variable(3, 1)
        >>> y = Variable(0, 1)
        >>> x / y
        Traceback (most recent call last):
            ...
        ZeroDivisionError: Division by zero encountered
        
        """
        try:
            if other.value == 0:
                raise ZeroDivisionError("Division by zero encountered")
            return Variable(self.value / other.value, (other.value *  self.derivative - self.value * other.derivative) / (other.value ** 2))
        except AttributeError:
            if other == 0:
                raise ZeroDivisionError("Division by zero encountered")
            other = Variable(other, 0)
            return Variable(self.value / other.value, (other.value *  self.derivative - self.value * other.derivative) / (other.value ** 2))
    

    def __rtruediv__(self, other):
        """ 
        Dunder method for overloading the "/" operator. 
        Computes the value and derivative of the divison operation

        INPUTS
        =======
        other: a Variable object, an int, or a float

        RETURNS
        ========
        a Variable object with the derivative and value of the divison operation.

        NOTES
        =====
        PRE:
         -  self.value cannot be Zero a ZeroDivisionError will be raised.
        POST:
         - self is not changed by this function

        EXAMPLES
        =========

        # Divide two variables
        >>> x = Variable(3, 2)
        >>> y = Variable(15, 5)
        >>> print(y / x)
        Variable(value=5.0, derivative=-1.6666666666666667)
        
        # Divide a constant by a constant
        >>> x = Variable(20.0, 3)
        >>> print(100 / x)
        Variable(value=5.0, derivative=-0.75)

        # Divide two variables with vector derivatives
        >>> import numpy as np
        >>> x = Variable(3, np.array([1, 6]))
        >>> y = Variable(3, np.array([4, 1]))
        >>> print(y / x)
        Variable(value=1.0, derivative=[ 1.         -1.66666667])

        # Divide a constant by a variable with vector derivatives 
        >>> import numpy as np
        >>> x = Variable(3, np.array([4, 1]))
        >>> print(3 / x)
        Variable(value=1.0, derivative=[-1.33333333 -0.33333333])

        """
        try:
            if self.value == 0:
                raise ZeroDivisionError("Division by zero encountered")
            return Variable(other.value / self.value, (self.value * other.derivative - other.value * self.derivative) / (self.value ** 2))
        except AttributeError:
            other = Variable(other, 0)
            return Variable(other.value / self.value, (self.value * other.derivative - other.value * self.derivative) / (self.value ** 2))
    

    def __pow__(self, other):
        """
        Dunder method for overloading the "**" operator.
        Computes the value and derivative of the power operation.

        INPUTS
        =======
        other: a Variable object, an int, or a float

        RETURNS
        ========
        a Variable object with the derivative and value of the power operation.

        NOTES
        =====
        PRE:
        -  A ValueError is raised if self.value is negative and other is non-integer
        -  A ValueError is raised if self.value is zero and other is negative
        POST:
         - self is not changed by this function

        EXAMPLES
        =========

        # Power of variables with scalar derivatives
        >>> x = Variable(3, 3)
        >>> y = Variable(1, 5)
        >>> print(y ** x)
        Variable(value=1, derivative=15.0)

        # Power of Variable with scalar exponent.
        >>> x = Variable(2.1, 3.2)
        >>> print(x ** 2)
        Variable(value=4.41, derivative=13.440000000000001)

        # Power of Variable with vector derivative.
        >>> x = Variable(2.1, np.array([3.2, 2.5]))
        >>> print(x ** 2)
        Variable(value=4.41, derivative=[13.44 10.5 ])

        # Power of Variable with vector derivative.
        >>> x = Variable(2.1, np.array([3.2, 2.5]))
        >>> y = Variable(5, np.array([0.4, 9.6]))
        >>> print(x ** y)
        Variable(value=40.84101000000001, derivative=[323.29018821 533.99536695])

        """
        try:
            val = self.value ** other.value
            intermediate_value = other * np.log(self)
            der = val * intermediate_value.derivative
            return Variable(val, der)
        except AttributeError:
            if self.value < 0 and other % 1 != 0:
                raise ValueError("Cannot raise a negative number to the power of a non-integer value.")
            if self.value == 0 and other < 1:
                raise ValueError("Power function does not have a derivative at 0 if the exponent is less than 1.")
            val = self.value ** other
            der = self.derivative * other * self.value ** (other - 1)
            return Variable(val, der)


    def __rpow__(self, other):
        """
        Dunder method for overloading the "**" operator.
        Computes the value and derivative of the power operation.

        INPUTS
        =======
        other: a Variable object, an int, or a float

        RETURNS
        ========
        a Variable object with the derivative and value of the power operation.

        NOTES
        =====
        PRE:
         -  ValueError is raised if other is zero and self.value is negative
         -  ValueError is raised if other is negative
        POST:
         - self is not changed by this function

        EXAMPLES
        =========

        # Power of variables with scalar derivatives
        >>> x = Variable(3, np.array([5, 6]))
        >>> print(3 ** x)
        Variable(value=27, derivative=[148.31265897 177.97519076])

        """
        if other == 0 and self.value <= 0:
            raise ValueError("Derivative of 0^x is undefined for non-positive x values")
        if other < 0:
            raise ValueError("Values and derivatives of a^x for a<0 are not defined in the real number domain")
        val = other ** self.value
        der = np.log(other) * val * self.derivative
        return Variable(val, der)
    

    def __neg__(self):
        """ 
        This method is called using '-' operator.
        Computes the value and derivative of the negation operation

        INPUTS
        =======
        None

        RETURNS
        ========
        a Variable object with the derivative and value of the negation operation.

        NOTES
        =====
        POST:
         - self is not changed by this function
         
        EXAMPLES
        =========

        # negation of a variable with scalar derivative
        >>> x = Variable(4.2, 1.3)
        >>> print(-x)
        Variable(value=-4.2, derivative=-1.3)

        # negation of a variable with vector derivative
        >>> import numpy as np
        >>> x = Variable(1.7, np.array([-2, 3]))
        >>> print(-x)
        Variable(value=-1.7, derivative=[ 2. -3.])

        """
        val = (-1) * self.value 
        der = (-1) * self.derivative
        return Variable(val, der)
    

    def log(self, base=None):
        """
        Computes the value and derivative of log function with any base. Default base is e.

        INPUTS
        =======
        base: an int, or a float. Default is None.

        RETURNS
        ========
        a Variable object with the derivative and value of the log function.

        NOTES
        =====
        POST:
         - self is not changed by this function
         
        EXAMPLES
        =========

        # log(base=5) of a variable with scalar derivative
        >>> x = Variable(4.2, 1.3)
        >>> print(x.log(5))
        Variable(value=0.891668149608153, derivative=0.19231795593511794)

        # log(base=e) of a variable with vector derivative
        >>> import numpy as np
        >>> x = Variable(1.7, np.array([-2, 3]))
        >>> print(x.log())
        Variable(value=0.5306282510621704, derivative=[-1.17647059  1.76470588])
        
        # ValueError will be raised if self.value is less than or equal to zero.
        >>> x = Variable(-2, 2)
        >>> print(x.log(2))
        Traceback (most recent call last):
            ...
        ValueError: Values for log should be greater than zero.
        
        # ValueError will be raised if base is less than or equal to zero.
        >>> x = Variable(2, -3)
        >>> print(x.log(-2))
        Traceback (most recent call last):
            ...
        ValueError: Base should be greater than zero and not equal to 1.
        
        # ValueError will be raised if base is equal to one.
        >>> x = Variable(5, -3)
        >>> print(x.log(1))
        Traceback (most recent call last):
            ...
        ValueError: Base should be greater than zero and not equal to 1.
        
        """
        if self.value <= 0.0:
            raise ValueError('Values for log should be greater than zero.')
        if base is None:
            val = np.log(self.value)
            der = self.derivative * (1/self.value)
            return Variable(val, der)
        else:
            if base <= 0.0 or base == 1:
                raise ValueError('Base should be greater than zero and not equal to 1.')
            
            val = np.log(self.value)/np.log(base)
            der = self.derivative * (1/(self.value * np.log(base)))
            return Variable(val, der)
        

    def exp(self):
        """
        Computes the value and derivative of exp function

        INPUTS
        =======
        None

        RETURNS
        ========
        a Variable object with the derivative and value of the exp function.

        NOTES
        =====
        POST:
         - self is not changed by this function

        EXAMPLES
        =========

        # exp of variable with scalar derivative
        >>> import numpy as np
        >>> x = Variable(4, 1)
        >>> print(np.exp(x))
        Variable(value=54.598150033144236, derivative=54.598150033144236)

        # exp of variable with vector derivative
        >>> import numpy as np
        >>> x = Variable(3, np.array([1, -4]))
        >>> print(np.exp(x))
        Variable(value=20.085536923187668, derivative=[ 20.08553692 -80.34214769])

        """
        val = np.exp(self.value)
        der = self.derivative * np.exp(self.value)
        return Variable(val, der)
    

    def sqrt(self):
        """
        Computes the value and derivative of sqrt function

        INPUTS
        =======
        None

        RETURNS
        ========
        a Variable object with the derivative and value of the sqrt function.

        NOTES
        =====
        POST:
         - self is not changed by this function

        EXAMPLES
        =========

        # sqrt of variable with scalar derivative
        >>> import numpy as np
        >>> x = Variable(4, 1)
        >>> print(np.sqrt(x))
        Variable(value=2.0, derivative=0.25)

        # sqrt of variable with vector derivative
        >>> import numpy as np
        >>> x = Variable(3, np.array([1, -4]))
        >>> print(np.sqrt(x))
        Variable(value=1.7320508075688772, derivative=[ 0.28867513 -1.15470054])
<<<<<<< HEAD
        
=======

>>>>>>> origin
        """
        return self.__pow__(0.5)
    

    def sin(self):
        """ 
        Computes the value and derivative of the sin function

        INPUTS
        =======
        None

        RETURNS
        ========
        a Variable object with the derivative and value of the sin function.
        
        NOTES
        =====
        POST:
         - self is not changed by this function
        
        EXAMPLES
        =========

        # sin of variable with scalar derivative
        >>> import numpy as np
        >>> x = Variable(np.pi/2, 1)
        >>> print(np.sin(x))
        Variable(value=1.0, derivative=6.123233995736766e-17)
        
        # sin of variable with vector derivative
        >>> import numpy as np
        >>> x = Variable(np.pi/2, np.array([1, 0]))
        >>> print(np.sin(x))
        Variable(value=1.0, derivative=[6.123234e-17 0.000000e+00])
<<<<<<< HEAD
        
=======

>>>>>>> origin
        """

        val = np.sin(self.value)
        der = np.cos(self.value) * self.derivative
        return Variable(val, der)
    
    
    def cos(self):
        """ 
        Computes the value and derivative of the cos function
        
        INPUTS
        =======
        None

        RETURNS
        ========
        a Variable object with the derivative and value of the cos function.

        NOTES
        =====
        POST:
         - self is not changed by this function
         
        EXAMPLES
        =========

        # cos of variable with scalar derivative
        >>> import numpy as np
        >>> x = Variable(np.pi/2, 2)
        >>> print(np.cos(x))
        Variable(value=6.123233995736766e-17, derivative=-2.0)
        
        # cos of variable with vector derivative
        >>> import numpy as np
        >>> x = Variable(np.pi/2, np.array([1, 3]))
        >>> print(np.cos(x))
        Variable(value=6.123233995736766e-17, derivative=[-1. -3.])
        
        """
        
        val = np.cos(self.value)
        der = -np.sin(self.value) * self.derivative
        return Variable(val, der)
    
    
    def tan(self):
        """ 
        Computes the value and derivative of the tan function

        INPUTS
        =======
        None

        RETURNS
        ========
        a Variable object with the derivative and value of the tan function.

        NOTES
        =====
        PRE:
         -  self.value is not an odd multiple of pi/2 otherwise a ValueError will be raised
        POST:
         - self is not changed by this function

        EXAMPLES
        =========

        # tan of variable with scalar derivative
        >>> import numpy as np
        >>> x = Variable(np.pi, 1)
        >>> print(np.tan(x))
        Variable(value=-1.2246467991473532e-16, derivative=1.0)
        
        # tan of variable with vector derivative
        >>> import numpy as np
        >>> x = Variable(np.pi/4, np.array([1, 0]))
        >>> print(np.tan(x))
        Variable(value=0.9999999999999999, derivative=[2. 0.])

        """
        if (self.value / (np.pi/2)) % 2 == 1:
            raise ValueError("Inputs to tan should not be odd multiples of pi/2")

        val = np.tan(self.value)
        der = self.derivative / np.cos(self.value)**2
        return Variable(val, der)


    def sinh(self):
        """ 
        Computes the value and derivative of the sinh function

        INPUTS
        =======
        None

        RETURNS
        ========
        a Variable object with the derivative and value of the sinh function.

        NOTES
        =====
        POST:
         - self is not changed by this function
        
        EXAMPLES
        =========
        # sinh of variable with scalar derivative
        >>> import numpy as np
        >>> x = Variable(2, 1)
        >>> print(np.sinh(x))
        Variable(value=3.6268604078470186, derivative=3.7621956910836314)
        
        # sinh of variable with vector derivative
        >>> import numpy as np
        >>> x = Variable(3, np.array([1, 1]))
        >>> print(np.sinh(x))
        Variable(value=10.017874927409903, derivative=[10.067662 10.067662])

        """
        val = np.sinh(self.value)
        der = np.cosh(self.value) * self.derivative
        return Variable(val, der)
    

    def cosh(self):
        """ 
        Computes the value and derivative of the cosh function

        INPUTS
        =======
        None

        RETURNS
        ========
        a Variable object with the derivative and value of the cosh function.
        
        NOTES
        =====
        POST:
         - self is not changed by this function
         
        EXAMPLES
        =========
        # cosh of variable with scalar derivative
        >>> import numpy as np
        >>> x = Variable(2, 2)
        >>> print(np.cosh(x))
        Variable(value=3.7621956910836314, derivative=7.253720815694037)
        
        # cosh of variable with vector derivative
        >>> import numpy as np
        >>> x = Variable(1.3, np.array([1, 3]))
        >>> print(np.cosh(x))
        Variable(value=1.9709142303266285, derivative=[1.69838244 5.09514731])

        """
        val = np.cosh(self.value)
        der = np.sinh(self.value) * self.derivative
        return Variable(val, der)
    

    def tanh(self):
        """ 
        Computes the value and derivative of the tanh function

        INPUTS
        =======
        None

        RETURNS
        ========
        a Variable object with the derivative and value of the tanh function.

        NOTES
        =====
        POST:
         - self is not changed by this function

        EXAMPLES
        =========

        # tanh of variable with scalar derivative
        >>> import numpy as np
        >>> x = Variable(2, 1)
        >>> print(np.tanh(x))
        Variable(value=0.9640275800758169, derivative=0.07065082485316447)
        
        # tanh of variable with vector derivative
        >>> import numpy as np
        >>> x = Variable(3, np.array([4, 1]))
        >>> print(np.tanh(x))
        Variable(value=0.9950547536867305, derivative=[0.03946415 0.00986604])

        """
        val = np.tanh(self.value)
        der = 1 / (np.cosh(self.value)**2) * self.derivative
        return Variable(val, der)
    

    def arcsin(self):
        """ 
        Computes the value and derivative of the arcsin function

        INPUTS
        =======
        None

        RETURNS
        ========
        a Variable object with the derivative and value of the arcsin function.

        NOTES
        =====
        PRE:
         - self.value should be in (-1, 1), otherwise a ValueError will be raised
        POST:
         - self is not changed by this function

        EXAMPLES
        =========

        # arcsin of variable with scalar derivative
        >>> import numpy as np
        >>> x = Variable(0.5, 1)
        >>> print(np.arcsin(x))
        Variable(value=0.5235987755982988, derivative=1.1547005383792517)
        
        # arcsin of variable with vector derivative
        >>> import numpy as np
        >>> x = Variable(-0.5, np.array([0, 1]))
        >>> print(np.arcsin(x))
        Variable(value=-0.5235987755982988, derivative=[0.         1.15470054])
        
        # ValueError will be raised if self.value is not in (-1, 1)
        >>> import numpy as np
        >>> x = Variable(3, 1)
        >>> print(np.arcsin(x))
        Traceback (most recent call last):
            ...
        ValueError: Inputs to arcsin should be in (-1, 1) for the derivative to be defined.

        """

        if self.value >= 1 or self.value <= -1:
            raise ValueError("Inputs to arcsin should be in (-1, 1) for the derivative to be defined.")
        
        val = np.arcsin(self.value)
        der = self.derivative / np.sqrt(1-self.value**2)
        return Variable(val, der)
    

    def arccos(self):
        """ 
        Computes the value and derivative of the arccos function

        INPUTS
        =======
        None

        RETURNS
        ========
        a Variable object with the derivative and value of the arccos function.

        NOTES
        =====
        PRE:
         - self.value should be in (-1, 1), otherwise a ValueError will be raised
        POST:
         - self is not changed by this function
         
        EXAMPLES
        =========
        # arccos of variable with scalar derivative
        >>> import numpy as np
        >>> x = Variable(0.5, 0.1)
        >>> print(np.arccos(x))
        Variable(value=1.0471975511965976, derivative=-0.11547005383792516)
        
        # arccos of variable with vector derivative
        >>> import numpy as np
        >>> x = Variable(-0.4, np.array([1, 1]))
        >>> print(np.arccos(x))
        Variable(value=1.9823131728623846, derivative=[-1.09108945 -1.09108945])
        
        # ValueError will be raised if self.value is not in (-1, 1)
        >>> import numpy as np
        >>> x = Variable(2, 0.1)
        >>> print(np.arccos(x))
        Traceback (most recent call last):
            ...
        ValueError: Inputs to arccos should be in (-1, 1) for the derivative to be defined.
        
        """
        
        if self.value >= 1 or self.value <= -1:
            raise ValueError("Inputs to arccos should be in (-1, 1) for the derivative to be defined.")
        val = np.arccos(self.value)
        der = (-1) * self.derivative / np.sqrt(1-self.value**2)
        return Variable(val,der)


    def arctan(self):
        """ 
        Computes the value and derivative of the arctan function

        INPUTS
        =======
        None

        RETURNS
        ========
        a Variable object with the derivative and value of the arctan function.

        NOTES
        =====
        POST:
         - self is not changed by this function

        EXAMPLES
        =========
        # arctan of variable with scalar derivative
        >>> import numpy as np
        >>> x = Variable(2, 1)
        >>> print(np.arctan(x))
        Variable(value=1.1071487177940906, derivative=0.2)
        
        # arctan of variable with vector derivative
        >>> import numpy as np
        >>> x = Variable(3, np.array([4, 1]))
        >>> print(np.arctan(x))
        Variable(value=1.2490457723982544, derivative=[0.4 0.1])

        """
        val = np.arctan(self.value)
        der = 1 / (1 + self.value**2) * self.derivative
        return Variable(val, der)


    def __abs__(self):
        """
        Dunder method for overloading the abs function.
        Computes the value and derivative of abs function

        INPUTS
        =======
        None

        RETURNS
        ========
        a Variable object with the derivative and value of the abs function.

        NOTES
        =====
        PRE:
         -  self.value is not 0 otherwise a ValueError will be raised
        POST:
         - self is not changed by this function

        EXAMPLES
        =========

        # abs of variable with scalar derivative
        >>> x = Variable(4, 1)
        >>> print(abs(x))
        Variable(value=4, derivative=1.0)

        # abs of variable with vector derivative
        >>> import numpy as np
        >>> x = Variable(3, np.array([1, -4]))
        >>> print(abs(x))
        Variable(value=3, derivative=[ 1. -4.])

        # ValueError will be raised if self.value is equal to 0
        >>> x = Variable(0, -0.6)
        >>> print(abs(x))
        Traceback (most recent call last):
            ...
        ValueError: Abs function derivative does not exist at 0

        """
        if self.value != 0.0:
            val = abs(self.value)
            der = self.derivative * (self.value / val)
            return Variable(val, der)
        else:
            raise ValueError('Abs function derivative does not exist at 0')
    
    def __lt__(self, other):
        """
        Dunder method for overloading the less than comparison.
        This operand will perform elementwise comparison of the value and 
        derivative of self and other.

        INPUTS
        =======
        other: a Variable object

        RETURNS
        ========
        a boolean tuple where the first element specifies if the comparison holds
        for the value of self and the second element specifies if the comparison
        holds for all the elements of the derivative

        NOTES
        =====
        POST:
         - self is not changed by this function

        EXAMPLES
        =========

        # "less than" comparison when the comparison is true only for the derivative
        >>> x = Variable(4, 1)
        >>> y = Variable(4, 2)
        >>> x < y
        (False, True)
        
        # "less than" comparison when the comparison is true for some of the derivative elements
        >>> import numpy as np
        >>> x = Variable(4, np.array([1, 3]))
        >>> y = Variable(5, np.array([3, 2]))
        >>> x < y
        (True, False)

        # "less than" comparison when the comparison is true for all of the derivative elements
        >>> import numpy as np
        >>> x = Variable(4, np.array([1, 3]))
        >>> y = Variable(6, np.array([6, 6]))
        >>> x < y
        (True, True)

        """
        val_comparison = self.value < other.value
        try:
            der_comparison = all(self.derivative < other.derivative)
        except TypeError:
            der_comparison = self.derivative < other.derivative
        
        return (val_comparison, der_comparison)

    
    def __le__(self, other):
        """
        Dunder method for overloading the less than or equal to comparison.
        This operand will perform elementwise comparison of the value and 
        derivative of self and other.

        INPUTS
        =======
        other: a Variable object

        RETURNS
        ========
        a boolean tuple where the first element specifies if the comparison holds
        for the value of self and the second element specifies if the comparison
        holds for all the elements of the derivative

        NOTES
        =====
        POST:
         - self is not changed by this function

        EXAMPLES
        =========

        # <= comparison with scalar derivative
        >>> x = Variable(4, 1)
        >>> y = Variable(4, 2)
        >>> x <= y
        (True, True)
        
        # <= comparison when the comparison is true for some of the derivative elements
        >>> import numpy as np
        >>> x = Variable(4, np.array([1, 3]))
        >>> y = Variable(5, np.array([3, 2]))
        >>> x <= y
        (True, False)

        # <= comparison when the comparison is true for all of the derivative elements
        >>> import numpy as np
        >>> x = Variable(4, np.array([1, 3]))
        >>> y = Variable(4, np.array([4, 4]))
        >>> x <= y
        (True, True)
<<<<<<< HEAD

=======
        
>>>>>>> origin
        """
        val_comparison = self.value <= other.value
        try:
            der_comparison = all(self.derivative <= other.derivative)
        except TypeError:
            der_comparison = self.derivative <= other.derivative
        
        return (val_comparison, der_comparison)
    
    def __eq__(self, other):
        """
        Dunder method for overloading the equal to comparison.
        This operand will perform elementwise comparison of the 
        value and derivative of self and other.
        
        INPUTS
        =======
        other: a Variable object
        
        RETURNS
        ========
        a boolean tuple where the first element specifies if the comparison holds
        for the value of self and the second element specifies if the comparison
        holds for all the elements of the derivative
        
        NOTES
        =====
        POST:
         - self is not changed by this function

        EXAMPLES
        =========
        # == comparison with scalar derivative
        >>> x = Variable(3, 1)
        >>> y = Variable(3, 2)
        >>> x == y
        (True, False)
        
        # == comparison when the comparison is true for some of the derivative elements
        >>> import numpy as np
        >>> x = Variable(2, np.array([3, 3]))
        >>> y = Variable(2, np.array([3, 2]))
        >>> x == y
        (True, False)
        
        # == comparison when the comparison is true for all of the derivative elements
        >>> import numpy as np
        >>> x = Variable(4, np.array([3, 3]))
        >>> y = Variable(4, np.array([3, 3]))
        >>> x == y
        (True, True)

        """
        val_comparison = self.value == other.value
        try:
            der_comparison = all(self.derivative == other.derivative)
        except TypeError:
            der_comparison = self.derivative == other.derivative
            
        return (val_comparison, der_comparison)

    def __ne__(self, other):
        """
        Dunder method for overloading the not equal to comparison.
        This operand will perform elementwise comparison of the
        value and derivative of self and other.
        
        INPUTS
        =======
        other: a Variable object
        
        RETURNS
        ========
        a boolean tuple where the first element specifies if the inequality holds
        for the value of self and the second element specifies if the inequality
        holds for any of the elements of the derivative
        
        NOTES
        =====
        POST:
         - self is not changed by this function
         
        EXAMPLES
        =========

        # != comparison with scalar derivative
        >>> x = Variable(5, 3)
        >>> y = Variable(5, 2)
        >>> x != y
        (False, True)

        # != comparison when some vector elements in derivative are not equal.
        >>> import numpy as np
        >>> x = Variable(2, np.array([3, 3]))
        >>> y = Variable(2, np.array([3, 2]))
        >>> x != y
        (False, True)

        # != comparison when all vector elements in derivative are the same.
        >>> import numpy as np
        >>> x = Variable(4, np.array([3, 3]))
        >>> y = Variable(4, np.array([3, 3]))
        >>> x != y
        (False, False)
        
        """
        val_comparison = self.value != other.value
        try:
            der_comparison = any(self.derivative != other.derivative)
        except TypeError:
            der_comparison = self.derivative != other.derivative

        return val_comparison, der_comparison


    def __gt__(self, other):
        """
        Dunder method for overloading the greater than comparison.
        This operand will perform elementwise comparison of the value and 
        derivative of self and other.

        INPUTS
        =======
        other: a Variable object

        RETURNS
        ========
        a boolean tuple where the first element specifies if the comparison holds
        for the value of self and the second element specifies if the comparison
        holds for all the elements of the derivative

        NOTES
        =====
        POST:
         - self is not changed by this function
        
        EXAMPLES
        =========

        # "greater than" comparison when the comparison is true only for the derivative
        >>> x = Variable(3, 7)
        >>> y = Variable(5, 2)
        >>> x > y
        (False, True)
        
        # "greater than" comparison when the comparison is true for some of the derivative elements
        >>> import numpy as np
        >>> x = Variable(2, np.array([1, 3]))
        >>> y = Variable(1, np.array([3, 2]))
        >>> x > y
        (True, False)

        # "greater than" comparison when the comparison is true for all of the derivative elements
        >>> import numpy as np
        >>> x = Variable(7, np.array([5, 6]))
        >>> y = Variable(3, np.array([4, 4]))
        >>> x > y
        (True, True)

        """
        val_comparison = self.value > other.value
        try:
            der_comparison = all(self.derivative > other.derivative)
        except TypeError:
            der_comparison = self.derivative > other.derivative
        
        return (val_comparison, der_comparison)
      
    def __ge__(self, other):
        """
        Dunder method for overloading the greater than or equal to comparison.
        This operand will perform elementwise comparison of the value and 
        derivative of self and other.
        
        =======
        other: a Variable object

        RETURNS
        ========

        a boolean tuple where the first element specifies if the comparison holds
        for the value of self and the second element specifies if the comparison
        holds for all the elements of the derivative

        NOTES
        =====
        POST:
         - self is not changed by this function

        EXAMPLES
        =========

        # >= comparison with scalar derivative
        >>> x = Variable(7, 2)
        >>> y = Variable(4, 2)
        >>> x >= y
        (True, True)
        
        # >= comparison when the comparison is true for some of the derivative elements
        >>> import numpy as np
        >>> x = Variable(4, np.array([1, 3]))
        >>> y = Variable(4, np.array([3, 2]))
        >>> x >= y
        (True, False)

        # >= comparison when the comparison is true for all of the derivative elements
        >>> import numpy as np
        >>> x = Variable(4, np.array([9, 7]))
        >>> y = Variable(4, np.array([4, 7]))
        >>> x >= y
        (True, True)

        """
        val_comparison = self.value >= other.value
        try:
            der_comparison = all(self.derivative >= other.derivative)
        except TypeError:
            der_comparison = self.derivative >= other.derivative
        
        return (val_comparison, der_comparison)

    def logistic(self):
        """
        Computes the value and derivative of the standard logistic function of the form 1/(1 + e^-x).

        INPUTS
        =======
        None

        RETURNS
        ========
        a Variable object with the derivative and value of the logistic function.

        NOTES
        =====
        POST:
         - self is not changed by this function

        EXAMPLES
        =========

        # logistic function with scalar derivative
        >>> x = Variable(3, 1)
        >>> y = x.logistic()
        >>> print(y)
        Variable(value=0.9525741268224334, derivative=0.045176659730912144)

        # logistic function with vector derivative
        >>> import numpy as np
        >>> x = Variable(2, np.array([3, 3]))
        >>> print(x.logistic())
        Variable(value=0.8807970779778823, derivative=[0.31498076 0.31498076])

        """
        return 1/(1 + np.exp(-self))
        