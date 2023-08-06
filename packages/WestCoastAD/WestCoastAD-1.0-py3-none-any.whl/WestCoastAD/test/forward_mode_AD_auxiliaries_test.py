import unittest
import numpy as np

from WestCoastAD import Variable
from WestCoastAD import vector_function_jacobian, vector_function_value, multivariate_dimension_check, differentiate

class AuxiliariesUnitTest(unittest.TestCase):

    def test_vector_function_polynomial_multivariate(self):
        x = Variable(2, np.array([1, 0, 0]))
        y = Variable(3, np.array([0, 1, 0]))
        z = Variable(1, np.array([0, 0, 1]))

        f_1 = x + y + z
        f_2 = x**2*y

        f = np.array([f_1, f_2])
        f_value = vector_function_value(f)
        f_jac = vector_function_jacobian(f)

        x = 2
        y = 3
        z = 1

        self.assertAlmostEqual(f_value[0], x + y + z)
        self.assertAlmostEqual(f_value[1], x**2*y)
        np.testing.assert_array_almost_equal(f_jac, np.array([[1, 1, 1], [2*x*y, x**2, 0]]))
    
    def test_vector_function_polynomial_univariate(self):
        x = Variable(1, 1)

        f_1 = x.sin()
        f_2 = x.cos().log(base=2)
        f_3 = 1/x

        f = np.array([f_1, f_2, f_3])
        f_value = vector_function_value(f)
        f_jac = vector_function_jacobian(f)

        x = 1
        
        np.testing.assert_array_almost_equal(f_value, np.array([np.sin(x), np.log2(np.cos(x)), 1/x]))
        np.testing.assert_array_almost_equal(f_jac, np.array([[np.cos(x)], [-np.tan(x)/np.log(2)], [-1/x**2]]))

        f_value = vector_function_value(np.array([f_1]))
        f_jac = vector_function_jacobian(np.array([f_1]))
        
        np.testing.assert_array_almost_equal(f_value, np.array([np.sin(x)]))
        np.testing.assert_array_almost_equal(f_jac, np.array([[np.cos(x)]]))
    

    def test_multivariate_dimension_check(self):
        x = Variable(2, np.array([1, 0, 0]))
        y = Variable(3, np.array([0, 1, 1]))
        z = Variable(1, np.array([0, 0, 1, 0]))
        self.assertFalse(multivariate_dimension_check([x,y,z]))

        x = Variable(2, np.array([1, 0]))
        y = Variable(3, np.array([0, 1, 1]))
        z = Variable(1, np.array([0, 0, 1]))
        self.assertFalse(multivariate_dimension_check([x,y,z]))

        x = Variable(2, np.array([1, 0]))
        y = Variable(3, np.array([0, 1]))
        z = Variable(1, np.array([0, 1]))
        self.assertTrue(multivariate_dimension_check([x,y,z]))

        x = Variable(2, np.array([1, 0]))
        self.assertTrue(multivariate_dimension_check([x]))

        x = Variable(2, 1)
        y = Variable(3, 1)
        z = Variable(1, 1)
        self.assertTrue(multivariate_dimension_check([x,y,z]))
    
    
    def test_multivariate_dimension_check_exception(self):
        with self.assertRaises(ValueError) as e:
            multivariate_dimension_check([])
        self.assertEqual('variable_list must have at least one variable.', str(e.exception))

    
    def test_differentiate_univariate_scalar_function(self):
        def func(x):
            return 3*x**2 + 4/x + np.sin(x**2)
        
        val, der = differentiate(func, np.array([2]))
        x = 2
        self.assertAlmostEqual(val, func(x))
        derivative_expected = np.array([6*x - 4/x**2 + np.cos(x**2)*2*x])
        np.testing.assert_array_almost_equal(der, derivative_expected)

        def func(x):
            return 3*x[0]**2 + 4/x[0] + np.sin(x[0]**2)
        
        val, der = differentiate(func, np.array([x]), scalar=False)
        self.assertAlmostEqual(val, func(np.array([x])))
        np.testing.assert_array_almost_equal(der, derivative_expected)


    def test_differentiate_multivariate_scalar_function(self):
        def func(x, y, z):
            return 3*x**2 + 4*z/x + np.log(x+y+z)
        
        x = 2
        y = 3
        z = 1
        x_arr = np.array([x, y, z])

        val, der = differentiate(func, x_arr)
        self.assertAlmostEqual(val, func(x, y, z))
        derivative_expected = np.array([6*x- 4*z/x**2+1/(x+y+z), 1/(x+y+z), (5*x+4*z+4*y)/(x*(x+y+z))])
        np.testing.assert_array_almost_equal(der, derivative_expected)

        def func(x):
            return 3*x[0]**2 + 4*x[2]/x[0] + np.log(x[0]+x[1]+x[2])
        
        val, der = differentiate(func, x_arr, scalar=False)
        
        self.assertAlmostEqual(val, func(x_arr))
        np.testing.assert_array_almost_equal(der, derivative_expected)


    def test_differentiate_multivariate_vector_function(self):

        def func(x, y, z):
            f1 = 3*x**2 + 4*z/x + np.log(x+y+z)
            f2 = x*y*z
            f3 = 1/(x-z)
            f4 = y
            return np.array([f1, f2, f3, f4])
        
        x = 2
        y = 3
        z = 1
        x_arr = np.array([x, y, z])
        val, der = differentiate(func, x_arr)
        
        f1_der = [6*x- 4*z/x**2+1/(x+y+z), 1/(x+y+z), (5*x+4*z+4*y)/(x*(x+y+z))]
        f2_der = [y*z, x*z, x*y]
        f3_der = [-1/(x-z)**2, 0, 1/(x-z)**2]
        f4_der = [0, 1, 0]
        derivative_expected = np.array([f1_der, f2_der, f3_der, f4_der])

        np.testing.assert_array_almost_equal(val, func(x, y, z))
        np.testing.assert_array_almost_equal(der, derivative_expected)

        def func(x):
            f1 = 3*x[0]**2 + 4*x[2]/x[0] + np.log(x[0]+x[1]+x[2])
            f2 = x[0]*x[1]*x[2]
            f3 = 1/(x[0]-x[2])
            f4 = x[1]
            return np.array([f1, f2, f3, f4])
        
        val, der = differentiate(func, x_arr, scalar=False)
        
        np.testing.assert_array_almost_equal(val, func(x_arr))
        np.testing.assert_array_almost_equal(der, derivative_expected)

    
    def test_differentiate_univariate_vector_function(self):

        def func(x):
            f1 = x.logistic()
            f2 = x.log(base=2)
            f3 = x**2
            f4 = 1 - x
            return np.array([f1, f2, f3, f4])
        
        x = Variable(2, 1)
        val, der = differentiate(func, np.array([2]))

        val_expected = np.array([1/(1+np.exp(-2)), np.log2(2), 4, -1])
        
        f1_der = [np.exp(-2)/(1+np.exp(-2))**2]
        f2_der = [1/(np.log(2)*2)]
        f3_der = [2*2]
        f4_der = [-1]
        derivative_expected = np.array([f1_der, f2_der, f3_der, f4_der])

        np.testing.assert_array_almost_equal(val, val_expected)
        np.testing.assert_array_almost_equal(der, derivative_expected)

        def func(x):
            f1 = x[0].logistic()
            f2 = x[0].log(base=2)
            f3 = x[0]**2
            f4 = 1 - x[0]
            return np.array([f1, f2, f3, f4])
        
        val, der = differentiate(func, np.array([2]), scalar=False)
        
        np.testing.assert_array_almost_equal(val, val_expected)
        np.testing.assert_array_almost_equal(der, derivative_expected)


if __name__ == '__main__':
    unittest.main()