import math as m
import numpy as np
from inspect import signature

class mvmtFloat():
    """
    This class implements the basic datatype used in the mvmt 
    auto-differentiation package

    ...

    Attributes
    ----------
    value : numeric
        value of the variable
    deriv : numeric or np.ndarray
        derivative of function at location 'value', optional, default=1
    name : str
        optional name of the variable, default=None

    Methods
    -------
    all arithmetic operators have been overloaded to implement the derivative
    rule for the given operation.

    all comparison operators have been overloaded to implement correct
    comparison, primarily on the value attribute.
    """
    __slots__ = ['value', 'deriv', 'name']

    def __init__(self, value=0, deriv=1, name=None):
        self.value = value
        self.deriv = deriv
        self.name = name

    def __str__(self):
        if self.name:
            return "mvmtFloat with Value: {0}, Derivative: {1}, Name: {2}"\
                .format(self.value, self.deriv, self.name)
        else:
            return "mvmtFloat with Value: {0}, Derivative: {1}"\
                .format(self.value, self.deriv)

    def __repr__(self):
        return self.__str__()

    def __len__(self):
        return 1

    #
    # Arithmetic operators
    #   see: https://docs.python.org/3/library/operator.html
    #

    def __add__(self, other):
        """
            Implements addition operator when when or both inputs are mvmtFloat

            INPUTS
            ======
            self: mvmtFloat, required
            other: mvmtFloat or numeric type, required

            RETURNS
            =======
            mvmtFloat

            NOTES
            =====
            PRE:
                - two inputs

            POST:
                - self and other are not changed by this function
                - returns a new mvmtFloat

            EXAMPLES
            ========
            >>> a = mvmtFloat(1, 1)
            >>> a + 1
            mvmtFloat with Value: 2, Derivative: 1
        """
        try:
            return mvmtFloat(self.value+other.value, self.deriv+other.deriv)
        except AttributeError:
            return mvmtFloat(self.value+other, self.deriv)
        
    def __mul__(self, other):
        '''
            Implements multiplcation operator when one or both inputs are mvmtFloat
        '''
        try:
            return mvmtFloat(self.value*other.value, 
                self.deriv*other.value + self.value*other.deriv)
        except AttributeError:
            return mvmtFloat(self.value*other, self.deriv*other)
    
    def __rpow__(self, other): 
        '''
            Implements power operator when exponent only is mvmtFloat
        '''
        if not isinstance(other,mvmtFloat): 
            
            if other > 0:
        
                return mvmtFloat(other**np.float(self.value), 
                    other**np.float(self.value)*m.log(other)*self.deriv) 
        
            elif other < 0:
                
                if float(self.value).is_integer() == True:
                    
                    return mvmtFloat(np.float(other)**np.float(self.value),np.float(other)**np.float(self.value)*m.log(np.abs(np.float(other)))*self.deriv)
                     
                else:
                    raise ValueError("Cannot take a negative base to a fractional power")

            elif other ==0:
                raise ValueError("Cannot take the derivative of an exponential function whose base is zero")
        
        elif other.value > 0:
            return mvmtFloat(other.value**np.float(self.value), 
                            (other.value**np.float(self.value))*((other.deriv/other.value)*self.value + self.deriv*m.log(other.value)))
        
        elif other.value < 0:
            
            if float(self.value).is_integer(): 
                return mvmtFloat(other.value**np.float(self.value), 
                                (other.value**np.float(self.value))*((other.deriv/other.value)*self.value - self.deriv*m.log(np.abs(other.value))))
            else:
                raise ValueError("Cannot take a negative base to a fractional power")
            
        elif other.value == 0:
            raise ValueError("Cannot take the derivative of an exponential function whose base is zero")    
    
    def __pow__(self, other):
        '''
            Implements power operator when base is mvmtFloat
        '''        
        if not isinstance(other, mvmtFloat): 
            if self.value >=0:
                return mvmtFloat(self.value**np.float(other), 
                                 other*self.value**np.float(other-1)*self.deriv)
            
            elif self.value < 0:
                if float(other).is_integer():
                    return mvmtFloat(self.value**np.float(other), 
                        other*self.value**np.float(other-1)*self.deriv)
                
                else:
                    raise ValueError("Cannot take a negative base to a fractional power")
        
        elif self.value > 0:
            return mvmtFloat(self.value**np.float(other.value), 
                            (self.value**np.float(other.value))*((self.deriv/self.value)*other.value + other.deriv*m.log(self.value)))
        
        elif self.value < 0:
            if float(other.value).is_integer():
                return mvmtFloat(self.value**np.float(other.value), 
                                (self.value**np.float(other.value))*((self.deriv/self.value)*other.value - other.deriv*m.log(np.abs(self.value))))

            else:
                raise ValueError("Cannot take a negative base to a fractional power")
                
        elif self.value == 0:
            raise ValueError("Cannot take the derivative of an exponential function whose base is zero")
        
    def __sub__(self, other): 
        '''
            Implements subtraction operator when left side or both inputs are mvmtFloat
        '''
        x = self
        if not isinstance(x,mvmtFloat):
            x = mvmtFloat(x,0)
        if not isinstance(other,mvmtFloat):
            other = mvmtFloat(other,0)
        return mvmtFloat(x.value - other.value, x.deriv - other.deriv)
    
    def __rsub__(self, other): 
        '''
            Implements subtraction operator right side only is mvmtFloat
        '''
        x = self
        if not isinstance(x,mvmtFloat):
            x = mvmtFloat(x,0)
        if not isinstance(other,mvmtFloat):
            other = mvmtFloat(other,0)
        return mvmtFloat(other.value - x.value, other.deriv - x.deriv)    

    def __floordiv__(self, other):
        '''Implements integer division
        
        Integer division, also known as floor division (applying the floor function after division)
        
        The derivative of the floor function is undefined (np.inf) for integer values and 0 everywhere else'''
        truediv = self.__truediv__(other)
        if m.floor(truediv.value)==truediv.value:
            deriv = np.inf
        else:
            if isinstance(self.deriv, np.ndarray):
                deriv=np.zeros(self.deriv.shape)
            else: deriv = 0
            
        return(mvmtFloat(m.floor(truediv.value),deriv))

    def __rfloordiv__(self, other):
        other = mvmtFloat(other)
        return other.__floordiv__(self)

    def __truediv__(self, other):
        try:
            value = self.value/other.value
            deriv = ((other.value*self.deriv) - (self.value*other.deriv)) / other.value**2
            return mvmtFloat(value,deriv)
        except AttributeError:
            other = mvmtFloat(other,0)
            return self/other

    def __rtruediv__(self, other):
        other = mvmtFloat(other)
        return other.__truediv__(self)

    def __mod__(self, other):
        '''
        Implements modulo operator support. 
        
        This function in invoked when the dividend ("a" in "a modulo n") is an 
        mvmtFloat.

        The remainder is returned as an mvmtFloat with derivative set to 1.
        '''
        # might be able to define it in terms of other overloaded operators:
        #return self - other // (self / other)
        try:
            value = self.value % other.value
            deriv = 1
        except AttributeError:
            value = self.value % other
            deriv = 1
        return mvmtFloat(value, deriv)    

    def __rmod__(self, other):
        '''
        Implements modulo operator support. 
        
        This function in invoked when the divisor ("n" in "a modulo n") is an 
        mvmtFloat but the dividend is not.

        The remainder is returned as an mvmtFloat with derivative set to 1.
        '''
        # might be able to define it in terms of other overloaded operators:
        #return other - self // (other / self)
        value = other % self.value
        deriv = 1
        return mvmtFloat(value, deriv)    

    def __abs__(self):
        '''Implements the absolute value function
        
        The derivative of the absolute value of x is:
        -1 where x<0
        undefinted where x=0
        1 where x>0
        '''
        value = np.absolute(self.value)
        if self.value == 0:
            deriv = np.inf
        elif self.value<0:
            if isinstance(self.deriv, np.ndarray):
                deriv=np.empty(self.deriv.shape)
                deriv[:]=-1
            else:
                deriv=-1
        else: # self.value>0
            if isinstance(self.deriv, np.ndarray):
                deriv=np.empty(self.deriv.shape)
                deriv[:]=1
            else:
                deriv=1
        return(mvmtFloat(value,deriv))

    def __neg__(self):
        ''' 
            implements negation operation
        '''
        value = -1*self.value
        deriv = -1*self.deriv
        return(mvmtFloat(value,deriv))

    def __pos__(self):
        # I'm pretty sure that __pos__ has no effect on floats or ints, so just return a new mvmtFloat with the same attributes as self
        return(mvmtFloat(self.value,self.deriv))

    __radd__ = __add__
    __rmul__ = __mul__

    #
    # Comparison operators
    #   see: https://docs.python.org/3/library/operator.html
    #

    def __ge__(self, other):
        "Same as a >= b"
        try:
            return self.value >= other.value
        except AttributeError:
            return self.value >= other

    def __gt__(self, other):
        "Same as a > b"
        try:
            return self.value > other.value
        except AttributeError:
            return self.value > other
    
    def __le__(self, other):
        "Same as a <= b"
        try:
            return self.value <= other.value
        except AttributeError:
            return self.value <= other

    def __lt__(self, other):
        "Same as a < b"
        try:
            return self.value < other.value
        except AttributeError:
            return self.value < other
    
    def __eq__(self, other):
        " evaluates equaltiy for value and derivative attributes "
        try:
            if isinstance(self.deriv,np.ndarray):
                return (self.value==other.value) and ((self.deriv==other.deriv).all())
            else:
                return (self.value==other.value) and (self.deriv==other.deriv)
        except AttributeError:
            return(False)

    def __ne__(self, other):
        " evaluates inequaltiy for value and derivative attributes "
        try:
            if isinstance(self.deriv,np.ndarray):
                return (self.value!=other.value) or ((self.deriv!=other.deriv).any())
            else:
                return (self.value!=other.value) or (self.deriv!=other.deriv)
        except AttributeError:
            return(True)

#
# Trig functions
#   see: https://docs.python.org/3/library/math.html
#

def sin(x):
    try:
        return mvmtFloat(m.sin(x.value), m.cos(x.value)*x.deriv)        
    except AttributeError:
        return m.sin(x)
    except TypeError:
        return mvmtFloat(sin(x.value), cos(x.value)*x.deriv)

def cos(x):
    try:
        return mvmtFloat(m.cos(x.value), -m.sin(x.value)*x.deriv)        
    except AttributeError:
        return m.cos(x)
    except TypeError:
        return mvmtFloat(cos(x.value), -sin(x.value)*x.deriv)
    
def tan(x):
    try:
        return mvmtFloat(m.tan(x.value), (1/(cos(x.value)**2))*x.deriv)        
    except AttributeError:
        return m.tan(x)

def asin(x):
    try:
        return mvmtFloat(m.asin(x.value), (1/m.sqrt(1-x.value**2))*x.deriv)        
    except AttributeError:
        return m.asin(x)
    except ValueError:
        raise ValueError("math domain error -- valid for (-np.pi/2 <= f(x)<= np.pi/2)")
    
def acos(x):
    try:
        return mvmtFloat(m.acos(x.value), (-1/m.sqrt(1-x.value**2))*x.deriv)        
    except AttributeError:
        return m.acos(x)
    except ValueError:
        raise ValueError("math domain error -- valid for (0 <= f(x)<= np.pi)")

def atan(x):
    try:
        return mvmtFloat(m.atan(x.value), (1/(1+x.value**2))*x.deriv)        
    except AttributeError:
        return m.atan(x)

#
# Hyperbolic functions
#   see: https://docs.python.org/3/library/math.html
#

def asinh(x):
    try:
        return mvmtFloat(m.asinh(x.value), (1/m.sqrt(1+x.value**2))*x.deriv)        
    except AttributeError:
        return m.asinh(x)

def acosh(x):
    try:
        return mvmtFloat(m.acosh(x.value), (1/m.sqrt(x.value**2-1))*x.deriv)        
    except AttributeError:
        return m.acosh(x)
    except ValueError:
        raise ValueError("math domain error -- x must be greater 1")

def atanh(x):
    try:
        return mvmtFloat(m.atanh(x.value), (1/(1-x.value**2))*x.deriv)        
    except AttributeError:
        return m.atanh(x)
    except ValueError:
        raise ValueError("math domain error -- |x| must be less than 1")

def sinh(x):
    try:
        return mvmtFloat(m.sinh(x.value), m.cosh(x.value)*x.deriv)        
    except AttributeError:
        return m.sinh(x)

def cosh(x):
    try:
        return mvmtFloat(m.cosh(x.value), m.sinh(x.value)*x.deriv)        
    except AttributeError:
        return m.cosh(x)

def tanh(x):
    try:
        return mvmtFloat(m.tanh(x.value), (1/(m.cosh(x.value)**2))*x.deriv)        
    except AttributeError:
        return m.tanh(x)

#
# Power and logarithmic functions
#   see: https://docs.python.org/3/library/math.html
#

def exp(x):
    try:
        return mvmtFloat(m.exp(x.value), m.exp(x.value)*x.deriv)
    except AttributeError:
        return m.exp(x)
    except TypeError:
        return mvmtFloat(exp(x.value), exp(x.value)*x.deriv)

def log(x, base=None):
    if not isinstance(x, mvmtFloat):
        if x < 0:
            raise ValueError("Cannot take log of negative number")
        if base:
            return m.log(x, base)
        else:
            return m.log(x)
    else:
        if base:
            return mvmtFloat(m.log(x.value,base),(1/x.value)*x.deriv/m.log(base))
        else:
            return mvmtFloat(m.log(x.value),(1/x.value)*x.deriv)
   
def pow(x, y):
    
    if isinstance(x,mvmtFloat):
    
        if not isinstance(y, mvmtFloat): 
            if x.value >= 0:
                return mvmtFloat(x.value**np.float(y), y*x.value**np.float(y-1)*x.deriv)
            elif x.value < 0:
                if float(y).is_integer():
                    return mvmtFloat(x.value**np.float(y), y*x.value**np.float(y-1)*x.deriv)
                
                else:
                    raise ValueError("Cannot take a negative base to a fractional power")

        elif x.value > 0:
            return mvmtFloat(x.value**np.float(y.value), 
                            (x.value**np.float(y.value))*((x.deriv/x.value)*y.value + y.deriv*m.log(x.value)))

        elif x.value < 0:
            #Check if y is fractional
            if float(y).is_integer():
                return mvmtFloat(x.value**np.float(y.value), 
                                (x.value**np.float(y.value))*((x.deriv/x.value)*y.value - y.deriv*m.log(np.abs(x.value))))

            else:
                raise ValueError("Cannot take a negative base to a fractional power")
            
        elif x.value == 0:
            raise ValueError("Cannot take the derivative of an exponential function whose base is zero - pow(x,y)")
    
    else:
        if not isinstance(y,mvmtFloat):
            return x**y 
        
        else: 
            if x >= 0:
                return mvmtFloat(x**np.float(y.value),
                                x**np.float(y.value)*m.log(x)*y.deriv)    
            elif x < 0:
                if float(y.value).is_integer():
                    return mvmtFloat(x**np.float(y.value),
                                    x**np.float(y.value)*m.log(np.abs(x))*y.deriv)
                else:
                    raise ValueError("Cannot take a negative base to a fractional power")

def sqrt(x):
    # just use overloaded power operator
    return x**(1/2)

def logistic(x):
    # supporting standard logistic function only, not generalized form
    try:
        v = (1.0 / (1.0 + m.exp(-x.value)))
        return mvmtFloat(v, v * (1 - v) * x.deriv)
    except AttributeError:
        return (1.0 / (1.0 + m.exp(-x)))

#
# Angular Conversion
#   see: https://docs.python.org/3/library/math.html
#

def degrees(x):
        return x * (180 / m.pi)

def radians(x):
        return x / (180 / m.pi)

#
# Calculus functions
#

def partials(f, in_x, BY_NAME=False):
    """
    calculates partials derivatives of scalar function f with respect to
    scalar or list of parameters in in_x

    INPUTS
    ======
    f: function to calculate partials of, required
    in_x: input variables to evaluate function at.
          type: scalar, list of scalars, or 1-D np.array  
                if list, all variables must be mvmtFloat type. required

    RETURNS
    =======
    mvmtFloat

    NOTES
    =====
    PRE:
        - two inputs

    POST:
        - f and in_x are not changed by this function
        - returns a new mvmtFloat

    EXAMPLES
    ========
    >>> def test_func(a, b):
            return a * b
    >>> f = test_func
    >>> partials(f,[2,1])
    [mvmtFloat with Value: 2, Derivative: [1. 2.]]
    """  

    # this is some heavy-handed validation.
    # it would be better to duck-type. future improvement :)
    try:        
        nx = len(in_x)
        # if len worked, in_x is an mvmtFloat or a list or numpy.ndarray()
        if isinstance(in_x, np.ndarray):
            if nx == 1 and len(in_x.shape) == 2:
                # this is the case if there is a degenerate dimension
                x = in_x[0].tolist()
            else:
                x = in_x.tolist()
        elif isinstance(in_x, list):
            x = in_x.copy()
        elif isinstance(in_x, mvmtFloat):
            x = [in_x]
    except:
        # if len didn't work, in_x is a primitive type, i.e. int or float
        nx = 1
        x = [mvmtFloat(in_x)]
        BY_NAME = False

    # ensure that all elements are "mvmtFloat-like"
    for idx, _x in enumerate(x):
        try:
            _ = x[idx].value
            _ = x[idx].deriv
            _ = x[idx].name
        except:
            x[idx] = mvmtFloat(_x)
            BY_NAME = False

    # at this point, it safe to assume we have a list of mvmtFloats
    
    # count positional parameters in f
    sig = signature(f)
    n_params = 0
    for param in sig.parameters.values():
        if (param.kind == param.POSITIONAL_ONLY or
            param.kind == param.POSITIONAL_OR_KEYWORD):
            n_params += 1

    # if n_params > nx, abort
    if n_params > nx:
        msg = 'function takes {0} parameters but {1} were given'.format(
                n_params, nx)
        raise ValueError(msg)
    
    # handle the simpler case first.
    # if we are not matching by variable name, then we have to deal with:
    # [...]
    if not BY_NAME:
        if n_params == 1: 
            if nx == 1:
                # return value is a scalar mvmtFloat
                return f(mvmtFloat(x[0].value, x[0].deriv))
            else:
                # setup gradients and send everything in a list. 
                for idx, var in enumerate(x):
                    grad = np.zeros(nx)
                    grad[idx] = var.deriv
                    x[idx] = mvmtFloat(var.value, grad)
                # return value is scalar mvmtFloat with array deriv
                return f(x)
        else:
            # else: n_params > 1, and n_params must == nx
            for idx, var in enumerate(x):
                grad = np.zeros(nx)
                grad[idx] = var.deriv
                x[idx] = mvmtFloat(var.value, grad)

            # return value is scalar mvmtFloat with scalar value and array deriv        
            return f(*x)

    # else caller requested we match by name...
    
    # first, build a some lookups so we can find variables by name
    # and get them back in order later
    name_to_var = {}
    name_to_idx = {}
    for idx, var in enumerate(x):
        name_to_var[var.name] = var
        name_to_idx[var.name] = idx

    # form a new list of the variables we are going to send to f(), in order.
    # if we are missing any named inputs, throw a ValueError.
    new_x = []
    try:
        for idx, param in enumerate(sig.parameters.values()):
            var = name_to_var[param.name]
            new_x.append(mvmtFloat(var.value, var.deriv))
    except KeyError:
        msg = 'function parameter ({}) has no matching input'.format(param.name)
        raise ValueError(msg)

    # set the gradient vector for each var in new_x
    if nx > 1:
        for idx, var in enumerate(new_x):
            grad = np.zeros(nx)
            grad[idx] = var.deriv 
            new_x[idx].deriv = grad
    
    # call the function
    ret = f(*new_x)
    
    # special case here, we don't need to reorder anything
    if nx == 1:
        # return value is scalar mvmtFloat with scalar deriv
        return ret

    # re-order the derivatives to match the input variable order
    df_dparam = ret.deriv
    ret.deriv = np.zeros(nx)

    for idx, param in enumerate(sig.parameters.values()):
        ret.deriv[name_to_idx[param.name]] = df_dparam[idx]

    # return value is scalar mvmtFloat with array deriv
    return ret

def jacobian(in_f, in_x, BY_NAME=True):
    """
    calculates jacobian matrix for a vector of functions and a vector of input
    variables

    INPUTS
    ======
    in_f: scalar or list of functions to calculate partials of, required
    in_x: input variables to evaluate function at.
          type: scalar, list of scalars, or 1-D np.array  
                if list, all variables must be mvmtFloat type. required

    RETURNS
    =======
    numpy.ndarray of dimension [# of functions, # of variables]

    NOTES
    =====
    PRE:
        - two inputs

    POST:
        - in_f and in_x are not changed by this function
        - returns a new numpy.ndarray

    EXAMPLES
    ========
    >>> def func1(a, b):
            return a * b
    >>> def func2(a, b):
            return a / b           
    >>> functions = [func1, func2]
    >>> variables = [2,1]
    >>> jacobian(functions, variables)
    [[ 1.  2.]
    [ 1. -2.]]
    """
    try:
        nf = len(in_f)
        f = in_f
    except TypeError:
        nf = 1
        f = in_f

    try:
        nx = len(in_x)
    except TypeError:
        nx = 1 # in_x is a primitive scalar
        BY_NAME = False

    if nf > 1:
        J = np.zeros((nf, nx))

        for idx, func in enumerate(f):
            J[idx,:] = partials(func, in_x, BY_NAME).deriv
    else:
        J = partials(f, in_x, BY_NAME).deriv

    return J

def bound_jacobian(obj_func): 
    '''
    bound_jacobian is just a simple closure to bind a user's objective function
    to the jacobian function. This is useful in scenarios where the user must pass
    a function that calculates derivatives of a specific function, for example, to
    scipy minimizers.

    in this example, obj_func is an objective function, and x0 is a vector

    Example:
    ========

    >>> J = bound_jacobian(obj_func)
    >>> result = sp.optimize.minimize(obj_func, x0, jac=J, method='BFGS')

    '''
    def _F(x):
        return jacobian(obj_func,x) 
    return _F

#-------------------------------------------------------------------------------
# if __name__ == "__main__":
#     import numpy as np
#     print("\n\n")

# the following tests the logistic function
    '''
    x = 1.23456
    eps = 1e-7
    f = logistic

    print('x=',x)
    print(f(x), (f(x)-f(x-eps)) / eps )
    print(f(mvmtFloat(x)), "\n")

    print('x=',-x)
    print(f(-x), (f(-x)-f(-x-eps)) / eps )
    print(f(mvmtFloat(-x)))
    '''

# the following tests the log function with change of base
    '''
    x = 123.456
    eps = 1e-7
    dx = (m.log(x,7) - m.log(x-eps,7)) / eps
    print(x, m.log(x), m.log(x,7), dx)

    x = mvmtFloat(123.456)
    print(x)
    print(log(x))
    print(log(x,7))
    '''

    # the following tests 2nd derivative of sin()
    '''
    x = mvmtFloat(mvmtFloat(np.pi/4))
    print(x)
    print(sin(x))
    '''

# the following tests the jacobian function for functions with one variable
    '''
    def f(x):
        return exp(sin(x))-cos(x**0.5)*sin((cos(x)**2+x**2)**0.5)

    def f_sqrt(x):
        return exp(sin(x))-cos(sqrt(x))*sin(sqrt(cos(x)**2+x**2))

    def df(x):
        return exp(sin(x))*cos(x) + (sin((x**2 + cos(x)**2)**(0.5))*sin(x**(0.5)))/(2*x**(0.5)) - (cos((x**2 + cos(x)**2)**(0.5))*cos(x**(0.5))*(2*x - 2*cos(x)*sin(x)))/(2*(x**2 + cos(x)**2)**(0.5))

    x = 2.0
    print(f(x))
    print(f_sqrt(x))
    print(df(x))

    x = mvmtFloat(2)
    print(f(x))
    print(f_sqrt(x))
    print(df(x))
    '''

# the following is more testing of experimental 2nd derivative
    '''
    print('--- 2nd derivative ---')
    xx = mvmtFloat(mvmtFloat(2))
    print( (f(xx).deriv).deriv )
    print( (f_sqrt(xx).deriv).deriv )

    flist = [f, f_sqrt, df]

    print( jacobian(f,x) )
    print( jacobian(flist,x) )

    def f(x,y):
        return exp(sin(x))-cos(x**0.5)*sin((cos(x)**2+x**2)**0.5) / exp(y)

    def f_sqrt(x,y):
        return exp(sin(x))-cos(sqrt(x))*sin(sqrt(cos(x)**2+x**2)) / exp(y)

    y = mvmtFloat(4)

    flist = [f, f_sqrt]
    xlist = [x, y]
    print( jacobian(flist, xlist) )
    
    a = mvmtFloat(2)
    b = mvmtFloat(3)
    c = mvmtFloat(4)

    '''

# the following tests jacobian / partials for functions with multiple variables
    '''
    
    x = mvmtFloat(1, name='x')
    y = mvmtFloat(2, name='y')
    a = mvmtFloat(3, name='a')
    b = mvmtFloat(4, name='b')
    c = mvmtFloat(5, name='c')

    f = sin
    
    print('\ntest', 1)
    print(partials(f, x))               # test x is scalar, no name validation
    
    print('\ntest', 2)
    print(partials(f, x, BY_NAME=True)) # test x is scalar, by name that matches
    
    print('\ntest', 3)
    try:
        print(partials(f, y, BY_NAME=True)) # test y is scalar, name doesn't match
    except ValueError as e:
        print(e)

    print('\ntest', 4)
    print(partials(f, [x]))             # test x is list of correct length

    print('\ntest', 5)
    try:
        print(partials(f, [x,y]))       # test x is too long, 
                                        # but don't match by name,
                                        # so call function on all variables
    except TypeError as e:
        print(e)
    
    def f1(x,a):
         return x*a

    print('\ntest', 6)
    try:
        print(partials(f1, x))          # test x is too short
    except ValueError as e:
        print(e)

    print('\ntest', 7)
    try:
        print(partials(f1, x, BY_NAME=True)) # test x is too short, 
                                             # but matches 1 name
    except ValueError as e:
        print(e)

    print('\ntest', 8)
    try:
        print(partials(f1, [x,y], BY_NAME=True))    # not all names match
    except ValueError as e:
        print(e)

    print('\ntest', 9) # test x is too long, but has match in first spot
    p = partials(f, [x,y], BY_NAME=True)
    print(p) 

    print('\ntest', 10)
    print(partials(f, [y,x], BY_NAME=True)) # test x is too long, 
                                            # but has match in second spot

    def f2(x,y,a,b,c):
        return x*y*a*b*c

    xlist = [x,y,a,b,c]

    print('\ntest', 11)
    print( partials(f2, xlist) ) # test nx == n_params, no match by name

    # test nx = n_params, match by name, variables are out of order
    print('\ntest', 12)
    xlist = [a,b,c,x,y]
    print( partials(f2, xlist, BY_NAME=True) ) 

    def f3(x,y,a,b,c):
        return x+y+a+b+c

    def f4(c,b,a,y,x):
        return x*y*a*b*c

    # test jacobian, with all functions with same number of params
    print('\ntest', 13)
    flist = [f2,f3,f4]
    J = jacobian(flist, xlist)
    print(J)


    # test jacobian, with functions with different numbers of params
    print('\ntest', 14)
    flist = [f, f1, f2,f3,f4]
    J = jacobian(flist, xlist)
    print(J)

    # test optimized scenario, where user just wants variables 
    # sent by position rather than name
    
    def f5(x,y,a,b,c):
        return 1*x + 2*y + 3*a + 4*b + 5*c

    def f6(c,b,a,y,x):
        return 1*x + 2*y + 3*a + 4*b + 5*c
    
    print('\ntest', 15)
    flist = [f5, f6]
    
    J = jacobian(flist, xlist, BY_NAME=False)
    print(J)

    J = jacobian(flist, xlist, BY_NAME=True)
    print(J)  


    print('\ntest 16')
    # test where x is too long, match by name,
    print(jacobian(f, [x,y], BY_NAME=True)) 
    print('\n')

    def f7(x):
        return x[0]*x[1]*x[2]*x[3]*x[4]

    print('\ntest 17')
    # test where x is too long, don't match by name,
    print( partials(f7, [x,y,a,b,c]) )
    print( jacobian(f7, [x,y,a,b,c], BY_NAME=False) )
    print('\n')

    '''

    # xlist = [ x y ]

    # J:
    # [ df2/dx  df2/dy df2/da df2/db df2/dc ]
    # [ df1/dx  0      df1/da      0      0 ]

    # [ df2/dx  df2/dy df2/da df2/db df2/dc ]
    # [ df1/dx  df2/dy      0      0      0 ]

# the following is a collection of older tests
    """   

    def test_func(x):
        return x * sin(x)**2

    def dtest_func1_dx(x):
        return sin(x)**2 + 2 * x * m.cos(x) * m.sin(x)
    
    f = test_func
    x = mvmtFloat(-3)
    p = partials(f, x)

    print(x)
    print(p)

 

    x = -3
    print(test_func(x))
    print(dtest_func1_dx(x))

    print("\n")
    def test_func_2(x, y):
        return sqrt(x) * sin(y) + (x**y)

    def test_func_2_dx(x, y):
        return m.sin(y) / (2*x**(1/2)) + x**(y-1)*y

    def test_func_2_dy(x, y):
        return x**(1/2)*m.cos(y) + x**y*m.log(x)
    
    # sin(2)+1
    # sin(2)/2 + 2
    # cos(2)

    f = test_func_2

    # here we are setting up the gradient vectors manually:
    x = mvmtFloat(1.0, np.array([1,0]))
    y = mvmtFloat(2.0, np.array([0,1]))
    ff = f(x,y)
    print(ff)

    # show it works with scalar ints as input
    x = 1
    y = 2
    p = partials(f, [x, y])
    print(p)
    j = jacobian(f, [x,y])
    print(j)

    # show it works with scalar floats as input
    x = 1.0
    y = 2.0
    p = partials(f, [x, y])
    print(p)
    j = jacobian(f, [x,y])
    print(j)

    # show it works with mvmtFloats, but without setting gradients
    x = mvmtFloat(1)
    y = mvmtFloat(2)
    p = partials(f, [x, y])
    print(p)
    j = jacobian(f, [x,y])
    print(j)

    # show it works with a mix of scalars and mvmtFloats
    x = 1.0
    y = mvmtFloat(2)
    p = partials(f, [x, y])
    print(p)
    j = jacobian(f, [x,y])
    print(j)

    # show it works without predeclaring x and y
    print(partials(f, [1,2]))

    x = 1
    y = 2
    print("expected value: ", test_func_2(x, y))
    #print("expected value: ", m.sin(2)+1)
    print("expected partial for first arg", test_func_2_dx(x, y))
    #print("expected partial for first arg", m.sin(2)/2 + 2)
    print("expected partial for second arg", test_func_2_dy(x, y))
    #print("expected partial for second arg", m.cos(2))




    # def test_func4(a, b):
    #     return a * b
    # f = test_func4
    # print(partials(f,[2,1]))

    # a = 12.5
    # b =  5.5
    # print( a %  b, mvmtFloat( a) % mvmtFloat( b), mvmtFloat( a) %  b,  a % mvmtFloat( b) )
    # print(-a %  b, mvmtFloat(-a) % mvmtFloat( b), mvmtFloat(-a) %  b, -a % mvmtFloat( b) )
    # print( a % -b, mvmtFloat( a) % mvmtFloat(-b), mvmtFloat( a) % -b,  a % mvmtFloat(-b) )
    # print(-a % -b, mvmtFloat(-a) % mvmtFloat(-b), mvmtFloat(-a) % -b, -a % mvmtFloat(-b) )

    # a = 15
    # b =  3
    # print( a %  b, mvmtFloat( a) % mvmtFloat( b), mvmtFloat( a) %  b,  a % mvmtFloat( b) )
    # print(-a %  b, mvmtFloat(-a) % mvmtFloat( b), mvmtFloat(-a) %  b, -a % mvmtFloat( b) )
    # print( a % -b, mvmtFloat( a) % mvmtFloat(-b), mvmtFloat( a) % -b,  a % mvmtFloat(-b) )    
    
    # def test_func(a, b):
    #     return a * b
    # f = test_func
    # x = [mvmtFloat(2), mvmtFloat(3)]
    # print(partials(f,x))
    
    # def test_func(a, b):
    #     return a * b

    # def test_func_2(a, b):
    #     return sin(a) * b

    # def test_func_3(a, b):
    #     return m.sin(a) * b

    # def test_func_4(a, b):
    #     return np.sin(a) * b

    # print("\n\n")

    # a = mvmtFloat(1)
    # b = mvmtFloat(2)
    # c = mvmtFloat(2)

    # print(a)
    # print(b)
    # print(c)
    # print( "a >= b: ", a >= b)
    # print( "b >= a: ", b >= a)
    # print( "c >= b: ", c >= b)

    # print("\n\n")  

    # a = mvmtFloat(1, 1)
    # print( "a      = ", a)
    # print( "a + 1  = ", a+1)
    # print( "1 + a  = ", 1+a)
    # print( "log(a) = ", log(a) )
    # print( "exp(a) = ", exp(a) )
    # print( "a**2   = ", a**2 )
    # print( "2**a   = ", 2**a )
    # print( "2*a    = ", 2*a )
    # print( "a*2    = ", a*2 )

    # a += 2
    # print( "a+=2   = ", a)

    # # b = mvmtFloat(3,1) 
    # # print( "b      = ", b)
    # # print( "a**b   = ", a**b )

    # print("\n")
    # a = mvmtFloat(3, np.array([1,0]))
    # print( "a      = ", a)
    # print( "a + 1  = ", a+1)
    # print( "2*a    = ", 2*a )
    # print( "a**2   = ", a**2 )

    # print("\n")
    # a = mvmtFloat(np.array(3), np.array([1,0]))
    # b = mvmtFloat(np.array(7), np.array([0,1]))
    # print( "a      = ", a)
    # print( "b      = ", b)
    # print( "a*b    = ", a*b )
    # print( "a**2*b = ", a**2*b )

    # print("\n")
    # print( "test_func(a, b) = ",   test_func(a, b) )
    # print( "test_func_2(a, b) = ", test_func_2(a, b) )
    # #print( "test_func_3(a, b) = ", test_func_3(a, b) )
    # #print( "test_func_4(a, b) = ", test_func_4(a, b) )
    # print( "test_func_4(a, b) = ", test_func_4(a.value, b.value) )

    # print("\n")

    # def f(x):
    #     m = 2
    #     b = 1
    #     return m * x + b 

    # x = mvmtFloat(7)

    # print("f(x) = m * x + b")
    # print("x = ", x)
    # print("f(x) = ", f(x))
    """