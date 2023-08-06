from unittest import TestCase
import numpy as np
import math as m
from mvmtAD.AD import *

a1 = mvmtFloat(1)
b1 = mvmtFloat(2)

a2 = mvmtFloat(1,1)

a3 = mvmtFloat(3, np.array([1,0]))
a4 = mvmtFloat(2, np.array([1,0]))
a15 = mvmtFloat(15)
a16 = mvmtFloat(16)

class test_str(TestCase):
    def test_str_and_repr(self):
        self.assertEqual(repr(mvmtFloat(1)), "mvmtFloat with Value: 1, Derivative: 1")
        x = mvmtFloat(1, name='x')
        str = 'mvmtFloat with Value: 1, Derivative: 1, Name: x'
        self.assertEqual(repr(x), str)

class test_add(TestCase):

    def test_mvmtFloats(self):
        self.assertEqual(a1+b1, mvmtFloat(3,2))
        self.assertEqual(a3+a3, mvmtFloat(6,np.array([2,0])))

    def test_mvmtFloat_and_float1(self):
        self.assertEqual(a1+1.0, mvmtFloat(2,1))
        self.assertEqual(a2+1.0, mvmtFloat(2,1))
        self.assertEqual(a3+1.0, mvmtFloat(4,[1,0]))

    def test_mvmtFloat_and_int1(self):
        self.assertEqual(a1+1, mvmtFloat(2,1))
        self.assertEqual(a2+1, mvmtFloat(2,1))
        self.assertEqual(a3+1, mvmtFloat(4,np.array([1,0])))

    def test_mvmtFloat_and_string1(self):
        # If we try to add a string to an mvmtFloat, we should get a TypeError
        self.assertRaises(TypeError, a1.__add__, self, 'string')
        self.assertRaises(TypeError, a2.__add__, self, 'string')
        self.assertRaises(TypeError, a3.__add__, self, 'string')

    def test_commutative(self):
        self.assertEqual(a1+b1,b1+a1)

class test_mul(TestCase):

    def test_mvmtFloats(self):
        self.assertEqual(a1*b1, mvmtFloat(2,3))
        self.assertEqual(a3*a3, mvmtFloat(9,np.array([6,0])))

    def test_mvmtFloat_and_float1(self):
        self.assertEqual(a1*2.0, mvmtFloat(2,2))
        self.assertEqual(a2*2.0, mvmtFloat(2,2))
        self.assertEqual(a3*2.0, mvmtFloat(6,[2,0]))

    def test_mvmtFloat_and_int1(self):
        self.assertEqual(a1*2, mvmtFloat(2,2))
        self.assertEqual(a2*2, mvmtFloat(2,2))
        self.assertEqual(a3*2, mvmtFloat(6,np.array([2,0])))

    def test_mvmtFloat_and_string1(self):
        # If we try to add a string to an mvmtFloat, we should get a TypeError
        self.assertRaises(TypeError, a1.__mul__, self, 'string')

    def test_commutative(self):
        self.assertEqual(a1+b1,b1+a1)

class test_rmul(TestCase):

    def test_mvmtFloat_and_float1(self):
        self.assertEqual(2.0*a1, mvmtFloat(2,2))
        self.assertEqual(2.0*a2, mvmtFloat(2,2))
        self.assertEqual(2.0*a3, mvmtFloat(6,[2,0]))

    def test_mvmtFloat_and_int1(self):
        self.assertEqual(2*a1, mvmtFloat(2,2))
        self.assertEqual(2*a2, mvmtFloat(2,2))
        self.assertEqual(2*a3, mvmtFloat(6,np.array([2,0])))

class test_sub(TestCase):

    def test_mvmtFloats(self):
        self.assertEqual(b1-a1, mvmtFloat(1,0))
        self.assertEqual(a3-a4, mvmtFloat(1,np.array([0,0])))

    def test_mvmtFloat_and_float1(self):
        self.assertEqual(b1-1.0, mvmtFloat(1,1))
        self.assertEqual(a2-1.0, mvmtFloat(0,1))
        self.assertEqual(a3-1.0, mvmtFloat(2,np.array([1,0])))

    def test_mvmtFloat_and_int1(self):
        self.assertEqual(b1-1, mvmtFloat(1,1))
        self.assertEqual(a2-1, mvmtFloat(0,1))
        self.assertEqual(a3-1, mvmtFloat(2,np.array([1,0])))       

    def test_mvmtFloat_and_string1(self):
        # If we try to subtract a string from an mvmtFloat, we should get a TypeError
        self.assertRaises(TypeError, a1.__sub__, self, 'string')
        self.assertRaises(TypeError, a2.__sub__, self, 'string')
        self.assertRaises(TypeError, a3.__sub__, self, 'string')
       
class test_rsub(TestCase):

    def test_mvmtFloat_and_float1(self):
        self.assertEqual(1.0-b1, mvmtFloat(-1,-1))
        self.assertTrue(1.0-a2, mvmtFloat(0,-1))
        self.assertTrue(1.0-a3, mvmtFloat(-2,np.array([-1,0])))

    def test_mvmtFloat_and_int1(self):
        self.assertEqual(1-b1, mvmtFloat(-1,-1))
        self.assertTrue(1-a2, mvmtFloat(0,-1))
        self.assertTrue(1-a3, mvmtFloat(-2,np.array([-1,0])))       
      
class test_floordiv(TestCase):

    def test_mvmtFloats(self):
        self.assertEqual(mvmtFloat(5,2)//mvmtFloat(2,7),mvmtFloat(2,0))
        self.assertEqual(mvmtFloat(5,2)//mvmtFloat(5,2),mvmtFloat(1,np.inf))
        self.assertEqual(mvmtFloat(5,np.array([0,1]))//mvmtFloat(2,np.array([0,1])),mvmtFloat(2,np.array([0,0])))
        self.assertEqual(mvmtFloat(5,np.array([0,1]))//mvmtFloat(5,np.array([0,1])),mvmtFloat(1,np.inf))

class test_rfloordiv(TestCase):

    def test_mvmtFloat_and_int(self):
        self.assertEqual(4//mvmtFloat(5,2),mvmtFloat(4)//mvmtFloat(5,2))
        self.assertEqual(4//mvmtFloat(5,np.array([0,1])),mvmtFloat(4)//mvmtFloat(5,np.array([0,1])))

    def test_mvmtFloat_and_float(self):
        self.assertEqual(4.0//mvmtFloat(5,2),mvmtFloat(4.0)//mvmtFloat(5,2))
        
class test_truediv(TestCase):

    def test_mvmtFloats(self):
        self.assertEqual(mvmtFloat(5,2)/mvmtFloat(2,7),mvmtFloat(2.5,-7.75))
        self.assertEqual(mvmtFloat(5,np.array([2,2]))/mvmtFloat(2,np.array([7,7])),mvmtFloat(2.5,np.array([-7.75,-7.75])))
        
    def test_mvmtFloat_and_int(self):
        self.assertEqual(mvmtFloat(5,2)/2,mvmtFloat(2.5,1))
        
    def test_mvmtFloat_and_float(self):
        self.assertEqual(mvmtFloat(5,2)/2.,mvmtFloat(2.5,1))

class test_rtruediv(TestCase):

    def test_mvmtFloat_and_int(self):
        self.assertEqual(4/mvmtFloat(5,2),mvmtFloat(4)/mvmtFloat(5,2))
        self.assertEqual(4/mvmtFloat(5,np.array([0,1])),mvmtFloat(4)/mvmtFloat(5,np.array([0,1])))

    def test_mvmtFloat_and_float(self):
        self.assertEqual(4.0/mvmtFloat(5,2),mvmtFloat(4.0)/mvmtFloat(5,2))

class test_abs(TestCase):

    def test_mvmtFloat_intderivs(self):
        self.assertEqual(abs(mvmtFloat(5,2)),mvmtFloat(5,1))
        self.assertEqual(abs(mvmtFloat(-5,2)),mvmtFloat(5,-1))
        self.assertEqual(abs(mvmtFloat(0,2)),mvmtFloat(0,np.inf))
        
    def test_mvmtFloat_arrayderivs(self):
        self.assertEqual(abs(mvmtFloat(5,np.array([2,3]))),mvmtFloat(5,np.array([1,1])))
        self.assertEqual(abs(mvmtFloat(-5,np.array([2,3]))),mvmtFloat(5,np.array([-1,-1])))
        self.assertEqual(abs(mvmtFloat(0,np.array([2,3]))),mvmtFloat(0,np.inf))

class test_neg(TestCase):

    def test_mvmtFloat(self):
        self.assertEqual(-mvmtFloat(5,2),mvmtFloat(-5,-2))
        self.assertEqual(-mvmtFloat(5,np.array([2,3])),mvmtFloat(-5,np.array([-2,-3])))
        self.assertEqual(-mvmtFloat(-5,-2),mvmtFloat(5,2))
        self.assertEqual(-mvmtFloat(-5,np.array([-2,-3])),mvmtFloat(5,np.array([2,3])))

class test_pos(TestCase):

    def test_mvmtFloat(self):
        self.assertEqual(+mvmtFloat(5,2),mvmtFloat(5,2))
        self.assertEqual(+mvmtFloat(5,np.array([2,3])),mvmtFloat(5,np.array([2,3])))
        self.assertEqual(+mvmtFloat(-5,2),mvmtFloat(-5,2))
        self.assertEqual(+mvmtFloat(-5,np.array([2,3])),mvmtFloat(-5,np.array([2,3])))
        
class test_eq(TestCase):

    def test_mvmtFloats_intderivs(self):
        self.assertTrue(mvmtFloat(5,2)==mvmtFloat(5,2))
        self.assertFalse(mvmtFloat(5,2)==mvmtFloat(5,1))
        self.assertFalse(mvmtFloat(4,2)==mvmtFloat(5,2))
        self.assertFalse(mvmtFloat(4,2)==mvmtFloat(5,1))
        
    def test_mvmtFloats_arrayderivs(self):
        self.assertTrue(mvmtFloat(5,np.array([2,3]))==mvmtFloat(5,np.array([2,3])))
        self.assertFalse(mvmtFloat(5,np.array([2,3]))==mvmtFloat(5,np.array([2,2])))
        self.assertFalse(mvmtFloat(5,np.array([2,3]))==mvmtFloat(5,np.array([1,2])))
        self.assertFalse(mvmtFloat(5,np.array([2,3]))==mvmtFloat(4,np.array([2,3])))
        self.assertFalse(mvmtFloat(5,np.array([2,3]))==mvmtFloat(4,np.array([1,3])))

    def test_mvmtFloat_and_int(self):
        self.assertFalse(mvmtFloat(5,2)==5)
        self.assertFalse(mvmtFloat(5,np.array([2,3]))==5)
        
    def test_mvmtFloat_and_float(self):
        self.assertFalse(mvmtFloat(5,2)==5.0)
        self.assertFalse(mvmtFloat(5,np.array([2,3]))==5.0)
        
    def test_mvmtFloat_and_string(self):
        self.assertFalse(mvmtFloat(5,2)=='five')
        self.assertFalse(mvmtFloat(5,np.array([2,3]))=='five')

class test_mod(TestCase):
    def test_mvmtFloats(self):
        self.assertEqual(a16 % a2,  mvmtFloat(0,1))
        self.assertEqual(a16 % a15, mvmtFloat(1,1))
        self.assertNotEqual(a16 % a15, mvmtFloat(2,1))

    def test_mvmtFloat_and_float1(self):
        self.assertEqual(a16 % 2.0,  mvmtFloat(0,1))
        self.assertEqual(a16 % 15.0, mvmtFloat(1,1))
    
    def test_mvmtFloat_and_int1(self):
        self.assertEqual(a16 % 2,  mvmtFloat(0,1))
        self.assertEqual(a16 % 15, mvmtFloat(1,1))

    def test_mvmtFloat_and_string1(self):
        self.assertRaises(TypeError, a1.__mod__, self, a16, 'string')

class test_rmod(TestCase):
    def test_mvmtFloats(self):
        self.assertEqual(16.0 % b1,  mvmtFloat(0,1))
        self.assertEqual(16.0 % a15, mvmtFloat(1,1))
    
    def test_mvmtFloat_and_int1(self):
        self.assertEqual(16 % b1,  mvmtFloat(0,1))
        self.assertEqual(16 % a15, mvmtFloat(1,1))

    def test_mvmtFloat_and_string1(self):
        self.assertRaises(TypeError, a1.__rmod__, self, a16, 'string')

class test_neq(TestCase):

    def test_mvmtFloats_intderivs(self):
        self.assertFalse(mvmtFloat(5,2)!=mvmtFloat(5,2))
        self.assertTrue(mvmtFloat(5,2)!=mvmtFloat(5,1))
        self.assertTrue(mvmtFloat(4,2)!=mvmtFloat(5,2))
        self.assertTrue(mvmtFloat(4,2)!=mvmtFloat(5,1))
        
    def test_mvmtFloats_arrayderivs(self):
        self.assertFalse(mvmtFloat(5,np.array([2,3]))!=mvmtFloat(5,np.array([2,3])))
        self.assertTrue(mvmtFloat(5,np.array([2,3]))!=mvmtFloat(5,np.array([2,2])))
        self.assertTrue(mvmtFloat(5,np.array([2,3]))!=mvmtFloat(5,np.array([1,2])))
        self.assertTrue(mvmtFloat(5,np.array([2,3]))!=mvmtFloat(4,np.array([2,3])))
        self.assertTrue(mvmtFloat(5,np.array([2,3]))!=mvmtFloat(4,np.array([1,3])))

    def test_mvmtFloat_and_int(self):
        self.assertTrue(mvmtFloat(5,2)!=5)
        self.assertTrue(mvmtFloat(5,np.array([2,3]))!=5)
        
    def test_mvmtFloat_and_float(self):
        self.assertTrue(mvmtFloat(5,2)!=5.0)
        self.assertTrue(mvmtFloat(5,np.array([2,3]))!=5.0)
        
    def test_mvmtFloat_and_string(self):
        self.assertTrue(mvmtFloat(5,2)!='five')
        self.assertTrue(mvmtFloat(5,np.array([2,3]))!='five')


class test_gt(TestCase): #check comparison to integers and floats  - Martha
    
    def test_mvmtFloats(self):
        self.assertTrue(mvmtFloat(5)>mvmtFloat(4))
        self.assertTrue(mvmtFloat(5,1)>mvmtFloat(4,2))
        self.assertTrue(mvmtFloat(5)>mvmtFloat(4,2))
        self.assertFalse(mvmtFloat(5, np.array([2,3]))>mvmtFloat(6,np.array([1,1])))
        self.assertFalse(mvmtFloat(5,2)>mvmtFloat(5,1))
        
class test_lt(TestCase): #check comparison to integers and floats - Martha
    
    def test_mvmtFloats(self):
        self.assertTrue(mvmtFloat(4)<mvmtFloat(5))
        self.assertTrue(mvmtFloat(4,2)<mvmtFloat(5,1))
        self.assertTrue(mvmtFloat(4,2)<mvmtFloat(5))
        self.assertFalse(mvmtFloat(6,np.array([1,1]))<mvmtFloat(5, np.array([2,3])))
        self.assertFalse(mvmtFloat(5,1)<mvmtFloat(5,2))

class test_le(TestCase): #need to check implementation of equal to integer or float - Martha
    
    def test_mvmtFloats(self):
        self.assertTrue(mvmtFloat(5)<=mvmtFloat(5))
        self.assertTrue(mvmtFloat(4,2)<=mvmtFloat(5,1))
        self.assertTrue(mvmtFloat(4,2)<=mvmtFloat(5))
        self.assertFalse(mvmtFloat(6,np.array([1,1]))<=mvmtFloat(5, np.array([2,3])))
        self.assertTrue(mvmtFloat(5,1)<=mvmtFloat(5,2))

    def test_mvmtFloat_and_int(self):
        self.assertTrue(mvmtFloat(4)<=5)

    def test_mvmtFloat_and_float(self):
        self.assertTrue(mvmtFloat(4)<=5.0)

class test_ge(TestCase):
    
    def test_mvmtFloats(self):
        self.assertTrue(mvmtFloat(5)>=mvmtFloat(5))
        self.assertTrue(mvmtFloat(5,2)>=mvmtFloat(4,1))
        self.assertTrue(mvmtFloat(5,2)>=mvmtFloat(4))
        self.assertTrue(mvmtFloat(6,np.array([1,0]))>=mvmtFloat(5, np.array([1,0])))
        self.assertTrue(mvmtFloat(5,1)<=mvmtFloat(5,1))

    def test_mvmtFloat_and_int(self):
        self.assertTrue(mvmtFloat(5)>=4)

    def test_mvmtFloat_and_float(self):
        self.assertTrue(mvmtFloat(5)>=4.0)

########## Trig Function Tests ###############

class test_sin(TestCase):
    
    def test_mvmtFloats(self):
        p = np.pi
        x = mvmtFloat(p/4)
        xx = mvmtFloat(x)
        f = lambda x: sin(2*x)
        
        self.assertEqual(f(x).value, np.sin(np.pi/2))
        self.assertEqual(f(x).deriv, 2*np.cos(np.pi/2))
        self.assertEqual(f(xx).deriv.deriv, -4*np.sin(np.pi/2))

    def test_floats(self):
        self.assertEqual(sin(np.pi), m.sin(np.pi))

class test_cos(TestCase):
    
    def test_mvmtFloats(self):
        p = np.pi
        x = mvmtFloat(p/4)
        xx = mvmtFloat(x)
        f = lambda x: cos(2*x)
        
        self.assertEqual(f(x).value, np.cos(np.pi/2))
        self.assertEqual(f(x).deriv, -2*np.sin(np.pi/2))
        self.assertEqual(f(xx).deriv.deriv, -4*np.cos(np.pi/2))

class test_tan(TestCase):
    
    def test_mvmtFloats(self):
        x = mvmtFloat(np.pi)
        f = lambda x: tan(x**2)
        
        self.assertEqual(f(x).value,np.tan(np.pi**2))
        self.assertEqual(f(x).deriv,(1/np.cos(np.pi**2)**2)*2*np.pi)
        
    def test_float(self):
        x = np.pi
        f = lambda x: tan(x**2)
        
        self.assertEqual(f(x),np.tan(np.pi**2))

class test_asin(TestCase):
    
    def test_mvmtFloats(self):
        val = np.pi/8
        x = mvmtFloat(val)
        f = lambda x: asin(x**2)
        
        self.assertEqual(f(x).value,m.asin(val**2))
        self.assertEqual(f(x).deriv,1/np.sqrt(1-(val**2)**2)*2*val)

        x = mvmtFloat(10)
        with self.assertRaises(ValueError):
            f(x)    

    def test_float(self):
        val = np.pi/8
        f = lambda x: asin(x**2)
        
        self.assertEqual(f(val),m.asin(val**2))

class test_acos(TestCase):
    
    def test_mvmtFloats(self):
        val = np.pi/8
        x = mvmtFloat(val)
        f = lambda x: acos(x**2)
        
        self.assertEqual(f(x).value,m.acos(val**2))
        self.assertEqual(f(x).deriv,(-1/np.sqrt(1-(val**2)**2))*2*val)

        x = mvmtFloat(10)
        with self.assertRaises(ValueError):
            f(x)    
    
        
    def test_float(self):
        val = np.pi/8
        f = lambda x: acos(x**2)
        
        self.assertEqual(f(val),m.acos(val**2))

class test_atan(TestCase):
    
    def test_mvmtFloats(self):
        val = np.pi/8
        x = mvmtFloat(val)
        f = lambda x: atan(x**2)
        
        self.assertEqual(f(x).value,m.atan(val**2))
        self.assertEqual(f(x).deriv,(1/(1+(val**2)**2))*2*val)

    def test_float(self):
        val = np.pi/8
        f = lambda x: atan(x**2)
        
        self.assertEqual(f(val),m.atan(val**2))

########## Hyperbolic Function Tests ###############

class test_asinh(TestCase):
    
    def test_mvmtFloats(self):
        val = np.pi/2
        x = mvmtFloat(val)
        f = lambda x: asinh(x**2)
        
        self.assertTrue(f(x).value,m.asinh(val**2))
        self.assertTrue(f(x).deriv,(1/np.sqrt(1+(val**2)**2))*2*val)

    def test_float(self):
        val = np.pi/2
        f = lambda x: asinh(x**2)
        
        self.assertTrue(f(val),m.asinh(val**2))

class test_acosh(TestCase):
    
    def test_mvmtFloats(self):
        val = np.pi/2
        x = mvmtFloat(val)
        f = lambda x: acosh(x**2)
        
        self.assertTrue(f(x).value,m.acosh(val**2))
        self.assertTrue(f(x).deriv,(1/np.sqrt(((val**2)**2)-1))*2*val)

        x = mvmtFloat(0.1)
        with self.assertRaises(ValueError):
            f(x)  

    def test_float(self):
        val = np.pi/2
        f = lambda x: acosh(x**2)
        
        self.assertTrue(f(val),m.acosh(val**2))

class test_atanh(TestCase):
    
    def test_mvmtFloats(self):
        val = np.pi/4
        x = mvmtFloat(val)
        f = lambda x: atanh(x**2)
        
        self.assertEqual(f(x).value,m.atanh(val**2))
        self.assertEqual(f(x).deriv,(1/(1-(val**2)**2))*2*val)
        
        x = mvmtFloat(10)
        with self.assertRaises(ValueError):
            f(x)  

    def test_float(self):
        val = np.pi/4
        f = lambda x: atanh(x**2)
        
        self.assertEqual(f(val),m.atanh(val**2))
        
class test_sinh(TestCase):
    
    def test_mvmtFloats(self):
        x = mvmtFloat(np.pi)
        f = lambda x: sinh(x**2)
        
        self.assertEqual(f(x).value,np.sinh(np.pi**2))
        self.assertEqual(f(x).deriv,np.cosh(np.pi**2)*2*np.pi)

    def test_float(self):
        x = np.pi
        f = lambda x: sinh(x**2)
        
        self.assertEqual(f(x),np.sinh(np.pi**2))

class test_cosh(TestCase):
    
    def test_mvmtFloats(self):
        x = mvmtFloat(np.pi)
        f = lambda x: cosh(x**2)
        
        self.assertEqual(f(x).value,np.cosh(np.pi**2))
        self.assertEqual(f(x).deriv,np.sinh(np.pi**2)*2*np.pi)

    def test_float(self):
        x = np.pi
        f = lambda x: cosh(x**2)
        
        self.assertEqual(f(x),np.cosh(np.pi**2))

class test_tanh(TestCase):
    
    def test_mvmtFloats(self):
        x = mvmtFloat(np.pi)
        f = lambda x: tanh(x**2)
        
        self.assertEqual(f(x).value,np.tanh(np.pi**2))
        self.assertEqual(f(x).deriv,(1/(np.cosh(np.pi**2)**2))*2*np.pi)

    def test_float(self):
        x = np.pi
        f = lambda x: tanh(x**2)
        
        self.assertEqual(f(x),np.tanh(np.pi**2))

class test_exp(TestCase):
    def test_mvmtFloats(self):
        x = mvmtFloat(np.pi)
        xx = mvmtFloat(x)
        f = lambda x: exp(2*x)
        self.assertEqual( f(x).value, m.exp(np.pi*2) )
        self.assertEqual( f(x).deriv, 2*m.exp(np.pi*2) )
        self.assertEqual( f(xx).deriv.deriv, 4*m.exp(np.pi*2) )

    def test_floats(self):
        self.assertEqual(exp(np.pi), m.exp(np.pi))

class test_sqrt(TestCase):
    def test_mvmtFloats(self):
        x = mvmtFloat(4)
        f = lambda x: sqrt(x)
        self.assertEqual( f(x).value, 2.0 )
        self.assertEqual( f(x).deriv, 0.25 )

    def test_floats(self):
        self.assertEqual(sqrt(2.0), m.sqrt(2.0))

class test_degrees(TestCase):
    def test_mvmtFloat(self):
        x = mvmtFloat(np.pi)
        f = lambda x: degrees(x)
        self.assertEqual( f(x).value, 180.0 )
        self.assertEqual( f(x).deriv, 180.0 / np.pi )

class test_radians(TestCase):
    def test_mvmtFloat(self):
        x = mvmtFloat(180.0)
        f = lambda x: radians(x)
        self.assertEqual( f(x).value, np.pi )
        self.assertEqual( f(x).deriv, np.pi / 180.0 )

class test_partials(TestCase):
    def test_mvmtFloat_scalar(self):

        def f(x):
            return 2*x
        
        x = mvmtFloat(10)

        p = partials(f,x)
        self.assertEqual( p.value, 20 )
        self.assertEqual( p.deriv, 2.0)

    def test_mvmtFloat_named_scalar(self):

        def f(x):
            return 2*x

        x = mvmtFloat(10, name='x')
        p = partials(f,x,BY_NAME=True)
        self.assertEqual( p.value, 20 )
        self.assertEqual( p.deriv, 2.0)       

    def test_scalar(self):

        def f(x):
            return 2*x
        
        x = 10

        self.assertEqual( partials(f,x).value, 20 )
        self.assertEqual( partials(f,x).deriv, 2.0)

    def test_multiple_scalar(self):

        def f(x,y):
            return x*y

        p = partials(f, [10,10])
        self.assertEqual(p.value, 100)

    def test_error_cond(self):

        def f(x,y):
            return x*y
        
        with self.assertRaises(ValueError):
            x = mvmtFloat(0.1)
            p = partials(f,x)

        with self.assertRaises(ValueError):
            x = mvmtFloat(0.1)
            a = mvmtFloat(0.2)
            p = partials(f,[x,a], BY_NAME=True)

    def test_mvmtFloat(self):

        def f(x,y,z):
            return 2*x + 3*y + 4*z
        
        x = mvmtFloat(10)
        y = mvmtFloat(20)
        z = mvmtFloat(30)

        self.assertEqual( partials(f, [x,y,z]).value, 200 )
        self.assertTrue( (partials(f, [x,y,z]).deriv == [2., 3., 4.]).all() )

    def test_float(self):

        def f(x,y,z):
            return 2*x + 3*y + 4*z
        
        x = 10
        y = 20
        z = 30

        self.assertEqual( partials(f, [x,y,z]).value, 200 )
        self.assertTrue( (partials(f, [x,y,z]).deriv == [2., 3., 4.]).all() )

    def test_mixed(self):

        def f(x,y,z):
            return 2*x + 3*y + 4*z
        
        x = 10
        y = mvmtFloat(20)
        z = 30

        self.assertEqual( partials(f, [x,y,z]).value, 200 )
        self.assertTrue( (partials(f, [x,y,z]).deriv == [2., 3., 4.]).all() )

class test_jacobian(TestCase):    
    def test_bound_jacobian(self):

        def f1(x):
            return 10*x[0] + 20*x[1]
        def g1(x):
            return sin(x[0]) + cos(x[1])

        f = [f1, g1]
        x = np.array([0, np.pi/2])
        J = jacobian(f, x)
        B = bound_jacobian(f)
        self.assertTrue((J==B(x)).all)
    
    def test_scalar(self):

        def f(x):
            return 2*x
        
        J = jacobian(f, 10)
        self.assertEqual(J, 2)

    def test_unnamed_mvmtFloat(self):

        def f(x,y,z):
            return 2*x + 3*y + 4*z
        
        x = mvmtFloat(10)
        y = mvmtFloat(20)
        z = mvmtFloat(30)

        J = jacobian(f, [x,y,z], BY_NAME=False)

        self.assertTrue( (J == [2., 3., 4.]).all() )

    def test_named_mvmtFloat(self):

        def f(x,y,z):
            return 2*x + 3*y + 4*z
        
        x = mvmtFloat(10, name='x')
        y = mvmtFloat(20, name='y')
        z = mvmtFloat(30, name='z')

        J = jacobian(f, [x,y,z])

        self.assertTrue( (J == [2., 3., 4.]).all() )

    def test_float_1_func(self):

        def f(x,y,z):
            return 2*x + 3*y + 4*z
        
        x = 10.0
        y = 20.0
        z = 30.0

        J = jacobian(f, [x,y,z], BY_NAME=False)
        self.assertTrue( (J == [2., 3., 4.]).all() )

    def test_float_N_func(self):

        def f(x,y,z):
            return 2*x + 3*y + 4*z
        
        x = 10.0
        y = 20.0
        z = 30.0

        ff = [f, f]

        ans = np.array(np.array([[2., 3., 4.],[2., 3., 4.]]))
        
        J = jacobian(ff, [x,y,z], BY_NAME=False)
        self.assertTrue( (J == ans).all() )

    def test_mixed(self):

        def f(x,y,z):
            return 2*x + 3*y + 4*z
        
        x = 10.0
        y = mvmtFloat(20)
        z = 30.0

        J = jacobian(f, [x,y,z], BY_NAME=False)
        self.assertTrue( (J == [2., 3., 4.]).all() )

class test_power_funs(TestCase):

    def test_pow_self(self):
        
        c = m.cos(1)
        c_der = -m.sin(1)

        d = m.sin(1)
        d_der = m.cos(1)

        c_mvmt = mvmtFloat(np.array(c),np.array([c_der]))
        d_mvmt = mvmtFloat(np.array(d),np.array([d_der]))

        new_val = c**d
        new_der = m.cos(1)**(m.sin(1))*(m.cos(1)*m.log(m.cos(1)) - m.sin(1)**2/m.cos(1))
        
        new_mvmt_float = c_mvmt**d_mvmt        

        #Note: We have to round, otherwise there are minute (<10^-10) differences between the values
        self.assertEqual(round(new_mvmt_float.value,5),round(new_val,5))
        self.assertEqual(round(float(new_mvmt_float.deriv),5), round(new_der,5))
    
    def test_pow_func_self(self):
        
        c = m.cos(1)
        c_der = -m.sin(1)

        d = m.sin(1)
        d_der = m.cos(1)

        c_mvmt = mvmtFloat(c,c_der)
        d_mvmt = mvmtFloat(d,d_der)

        new_val = pow(c,d)
        new_der = m.cos(1)**(m.sin(1))*(m.cos(1)*m.log(m.cos(1)) - m.sin(1)**2/m.cos(1))
        
        new_mvmt_float = pow(c_mvmt, d_mvmt)

        #Note: We have to round, otherwise there are minute (<10^-10) differences between the values
        self.assertEqual(round(new_mvmt_float.value,5),round(new_val,5))
        self.assertEqual(round(float(new_mvmt_float.deriv),5), round(new_der,5))


    def test_pow_self_2(self):
        
        def c_val(x):
            return 2*x**3

        def c_der(x):
            return 6*x**2

        def d_val(x):
            return m.log(x)

        def d_der(x):
            return 1/x

        def cd_val(x):
            return (2*x**3)**m.log(x)

        def cd_der(x):
            return (x**(3*m.log(x)-1))*(2**m.log(x))*(6*m.log(x) + m.log(2))        
    
        x = 2

        c = c_val(x)
        c_der = c_der(x)

        d = d_val(x)
        d_der = d_der(x)

        cd_val_float = cd_val(x)
        cd_der_float = cd_der(x)

        c_mvmt = mvmtFloat(np.array(c),np.array([c_der]))
        d_mvmt = mvmtFloat(np.array(d),np.array([d_der]))

        new_mvmt_float = c_mvmt**d_mvmt        

        #Note: We have to round, otherwise there are minute (<10^-10) differences between the values
        self.assertEqual(round(new_mvmt_float.value,5),round(cd_val_float,5))
        self.assertEqual(round(float(new_mvmt_float.deriv),5), round(cd_der_float,5))

class test_log_funs(TestCase):

    def test_log(self):

        def c_val(x):
            return 2*x**3

        def c_der(x):
            return 6*x**2   
    
        x = 5
        c = c_val(x)
        c_der = c_der(x)
        c_mvmt = mvmtFloat(np.array(c),np.array([c_der]))
        c_log = log(c_mvmt)
        
        self.assertEqual(c_log.value,m.log(c_mvmt.value))
        
        
    def test_log_2(self):

        def c_val(x):
            return 2*x**3

        def c_der(x):
            return 6*x**2   
    
        x = 30
        c = c_val(x)
        c_der = c_der(x)
        c_mvmt = mvmtFloat(np.array(c),np.array([c_der]))
        c_log = log(c_mvmt)
        
        self.assertEqual(c_log.value,m.log(c_mvmt.value))

    def test_log_neg(self):
        f = lambda x: log(x)
        x = mvmtFloat(-1)
        with self.assertRaises(ValueError):        
            f(x)
    
    def test_log_base(self):
        x = mvmtFloat(3)
        self.assertEqual(log(3,3), 1.0)
        self.assertEqual(log(x,3).value, 1.0)

class test_logistic_funs(TestCase):
    def test_logistic(self):
        x = mvmtFloat(0)
        v = logistic(x)
        self.assertEqual(v.value, 0.5)
        self.assertEqual(v.deriv, 0.25)

        v = logistic(0)
        self.assertEqual(v, 0.5)

