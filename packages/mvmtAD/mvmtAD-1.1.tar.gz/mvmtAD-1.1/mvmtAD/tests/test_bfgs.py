from unittest import TestCase
import numpy as np
import math as m
from mvmtAD.AD import *
from mvmtAD.bfgs import bfgs

class test_bfgs(TestCase):

    def test_bfgs_2d(self):

        def f(x):
            return x[0]**2 - x[0]*x[1] + x[1]**2 + 9*x[0] - 6*x[1] + 20
        def g(x):
            return x[0]**2 - x[0]*x[1] + x[1]**2 + 7*x[0] - 4*x[1] + 20

        e = np.array( [[-4.,1],[-3.333333,0.333333]])

        r = bfgs([f,g], np.array([1,1]), USE_SCIPY_LS=False)

        match = (np.abs(r-e) < 1e-6)
        self.assertTrue(match.all())

    def test_bfgs_2d_sp_linesearch(self):

        def f(x):
            return x[0]**2 - x[0]*x[1] + x[1]**2 + 9*x[0] - 6*x[1] + 20
        def g(x):
            return x[0]**2 - x[0]*x[1] + x[1]**2 + 7*x[0] - 4*x[1] + 20

        e = np.array( [[-4.,1],[-3.333333,0.333333]])

        r = bfgs([f,g], np.array([1,1]))

        match = (np.abs(r-e) < 1e-6)
        self.assertTrue(match.all())

    def test_bfgs_1_func_1_var(self):

        def f(x):
            return x**2

        e = np.array([0])

        r = bfgs(f, np.array([2]))

        match = (np.abs(r-e) < 1e-6)
        self.assertTrue(match.all())
      
        

