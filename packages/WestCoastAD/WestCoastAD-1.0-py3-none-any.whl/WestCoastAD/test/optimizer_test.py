import unittest
import numpy as np

from WestCoastAD import Optimizer


class VariableUnitTest(unittest.TestCase):
    def test_x_squared_optimization(self):
        def objective_func(x):
            return x ** 2

        var_init = np.array([2])
        optimizer = Optimizer(objective_func, var_init)
        min_value, var_value = optimizer.gd_optimize(
            tolerance=0.0000001, num_iterations=1000
        )
        self.assertAlmostEqual(min_value, 0, places=5)
        self.assertAlmostEqual(var_value[0], 0, places=5)

    def test_x_y_z_squared_optimization(self):
        def objective_func(x, y, z):
            return x ** 2 + y ** 2 + z ** 2

        var_init = np.array([-15, 100, -20])
        optimizer = Optimizer(objective_func, var_init)
        min_value, var_value = optimizer.gd_optimize(
            tolerance=0.0000001, num_iterations=1000
        )
        self.assertAlmostEqual(min_value, 0, places=5)
        self.assertAlmostEqual(var_value[0], 0, places=5)
        self.assertAlmostEqual(var_value[1], 0, places=5)
        self.assertAlmostEqual(var_value[2], 0, places=5)

        def objective_func(x):
            return x[0] ** 2 + x[1] ** 2 + x[2] ** 2

        var_init = np.array([-15, 100, -20])
        optimizer = Optimizer(objective_func, var_init, scalar=False)
        min_value, var_value = optimizer.gd_optimize(
            tolerance=0.0000001, num_iterations=1000
        )
        self.assertAlmostEqual(min_value, 0, places=5)
        self.assertAlmostEqual(var_value[0], 0, places=5)
        self.assertAlmostEqual(var_value[1], 0, places=5)
        self.assertAlmostEqual(var_value[2], 0, places=5)

    def test_univariate_scalar_momentum_optimization(self):
        def objective_func(x):
            return x ** 6 - 2 * x

        var_init = np.array([2])
        optimizer = Optimizer(objective_func, var_init)
        min_value, var_value = optimizer.momentum_optimize(
            tolerance=None, num_iterations=1000
        )
        self.assertAlmostEqual(min_value, -5 / (3 * 3 ** (1 / 5)), places=5)
        self.assertAlmostEqual(var_value[0], 1 / (3 ** (1 / 5)), places=5)

    def test_multivariate_scalar_momentum_optimization(self):
        def objective_func(x, y):
            return x ** 2 + x * y + y ** 2

        var_init = np.array([0.2, 0.5])
        optimizer = Optimizer(objective_func, var_init)
        min_value, var_value = optimizer.momentum_optimize(
            tolerance=None, num_iterations=1000
        )
        self.assertAlmostEqual(min_value, 0, places=5)
        self.assertAlmostEqual(var_value[0], 0, places=5)
        self.assertAlmostEqual(var_value[1], 0, places=5)

    def test_multivariate_vector_momentum_optimization(self):
        def objective_func(x):
            return x[0] ** 2 + x[0] * x[1] + x[1] ** 2

        var_init = np.array([0.2, 0.5])
        optimizer = Optimizer(objective_func, var_init, scalar=False)
        min_value, var_value = optimizer.momentum_optimize(
            tolerance=None, num_iterations=1000
        )
        self.assertAlmostEqual(min_value, 0, places=5)
        self.assertAlmostEqual(var_value[0], 0, places=5)
        self.assertAlmostEqual(var_value[1], 0, places=5)

    def test_beta_momentum_exception(self):
        def objective_func(x):
            return x

        with self.assertRaises(ValueError) as e:
            var_init = np.array([0.2])
            optimizer = Optimizer(objective_func, var_init)
            optimizer.momentum_optimize(beta=54, num_iterations=1000)
        self.assertEqual(
            "The value of beta (sample weight) should be between 0 and 1.",
            str(e.exception),
        )

    def test_univariate_scalar_adagrad_optimization(self):
        def objective_func(x):
            return x * np.log(x)

        var_init = np.array([2])
        optimizer = Optimizer(objective_func, var_init)
        min_value, var_value = optimizer.adagrad_optimize(
            tolerance=None, num_iterations=100000
        )
        self.assertAlmostEqual(min_value, -1 / np.e, places=3)
        self.assertAlmostEqual(var_value[0], 1 / np.e, places=3)

    def test_multivariate_scalar_adagrad_optimization(self):
        def objective_func(x, y):
            return x ** 2 + x * y + y ** 2

        var_init = np.array([0.2, 0.5])
        optimizer = Optimizer(objective_func, var_init)
        min_value, var_value = optimizer.adagrad_optimize(
            tolerance=None, num_iterations=10000
        )
        self.assertAlmostEqual(min_value, 0, places=4)
        self.assertAlmostEqual(var_value[0], 0, places=4)
        self.assertAlmostEqual(var_value[1], 0, places=4)

    def test_multivariate_vector_adagrad_optimization(self):
        def objective_func(x):
            return x[0] ** 2 + x[0] * x[1] + x[1] ** 2

        var_init = np.array([0.2, 0.5])
        optimizer = Optimizer(objective_func, var_init, scalar=False)
        min_value, var_value = optimizer.adagrad_optimize(
            tolerance=None, num_iterations=10000
        )
        self.assertAlmostEqual(min_value, 0, places=4)
        self.assertAlmostEqual(var_value[0], 0, places=4)
        self.assertAlmostEqual(var_value[1], 0, places=4)

    def test_univariate_scalar_rmsprop_optimization(self):
        def objective_func(x):
            return x * np.log(x)

        var_init = np.array([2])
        optimizer = Optimizer(objective_func, var_init)
        min_value, var_value = optimizer.rmsprop_optimize(
            tolerance=None, num_iterations=10000
        )
        self.assertAlmostEqual(min_value, -1 / np.e, places=5)
        self.assertAlmostEqual(var_value[0], 1 / np.e, places=5)

    def test_multivariate_scalar_rmsprop_optimization(self):
        def objective_func(x, y):
            return x ** 2 + x * y + y ** 2

        var_init = np.array([0.2, 0.5])
        optimizer = Optimizer(objective_func, var_init)
        min_value, var_value = optimizer.rmsprop_optimize(
            tolerance=None, num_iterations=10000
        )
        self.assertAlmostEqual(min_value, 0, places=5)
        self.assertAlmostEqual(var_value[0], 0, places=3)
        self.assertAlmostEqual(var_value[1], 0, places=3)

    def test_multivariate_vector_rmsprop_optimization(self):
        def objective_func(x):
            return x[0] ** 2 + x[0] * x[1] + x[1] ** 2

        var_init = np.array([0.2, 0.5])
        optimizer = Optimizer(objective_func, var_init, scalar=False)
        min_value, var_value = optimizer.rmsprop_optimize(
            tolerance=None, num_iterations=10000
        )
        self.assertAlmostEqual(min_value, 0, places=5)
        self.assertAlmostEqual(var_value[0], 0, places=3)
        self.assertAlmostEqual(var_value[1], 0, places=3)

    def test_beta_rmsprop_exception(self):
        def objective_func(x):
            return x

        with self.assertRaises(ValueError) as e:
            var_init = np.array([0.2])
            optimizer = Optimizer(objective_func, var_init)
            optimizer.rmsprop_optimize(beta=54, num_iterations=1000)
        self.assertEqual(
            "The value of beta (sample weight) should be between 0 and 1.",
            str(e.exception),
        )

    def test_univariate_scalar_adam_optimize(self):
        def objective_func(x):
            return np.exp(-2.0 * np.sin(4.0*x)*np.sin(4.0*x))

        var_init = np.array([2])
        optimizer = Optimizer(objective_func, var_init)
        min_value, var_value = optimizer.adam_optimize(learning_rate=0.001, beta1=0.9, beta2=0.999, 
        epsilon=1e-8, num_iterations=1000)
        self.assertEqual(min_value, 0.1353352832366127)
        self.assertEqual(var_value[0], 1.963495408493621)

    def test_x_y_exp_func_adam_optimize(self):
        def objective_func(x, y):
            return x*y + np.exp(x*y)

        var_init = np.array([2, 2])
        optimizer = Optimizer(objective_func, var_init)
        min_value, var_value = optimizer.adam_optimize(learning_rate=0.01, beta1=0.9, beta2=0.999, epsilon=1e-8, 
        num_iterations=1000, tolerance=1.0e-08)
        self.assertEqual(min_value, 1.1762618133993703)
        self.assertEqual(var_value[0], 0.2936289210258825)
        self.assertEqual(var_value[1], 0.2936289210258825)

    def test_beta_adam_exception(self):
        def objective_func(x):
            return x

        with self.assertRaises(ValueError) as e:
            var_init = np.array([0.2])
            optimizer = Optimizer(objective_func, var_init)
            optimizer.adam_optimize(learning_rate=0.01, beta1=1.9, beta2=0.999, epsilon=1e-8, 
            num_iterations=1000, tolerance=1.0e-08)
        self.assertEqual(
            "The value of beta (sample weight) should be between 0 and 1 (excluding 1).",
            str(e.exception),)
        
        with self.assertRaises(ValueError) as e:
            var_init = np.array([0.2])
            optimizer = Optimizer(objective_func, var_init)
            optimizer.adam_optimize(learning_rate=0.01, beta1=0.9, beta2=1.999, epsilon=1e-8, num_iterations=1000, 
            tolerance=1.0e-08)
        self.assertEqual(
            "The value of beta (sample weight) should be between 0 and 1 (excluding 1).",
            str(e.exception),)

    def test_x_y_z_squared_adam_optimize(self):
        def objective_func(x):
            return x[0]**2+x[1]**2+x[2]**2

        var_init = np.array([-15, 100, -20])
        optimizer = Optimizer(objective_func, var_init, scalar=False)
        min_value, var_value = optimizer.adam_optimize(learning_rate=0.1, beta1=0.9, beta2=0.999, 
        epsilon=1e-8, num_iterations=10000)
        self.assertAlmostEqual(min_value, 0, places=5)
        self.assertAlmostEqual(var_value[0], 0, places=5)
        self.assertAlmostEqual(var_value[1], 0, places=5)
        self.assertAlmostEqual(var_value[2], 0, places=5)

        def objective_func(x, y, z):
            return x**2+y**2+z**2

        var_init = np.array([-15, 100, -20])
        optimizer = Optimizer(objective_func, var_init)
        min_value, var_value = optimizer.adam_optimize(learning_rate=0.1, beta1=0.9, beta2=0.999, 
        epsilon=1e-8, num_iterations=10000)
        self.assertAlmostEqual(min_value, 0, places=5)
        self.assertAlmostEqual(var_value[0], 0, places=5)
        self.assertAlmostEqual(var_value[1], 0, places=5)
        self.assertAlmostEqual(var_value[2], 0, places=5)

    
    def test_x_squared_optimization_bfgs(self):
        def objective_func(x):
            return x**2

        var_init = np.array([2])
        optimizer = Optimizer(objective_func, var_init)
        min_value, var_value = optimizer.bfgs_optimize(num_iterations=2000)
        self.assertAlmostEqual(min_value, 0, places=5)
        self.assertAlmostEqual(var_value[0], 0, places=5)
    

    def test_x_y_z_squared_optimization_bfgs(self):
        def objective_func(x, y, z):
            return x**2+y**2+z**2

        var_init = np.array([-15, 100, -20])
        optimizer = Optimizer(objective_func, var_init)
        min_value, var_value = optimizer.bfgs_optimize(num_iterations=2000)
        self.assertAlmostEqual(min_value, 0, places=5)
        self.assertAlmostEqual(var_value[0], 0, places=5)
        self.assertAlmostEqual(var_value[1], 0, places=5)
        self.assertAlmostEqual(var_value[2], 0, places=5)

        def objective_func(x):
            return x[0]**2+x[1]**2+x[2]**2

        var_init = np.array([-15, 100, -20])
        optimizer = Optimizer(objective_func, var_init, scalar=False)
        min_value, var_value = optimizer.bfgs_optimize(tolerance=0.0000001, num_iterations=2000)
        self.assertAlmostEqual(min_value, 0, places=4)
        self.assertAlmostEqual(var_value[0], 0, places=4)
        self.assertAlmostEqual(var_value[1], 0, places=4)
        self.assertAlmostEqual(var_value[2], 0, places=4)
    
if __name__ == "__main__":
    unittest.main()