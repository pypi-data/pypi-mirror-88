from unittest import TestCase
from mvmtAD.Roots import *
from mvmtAD.AD import *
import numpy as np
import math as m

def func(x=8):
    return x**3 + x**2 - x
        
x_bisection_scalar = root_scalar(func,method ='bisection', bracket =[0.5,1], epsilon = 1e-8)
x_secant_scalar = root_scalar(func,method ='secant', bracket =[0.5,1], epsilon = 1e-8)
x_newton_scalar = root_scalar(func,method ='newton', x0 = 0.5, epsilon = 1e-8)
x_newton_hybrid_scalar = root_scalar(func,method ='newton_hybrid', bracket =[0.5,1])
        
class test_root_scalar(TestCase):
    
    def test_no_bracket_bisection(self):
        self.assertRaises(Exception, root_scalar, func(), method ='bisection', epsilon = 1e-8)
    
    def test_no_bracket_secant(self):
        self.assertRaises(Exception, root_scalar, func(), method ='secant', epsilon = 1e-8)
    
    def test_no_bracket_newton_hybrid(self):
        self.assertRaises(Exception, root_scalar, func(), method ='newton_hybrid', epsilon = 1e-8)
    
    def test_no_initial_guess(self):
        self.assertRaises(Exception, root_scalar, func(), method ='newton_hybrid', epsilon = 1e-8)
    
    def test_functionality_bisection(self):
        fval = func(x_bisection_scalar)
        self.assertAlmostEqual(fval, 0)

    def test_functionality_secant(self):
        fval = func(x_secant_scalar)
        self.assertAlmostEqual(fval, 0)
        
    def test_functionality_newton(self):
        fval = func(x_newton_scalar)
        self.assertAlmostEqual(fval, 0)
    
    def test_functionality_newton_hybrid(self):
        fval = func(x_newton_hybrid_scalar)
        self.assertAlmostEqual(fval, 0)

def f1(x=np.array([1,2])):
     return x[0]**2 - x[1] + x[0]*cos(np.pi*x[0])

def f2(x=np.array([4,5,3])):
    return x[0]*x[1] + exp(-x[1]) - x[0]**(-1)
    
F = [f1,f2]

x_newton, _ = root(F, x=[2, -1], method = 'Newton', epsilon=1e-10)
F_value_newton = np.array([func(x_newton) for func in F])

x_Broyden, _ = root(F, x=[2, -1], method = 'Broyden', epsilon=1e-10)
F_value_Broyden = np.array([func(x_Broyden) for func in F])

x_Broyden_inverse_update, _ = root(F, x=[2, -1], method = 'Broyden_inverse_update', epsilon=1e-10)
F_value_Broyden_inverse_update = np.array([func(x_Broyden_inverse_update) for func in F])

class test_root(TestCase):

    def test_no_initial_guess(self):
        self.assertRaises(Exception, root, F, method ='Newton', epsilon = 1e-8)
        self.assertRaises(Exception, root, F, method ='Broyden', epsilon = 1e-8)
        self.assertRaises(Exception, root, F, method ='Broyden_inverse_update', epsilon = 1e-8)

    def test_functionality_Newton(self):
        self.assertTrue(np.allclose(F_value_newton,np.zeros(F_value_newton.shape)))

    def test_functionality_Broyden(self):
        self.assertTrue(np.allclose(F_value_Broyden,np.zeros(F_value_Broyden.shape)))

    def test_functionality_Broyden_inverse_update(self):
        self.assertTrue(np.allclose(F_value_Broyden_inverse_update,np.zeros(F_value_Broyden_inverse_update.shape)))

def identity_func(x=8):
    return x
    
x_bisection_identity = bisection(identity_func,a=-1,b=1)
x_bisection_functionality = bisection(func,0.5,1)
fval_bisection_functionality = func(x_bisection_functionality)

class test_bisection(TestCase):

    def bisection_identity(self):
        self.assertAlmostEqual(x_bisection_identity, 0)

    def test_no_bracket(self):
        self.assertRaises(ValueError, bisection, func,1,1)

    def test_bad_bracket(self):
        self.assertRaises(ValueError, bisection, func,1, 2)

    def test_functionality(self):
        self.assertAlmostEqual(fval_bisection_functionality, 0)

x_secant_identity = secant(identity_func,a=-1,b=1)

x_secant_functionality =secant(func, 0.5, 1)
fval_secant_functionality = func(x_secant_functionality)

class test_secant(TestCase):

    def secant_identity(self):
        self.assertAlmostEqual(x_secant_identity, exp)

    def test_no_bracket(self):
        self.assertRaises(ValueError, secant, func, 1, 1)

    def test_functionality(self):
        self.assertAlmostEqual(fval_secant_functionality, 0)

x_newton_identity = newton(func, 0.5, 1e-8)

x_newton_functionality = newton(func,1,1e-8)
fval_newton_functionality = func(x_newton_functionality)

class test_newton(TestCase):

    def newton_identity(self):
        self.assertAlmostEqual(x, 0)

    def test_functionality(self):
        self.assertAlmostEqual(fval_newton_functionality, 0)

x_newton_hybrid_identity = newton_hybrid(identity_func, -1, 1)

x_newton_hybrid_functionality = newton_hybrid(func,a=0.5,b=1)
fval_newton_hybrid_functionality = func(x_newton_hybrid_functionality)

class test_newton_hybrid(TestCase):

    def test_no_bracket(self):
        self.assertRaises(ValueError, newton_hybrid, func, 1, 1)

    def test_bad_bracket(self):
        self.assertRaises(ValueError, newton_hybrid, func, 1, 2)

    def test_functionality(self):
        self.assertAlmostEqual(fval_newton_hybrid_functionality, 0)

F_norm_test_Newton_functionality = np.linalg.norm(F_value_newton, ord=2)

class test_Newton(TestCase):

    def test_Newton_functionality(self):
        self.assertAlmostEqual(F_norm_test_Newton_functionality, 0)

F_norm_test_Broyden_functionality = np.linalg.norm(F_value_Broyden, ord=2)

class test_Broyden(TestCase):

    def test_Broyden_functionality(self):
        self.assertAlmostEqual(F_norm_test_Broyden_functionality, 0)

F_norm_test_Broyden_inverse_update_functionality = np.linalg.norm(F_value_Broyden_inverse_update, ord=2)

class test_Broyden_inverse_update(TestCase):

    def test_Broyden_inverse_update_functionality(self):
        self.assertAlmostEqual(F_norm_test_Broyden_inverse_update_functionality, 0)
