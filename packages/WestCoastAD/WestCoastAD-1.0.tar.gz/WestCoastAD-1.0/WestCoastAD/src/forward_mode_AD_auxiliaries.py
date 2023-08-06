"""
This file provides several auxiliary functions that assist users in working with WestCoastAD's
automatic differentiation module.
"""
import numpy as np
import numbers

from WestCoastAD import Variable


def vector_function_jacobian(vector_function):
    """
    Function that returns the jacobian of the given vector valued function as a 
    single numpy array

    INPUTS
    =======
    vector_function: a 1D numpy array (size n) of multi or uni variate functions defined in
    terms of WestCoastAD variables

    RETURNS
    ========
    The Jacobian of the vector function as an n by d matrix where n is the size of the
    input array and d is the dimensionality of the derivative of individual Variables in
    the input array. 

    NOTES
    =====
    PRE:
     - vector_function elements must be of the type WestCoastAD.Variable class
     - vector_function elements must have the same dimensionality (ie. their derivative dimensions must match).
       multivariate_dimension_check can be used to check the dimensionality constraint is satisfied 
    
    EXAMPLES
    =========

    >>> import numpy as np
    >>> from WestCoastAD import Variable
    >>> x = Variable(4, np.array([1, 0]))
    >>> y = Variable(3, np.array([0, 1]))
    >>> vector_function_jacobian(np.array([x+y, y**2, x*y]))
    array([[1., 1.],
           [0., 6.],
           [3., 4.]])
    
    >>> import numpy as np
    >>> from WestCoastAD import Variable
    >>> x = Variable(4, 1)
    >>> vector_function_jacobian(np.array([np.sin(x), x/2, np.sqrt(x)]))
    array([[-0.65364362],
           [ 0.5       ],
           [ 0.25      ]])

    """
    jacobian = np.array([func.derivative for func in vector_function])
    if len(jacobian.shape) == 1:
        jacobian = jacobian.reshape(-1, 1)
    return jacobian


def vector_function_value(vector_function):
    """
    Function that returns the value of the given vector valued function as a 
    single numpy array

    INPUTS
    =======
    vector_function: a 1D numpy array (size n) of multi or uni variate functions defined in
    terms of WestCoastAD variables

    RETURNS
    ========
    The  value of the vector function as an array of size n

    NOTES
    =====
    PRE:
     - vector_function elements must be of the type WestCoastAD.Variable class
     - vector_function elements must have the same dimensionality (ie. their derivative dimensions must match).
       multivariate_dimension_check can be used to check the dimensionality constraint is satisfied 
    
    EXAMPLES
    =========

    >>> import numpy as np
    >>> from WestCoastAD import Variable
    >>> x = Variable(4, np.array([1, 0]))
    >>> y = Variable(3, np.array([0, 1]))
    >>> vector_function_value(np.array([x+y, y**2, x*y]))
    array([ 7,  9, 12])

    >>> import numpy as np
    >>> from WestCoastAD import Variable
    >>> x = Variable(4, 1)
    >>> vector_function_value(np.array([x, x/2]))
    array([4., 2.])

    """
    return np.array([func.value for func in vector_function])


def multivariate_dimension_check(variables):
    """
    Function that checks whether the derivatives of the variable classes have the same
    dimensionality

    INPUTS
    =======
    variables: a 1D numpy array or a list (size n) of WestCoastAD variable instances

    RETURNS
    ========
    True if the dimensions of all the variables match, else False

    NOTES
    =====
    PRE:
     - variables' elements must be of the type WestCoastAD.Variable class
     - variables must have length greater than zero otherwise a ValueError will be raised
    
    EXAMPLES
    =========

    # mismatched dimensions with list input
    >>> from WestCoastAD import Variable
    >>> x = Variable(4, np.array([1, 0]))
    >>> y = Variable(3, np.array([0, 1, 0]))
    >>> multivariate_dimension_check([x, y])
    False

    # matched dimensions with array input
    >>> import numpy as np
    >>> from WestCoastAD import Variable
    >>> x = Variable(4, np.array([1, 0, 0]))
    >>> y = Variable(3, np.array([0, 1, 0]))
    >>> multivariate_dimension_check(np.array([x, y]))
    True

    """
    
    if len(variables) < 1:
        raise ValueError("variable_list must have at least one variable.")
    derivative_dim = variables[0]._dimensionality
    for variable in variables:
        if variable._dimensionality != derivative_dim:
            return False
    return True


def differentiate(func, variable_values, scalar=True):
    """
    Function that can be used to differentiate scalar and vector functions of one or more 
    variables. 

    INPUTS
    =======
    - func: a python function that takes as input a single vector or one or more scalars and
        returns a 1D numpy array of functions if func is a vector function or a single function
        if func is a scalar function.
    - variable_values: a 1D numpy array of floats/ints giving the values of the input variables to func
    - scalar: True if the inputs to func are one or more scalars otherwise False; Default is True


    RETURNS
    ========
    - the value of func evaluated at variable_values (a numpy array for vector functions and a 
         scalar for scalar functions)
    - the first derivative/gradient/jacobian of func evaluated at variable_values (a numpy array of
        size n by d where n is the number of functions and d is the number of variables)

    NOTES
    =====
    PRE:
     - func must only use operations that are supported by WestCoastAD's Variable class
     - variable_values has the same length as the number of inputs to func if func takes scalar inputs, or
       the length of the vector input to func.
     - variable_values must be in the same order as the inputs to func
    
    EXAMPLES
    =========

    # Derivative computation for a univariate scalar functions
    >>> import numpy as np
    >>> func = lambda x: 3*x**2 + 3
    >>> differentiate(func, np.ones(1))
    (6.0, array([6.]))

    # Derivative computation for a multivariate scalar functions
    >>> import numpy as np
    >>> func = lambda x, y: 3*x**2 + 3/y
    >>> differentiate(func, np.array([1, 3]))
    (4.0, array([ 6.        , -0.33333333]))

    # alternatively giving the input as a vector:
    >>> import numpy as np
    >>> func = lambda x: 3*x[0]**2 + 3/x[1]
    >>> differentiate(func, np.array([1, 3]), scalar=False)
    (4.0, array([ 6.        , -0.33333333]))

    # Derivative computation for a univariate vector functions
    >>> import numpy as np
    >>> func = lambda x: np.array([x*2, x, x.log(base=2)])
    >>> val, der = differentiate(func, np.array([2]))
    >>> val
    array([4., 2., 1.])
    >>> der
    array([[2.        ],
           [1.        ],
           [0.72134752]])

    # Derivative computation for a multivariate vector functions
    >>> import numpy as np
    >>> func = lambda x, y: np.array([x*y, x-y, x.log(base=2)])
    >>> val, der = differentiate(func, np.array([1, 3]))
    >>> val
    array([ 3., -2.,  0.])
    >>> der 
    array([[ 3.        ,  1.        ],
           [ 1.        , -1.        ],
           [ 1.44269504,  0.        ]])

    # alternatively giving the input as a vector:
    >>> import numpy as np
    >>> func = lambda x: np.array([x[0]*x[1], x[0]-x[1], x[0].log(base=2)])
    >>> val, der = differentiate(func, np.array([1, 3]), scalar=False)
    >>> val
    array([ 3., -2.,  0.])
    >>> der
    array([[ 3.        ,  1.        ],
           [ 1.        , -1.        ],
           [ 1.44269504,  0.        ]])


    """

    num_variables = len(variable_values)

    def _generate_seed_derivative(index):
        """
        This is an inner function used for generating standard unit vectors to represent seed derivatives of
        the variables of the objective function.
        """
        seed_derivative = np.zeros(num_variables)
        seed_derivative[index] = 1.0
        return seed_derivative
    
    
    variables = [Variable(variable_values[i], _generate_seed_derivative(i)) for i in range(num_variables)]
    result = func(*variables) if scalar else func(variables)

    try:
        return result.value, result.derivative
    except AttributeError:
        return vector_function_value(result), vector_function_jacobian(result)