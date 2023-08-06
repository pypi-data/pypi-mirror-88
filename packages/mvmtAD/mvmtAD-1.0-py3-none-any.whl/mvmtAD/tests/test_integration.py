import numpy as np
from unittest import TestCase
from mvmtAD.AD import mvmtFloat, exp, sin, cos, sqrt

a = mvmtFloat(3, np.array([1,0]))
b = mvmtFloat(7, np.array([0,1]))

class test_integration(TestCase):
    def test_pow_mult(self):
        self.assertEqual(a**2*b, mvmtFloat(63,np.array([42,9])))

    def test_milestone_2_eqn(self):
        # the following compares an equation and its symbolic derivative to
        # the result when using AD

        from math import exp, sin, cos, sqrt

        def f(x):
            return exp(sin(x))-cos(x**0.5)*sin((cos(x)**2+x**2)**0.5)

        def df(x):
            return exp(sin(x))*cos(x) + (sin((x**2 + cos(x)**2)**(0.5))*sin(x**(0.5)))/(2*x**(0.5)) - (cos((x**2 + cos(x)**2)**(0.5))*cos(x**(0.5))*(2*x - 2*cos(x)*sin(x)))/(2*(x**2 + cos(x)**2)**(0.5))

        x = 2.0
        m_fx = f(x)
        m_dfdx = df(x)

        from mvmtAD.AD import exp, sin, cos, sqrt

        x = mvmtFloat(2)
        a_fx = f(x)
        a_dfdx = df(x)

        self.assertEqual(a_fx.value,   m_fx)
        self.assertAlmostEqual(a_fx.deriv,   m_dfdx)
        self.assertAlmostEqual(a_dfdx.value, m_dfdx)