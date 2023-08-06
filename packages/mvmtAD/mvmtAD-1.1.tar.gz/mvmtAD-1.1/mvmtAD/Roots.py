from mvmtAD.AD import mvmtFloat,jacobian
import numpy as np
import scipy.linalg as linalg


def root_scalar(f, x0 = None, method = None, bracket = None, epsilon = 1e-10 ,max_iter = 100):
    if method == 'bisection':
        if bracket == None:
            raise TypeError("Bracket cannot be Nonetype - please provide bracket for the root")
        else:
            return bisection(f,bracket[0],bracket[1], max_iter)
    if method == 'secant':
        if bracket == None:
            raise TypeError("Initial guesses cannot be Nonetype - please provide two guesses for the root")
        else:
            return secant(f,bracket[0],bracket[1], max_iter)
    if method == 'newton':
        if x0 == None:
            raise TypeError("Initial guees x0 cannot be Nonetype - please provide initial guess")
        else:
            return newton(f,x0,epsilon, max_iter)
    if method == 'newton_hybrid':
        if bracket == None:
            raise TypeError("Bracket cannot be Nonetype - please provide bracket for the root")
        else:
            return newton_hybrid(f,bracket[0],bracket[1])    
    
def root(F, x = None, method = None, epsilon = 1e-10 ,max_iter = 100):
    if method == 'Newton':
        if x == None:
            raise TypeError("Initial guees x cannot be Nonetype - please provide initial guess")
        else:
            return Newton(F, x, epsilon, max_iter)
    if method == 'Broyden':
        if x == None:
            raise TypeError("Initial guees x cannot be Nonetype - please provide initial guess")
        else:
            return Broyden(F, x, epsilon, max_iter)
    if method == 'Broyden_inverse_update':
        if x == None:
            raise TypeError("Initial guees x cannot be Nonetype - please provide initial guess")
        else:
            return Broyden_inverse_update(F, x, epsilon, max_iter)
        
def bisection(f,a,b,max_iter=100):
    '''
    Approximate solution of f(x)=0 using bisection method.

    Parameters
    ----------
    f : function
        Function for which we are searching for a solution
    a, b: number
        Bracket containing a root of the function
        sign (f(a)) != sign (f(b))
    max_iter : integer
        Maximum number of iterations

    Returns
    -------
    xn : mvmtFloat object
        A root of the function provided 
    Examples
    --------
    >>> f = lambda x: x**3 + x**2 - x
    >>> bisection(f, 0.5, 1, 50)
    0.6180339887498949
    '''
    
    #check initial bracket provided 
    if a==b:
        raise ValueError("Bad initial range provided - root must be bracketed in range provided")
        #return None
    if f(a)*f(b) >= 0: #check that function evaluated at end of range have different signs
        raise ValueError("Bad initial range provided - root must be bracketed in range provided")
        #return None
    
    #check for solution in provided bracket
    for n in range(0,max_iter):
        mid = (a + b)/2
        f_mid = f(mid)
        if f(a)*f_mid < 0:
            b = mid
        elif f(b)*f_mid < 0:
            a = mid
        elif f_mid == 0:
            return mid
        else:
            print("Bisection method failed")
            return None
    return (a + b)/2

def secant(f,a,b,max_iter=100):
    '''
    Approximate solution of f(x)=0 using secant method.

    Parameters
    ----------
    f : function
        Function for which we are searching for a solution
    a, b: number
        Two initial guesses for the root of the function
        a != b
    max_iter : integer
        Maximum number of iterations

    Returns
    -------
    xn : mvmtFloat object
        A root of the function provided 
    Examples
    --------
    >>> f = lambda x: x**3 + x**2 - x
    >>> secant(f, 0.5, 1, 50)
    0.6180339887498948
    '''
    
    #check initial bracket provided 
    if a==b:
        raise ValueError("Bad initial range provided - two distinct guesses must be provided")
        #return None
    #if f(a)*f(b) >= 0: #check that function evaluated at end of range have different signs
    #    raise ValueError("Bad initial range provided - root must be bracketed in range provided")
    #    #return None
    
    for n in range(0,max_iter):
        mid = a - f(a)*(b - a)/(f(b) - f(a))
        f_mid = f(mid)
        if f(a)*f_mid < 0:
            b = mid
        elif f(b)*f_mid < 0:
            a = mid
        elif f_mid == 0:
            return mid
        else:
            print("Secant method failed")
            return None
    return a - f(a)*(b - a)/(f(b) - f(a))

def newton(f,x0,epsilon,max_iter=100):
    '''
    Approximate solution of f(x)=0 by Newton's method.

    Parameters
    ----------
    f : function
        Function for which we are searching for a solution f(x)=0.
    x0 : number
        Initial guess for a solution f(x)=0.
    epsilon : number
        Stopping criteria is abs(f(x)) < epsilon.
    max_iter : integer
        Maximum number of iterations of Newton's method.

    Returns
    -------
    xn : mvmtFloat object
        A root of the function provided

    Examples
    --------
    >>> f = lambda x: x**3 + x**2 - x
    >>> newton(f,1,1e-20,10)
    0.6180339887498949
    '''
    xn = mvmtFloat(x0)
    for n in range(0,max_iter):
        fval = f(xn).value
        if abs(fval) < epsilon:
            return xn.value
        fderiv = f(xn).deriv
        if fderiv == 0:
            print('Zero derivative. No solution found.')
            return None
        xn = xn - fval/fderiv
    print('Exceeded maximum iterations. No solution found.')
    return None
        
def newton_hybrid(f,a,b):
    '''
    Approximate solution of f(x)=0 by a mix of Newton and bisection methods.
    In cases where the solution is not converging or  the first derivative is zero,
    hybrid uses bisection

    Parameters
    ----------
    f : function
        Function for which we are searching for a solution f(x)=0.
    x0 : number
        Initial guess for a solution f(x)=0.
    epsilon : number
        Stopping criteria is abs(f(x)) < epsilon.
    max_iter : integer
        Maximum number of iterations of Newton's method.

    Returns
    -------
    xn : mvmtFloat object
        A root of the function provided

    Examples
    --------
    >>> f = lambda x: x**3 + x**2 - x
    >>> newton_hybrid(f,0.5,1)
    0.6180339887498949
    '''
    
    epsilon = 1e-10
    if a==b:
        raise ValueError("Bad initial range provided - root must be bracketed in range provided")
        #return None
    if f(a)*f(b) >= 0: #check that function evaluated at end of range have different signs
        raise ValueError("Bad initial range provided - root must be bracketed in range provided")
        #return None
    
    if b < a: # swap so a is the smaller end of the bracket
        tmp = a
        a = b
        b = tmp
    
    if f(a) == 0:
        return a
    elif f(b) == 0:
         return b
        
    xn = (a + b)/2 # start at the midpoint
    xn = mvmtFloat(xn)
    fval = f(xn).value
    fderiv = f(xn).deriv
        
    if abs(fval) < epsilon:
        return xn.value
        
    while abs(fval) > epsilon:
        #fval = f(xn).value
        #fderiv = f(xn).deriv
        
        if fderiv == 0: # if zero derivative force bisection
            return force_bisection(f,a, b)
                
        x_previous = xn 
        xn = xn - fval/fderiv
        delta = abs(xn - x_previous)
            
        if x_previous == xn: #converged on the solution
            return xn.value
            
        if xn < a or xn > b: #if it diverges force bisection
            return force_bisection(f,a,b)
            
        if abs(fval * 2) > abs(delta * fval): # if it is converging too slowly, force bisection
            return force_bisection(f,a,b)
         
def force_bisection(f,a,b):
    xn = (a + b)/2
    if f(a)*f(xn) < 0:
        return newton_hybrid(f,a,xn)
    else:
        return newton_hybrid(f,xn,b)              

##################################################
### Implementation of multivariate root finders###
##################################################

def Newton(F, x, epsilon, max_iter=100):
    """
    Approximate solution of F(x)=0 by Newton's method

    Parameters
    ----------
    F : function
        Function for which we are searching for a solution f(x)=0
    x0 : list
        Initial guess for a solution F(x)=0.
    epsilon : number
        Stopping criteria is abs(f(x)) < epsilon.
    max_iter : integer
        Maximum number of iterations
        Assumes max_iteration = 100 if not specified

    Returns
    -------
    x : mvmtFloat object
        Continues until abs(F_norm) < epsilon or max_iterations reached and returns x.
    n : number
        Number of iterations reached
        
    Examples
    --------
   >>> def f1(x):
       return x[0]**2 + x[1]**2 - 3

    >>> def f2(x):
        return 2.*x[1] - x[0]**2

   >>> F = [f1,f2]
   >>> x, n = Newton(F, x=[-2, 1], epsilon=1e-10, max_iter=100)
   >>> print(x)
   [-1.41421356  1.       ]
    """
    
    F_value = np.array(([func(x) for func in F]))
    F_norm = np.linalg.norm(F_value, ord=2)  # calculate the largest singular value
    counter = 0
    while abs(F_norm) > epsilon and counter < max_iter:
        J = np.array(jacobian(F,x))
        
        #solves system using QR for solving of least_squares problems
        Q, R = np.linalg.qr(J, mode ='complete')
        delta = linalg.solve_triangular(R[:len(F_value)], 
                                           Q.T[:len(F_value)].dot(-F_value), 
                                           lower=False)
        x = x + delta
        F_value = np.array([func(x) for func in F])
        F_norm = np.linalg.norm(F_value, ord=2)
        counter += 1
        
    if abs(F_norm) < epsilon:
        counter -=1
        return x, counter
    else:
        print('Exceeded maximum iterations. No solution found.')
        return None, counter

def Broyden(F, x, epsilon, max_iter=100):
    
    """
    Approximate solution of F(x)=0 by Broyden's method

    Parameters
    ----------
    F : function
        Function for which we are searching for a solution f(x)=0
    x0 : list
        Initial guess for a solution F(x)=0.
    epsilon : number
        Stopping criteria is abs(f(x)) < epsilon.
    max_iter : integer
        Maximum number of iterations
        Assumes max_iteration = 100 if not specified

    Returns
    -------
    x : mvmtFloat object
        Continues until abs(F_norm) < epsilon or max_iterations reached and returns x.
    n : number
        Number of iterations reached
        
    Examples
    --------
   >>> def f1(x):
       return x[0]**2 + x[1]**2 - 3

    >>> def f2(x):
        return 2.*x[1] - x[0]**2

   >>> F = [f1,f2]
   >>> x, n = Broyden(F, x=[-2, 1], epsilon=1e-10, max_iter=100)
   >>> print(x)
   [-1.41421356  1.        ]
    """
    
    F_value = np.array(([func(x) for func in F]))
    F_norm = np.linalg.norm(F_value, ord=2)  # calculate the largest singular value
    J = np.array(jacobian(F,x))
    counter = 0
    while abs(F_norm) > epsilon and counter < max_iter:

        Q, R = np.linalg.qr(J, mode ='complete')
        delta = linalg.solve_triangular(R[:len(F_value)], 
                                           Q.T[:len(F_value)].dot(-F_value), 
                                           lower=False)
        x = x + delta
        F_value_new = np.array([func(x) for func in F])
        diff = F_value_new - F_value
        J = J + (np.outer((diff - np.dot(J,delta)),delta)) / np.dot(delta,delta)
        F_value = F_value_new
        F_norm = np.linalg.norm(F_value, ord=2)
        counter += 1
        
    if abs(F_norm) < epsilon:
        counter -=1
        return x, counter
    else:
        print('Exceeded maximum iterations. No solution found.')
        return None, counter

def Broyden_inverse_update(F, x, epsilon, max_iter=100):
    
    """
    Approximate solution of F(x)=0 by Broyden's inverse update method

    Parameters
    ----------
    F : function
        Function for which we are searching for a solution f(x)=0
    x0 : list
        Initial guess for a solution F(x)=0.
    epsilon : number
        Stopping criteria is abs(f(x)) < epsilon.
    max_iter : integer
        Maximum number of iterations
        Assumes max_iteration = 100 if not specified

    Returns
    -------
    x : mvmtFloat object
        Continues until abs(F_norm) < epsilon or max_iterations reached and returns x.
    n : number
        Number of iterations reached
        
    Examples
    --------
   >>> def f1(x):
       return x[0]**2 + x[1]**2 - 3

    >>> def f2(x):
        return 2.*x[1] - x[0]**2

   >>> F = [f1,f2]
   >>> x, n = Broyden_inverse_update(F, x=[-2, 1], epsilon=1e-10, max_iter=100)
   >>> print(x)
   [-1.41421356  1.        ]
    """
    
    F_value = np.array(([func(x) for func in F]))
    F_norm = np.linalg.norm(F_value, ord=2)  # calculate the largest singular value
    J = np.array(jacobian(F,x))
    B = np.linalg.inv(J)
    counter = 0
    while abs(F_norm) > epsilon and counter < max_iter:

        s = np.dot(B, F_value)
        x = x + s
        F_value_new = np.array([func(x) for func in F])
        f_diff = F_value_new - F_value
        u = np.dot(B,f_diff)
        d = -1*s
        B = B + (np.dot(((d-u).dot(d)),B)) / np.dot(d,u)
        F_value = F_value_new
        F_norm = np.linalg.norm(F_value, ord=2)
        counter += 1
        
    if abs(F_norm) < epsilon:
        counter -=1
        return x, counter
    else:
        print('Exceeded maximum iterations. No solution found.')
        return None, counter


"""
############################################################
#demo1 of root finders
def f1(x):
    return x[0]**2 + x[1]**2 - 3

def f2(x):
    return 2.*x[1] - x[0]**2
  
F = [f1,f2]
x, n = Newton(F, x=[-2, 1], epsilon=1e-10)
print("Newton: roots = %s, num_iter = %s:" % (x,n))
x, n = Broyden(F, x=[-2, 1], epsilon=1e-10)
print("Broyden: roots = %s, num_iter = %s:" % (x,n))
x, n = Broyden_inverse_update(F, x=[-2, 1], epsilon=1e-10)
print("Broyden Inverse Update: roots = %s, num_iter = %s:" % (x,n))

def f3(x):
    return x[0]**3 + x[1] - 1

def f4(x):
    return x[1]**3 - x[0] + 1

F2 = [f3,f4]
x, n = Newton(F2, x=[0.5, 0.5], epsilon=1e-10)
print("Newton: roots = %s, num_iter = %s:" % (x,n))
x, n = Broyden(F2, x=[0.5, 0.5], epsilon=1e-10)
print("Broyden: roots = %s, num_iter = %s:" % (x,n))
x, n = Broyden_inverse_update(F2, x=[0.5, 0.5], epsilon=1e-10)
print("Broyden Inverse Update: roots = %s, num_iter = %s:" % (x,n))
####################################################################################
"""
# # demo of newton scalar root finding
# def f(x):
#     return x**3 + x**2 - x

# w = bisection(f, 0.5, 1, 50)
# print(w)
# x = secant(f, 0.5, 1, 50)
# print(x)
# y = newton(f, 1, 1e-20, 50)
# print(y)
# z = newton_hybrid(f,0.5,1)
# print(z)

# #demo of one where newton's fails but hybrid works
# def f(x):
#     return x**2 - 2*x

# w = bisection(f, 1, 3, 50)
# print(w)
# x = secant(f, 1, 3, 50)
# print(x)
# y = newton(f, 1, 1e-20, 50)
# print(y)
# z = newton_hybrid(f,1,3)
# print(z)

