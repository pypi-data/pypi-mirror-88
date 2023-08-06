import numpy as np
import numpy.linalg as ln
import scipy as sp
import scipy.optimize
from scipy.optimize import linesearch as ls
from mvmtAD.AD import jacobian, partials, bound_jacobian

def bfgs(in_f, in_x, **kwargs):
    """
    minimizer that implements the bfgs method for scalar or list of functions
    of more than one variable. if list of functions, they all must accept the
    same number of variables.

    INPUTS
    ======
    in_f: scalar or list of functions for minimization, required
    in_x: input variables to provide initial estimate. np.array. required

    keyword USE_SCIPY_LS: an optional boolian to specify that scipy's 
        line_search algorithm should be used to set the initial step size, 
        rather than the custom implementation here. Default is True.

    RETURNS
    =======
    numpy.ndarray of dimension [# of functions, # of variables]

    EXAMPLES
    ========
    where f is a callable function
    >>> r = bfgs(f, np.array([1,1]), USE_SCIPY_LS=False)
    [-3.99999988  0.99999966]
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

    if nf > 1:
        R = np.zeros((nf, nx))

        for idx, _f in enumerate(f):
            R[idx,:] = _bfgs_method_1d(_f, in_x, **kwargs)
    else:
        R = _bfgs_method_1d(f, in_x, **kwargs)

    return R

# Algorithm 6.1 BFGS Method from Numerical Optimization, 2006
def _bfgs_method_1d(f, x0, max_iter=100, eps=10e-7, USE_SCIPY_LS=True):

    # input x0 must be 1-D numpy.array
    if not isinstance(x0, np.ndarray):
        raise ValueError('input x0 must be np.ndarray type')

    # (CHECK SIZE HERE?)

    k = 0                   # init iteration counter
    n = len(x0)             # get size of input vector
    I = np.eye(n)           # init an identity matrix
    xk = x0                 # init vector to be used in iteration
    Hk = I                  # init hessian to identity
    conv = eps + 1          # init convergence criteria

    # get rid of the following line when we get rid of sp.optimize
    J = bound_jacobian(f)    # Derivative function of input objective function
    Gfk = partials(f,xk).deriv  # compute gradient at current position
    
    while True:
        pk = -np.dot(Hk, Gfk)   # compute search direction (eqn 6.18)

        # compute step size with line search that satisfies Wolfe (eqn 3.6)
        if USE_SCIPY_LS:
            ls_result = sp.optimize.line_search(f, J, xk, pk)
            ak = ls_result[0]
        else:
            ak = _line_search(f, xk, pk)
        
        if ak is None:
            raise Exception('line search algorithm failed.')

        xkp1 = xk + ak * pk # take the step to position at next iteration
        Gfkp1 = partials(f,xkp1).deriv

        conv = ln.norm(Gfkp1) # conv is the 2-norm
        if (conv < eps):
            xk = xkp1
            success = True
            break # success

        sk = xkp1 - xk      # calculate displacement (eqn 6.5)
        yk = Gfkp1 - Gfk    # calculate change in gradient (also eqn 6.5)
        
        ro = 1.0 / (yk.T @ sk) # (eqn 6.14)

        # update Hessian (eqn 6.17)
        tmp1 = (I - ro * sk @ yk.T)
        tmp2 = (I - ro * yk @ sk.T)
        tmp3 = ro * sk @ sk.T

        Hk = np.dot(tmp1, np.dot(Hk, tmp2)) + tmp3

        xk = xkp1           # set next position
        Gfk = Gfkp1         # set next gradient
        k += 1              # update count

        if (k > max_iter):
            success = False
            break # fail - warn on this case

    if success:
        return xk
    else: 
        raise Exception('BFGS method failed to converge!')

# Algorithm 3.5: Line Search Algorithm from Numerical Optimization, 2006
#  finds alpha that satisfies the strong Wolfe conditions
def _line_search(f, xk, pk):
    c1 = 1e-4
    c2 = 0.9
    max_iter = 10

    a0 = 0
    a1 = 1
    i = 1

    def phi(alpha):
        return f(xk + alpha * pk)

    def d_phi(alpha):
        return np.dot( partials(f, xk + alpha * pk).deriv, pk)

    phi_0 = phi(0)
    dphi_0 = d_phi(0)

    # Algorithm 3.6: "Zoom"" Algorithm from Numerical Optimization, 2006
    def _zoom(a_lo, a_hi, f, xk, pk):
        
        max_iter = 100
        i = 0

        while True:
            # interpolate using quadratic to find a trial step length aj
            aj = _quadratic_min(a_lo, phi(a_lo), d_phi(a_lo), a_hi, phi(a_hi))
        
            phi_aj = phi(aj)

            if (phi_aj > phi_0 + c1*aj*dphi_0) or (phi_aj >= phi(a_lo)):
                a_hi = aj
            else:
                dphi_aj = d_phi(aj)
                if np.absolute(dphi_aj) <= - c2*dphi_0:
                    alpha_star = aj
                    break
                if dphi_aj*(a_hi-a_lo) >= 0:
                    a_hi = a_lo
                a_lo = aj
            i += 1
            if i > max_iter:
                raise Exception('zoom algorithm failed in main loop.')
        return alpha_star
    # --- end of def zoom() ---

    ai = a1
    phi_prev = 0
    a_prev = 0

    while True:

        phi_ai = phi(ai)
        dphi_ai = d_phi(ai)

        if phi_ai > phi_0 + c1*ai*dphi_0 or (phi_ai >= phi_prev and i > 1):
            alpha_star = _zoom(a_prev, ai, f, xk, pk)
            break

        dphi_ai = d_phi(ai)

        if np.absolute(dphi_ai) <= -c2*dphi_0:
            alpha_star = ai
            break

        if dphi_ai >= 0:
            alpha_star = _zoom(ai, a_prev, f, xk, pk)
            break

        a_next = ai * 2
        a_prev = ai
        ai = a_next
        phi_prev = phi_ai
        phi_ai = phi(ai)

        i = i+1
        if i > max_iter:
            raise Exception('The line search algorithm did not converge')

    return alpha_star

def _quadratic_min(x1, y1, dx1, x2, y2):
    return x1 - dx1 / (2.0 * (y2 - y1 - dx1 * (x2 - x1)) / (x2 - x1)**2)
#-------------------------------------------------------------------------------
'''
if __name__ == "__main__":
    import numpy as np
    print("\n\n")

    # Objective function
    def f(x):
        return x[0]**2 - x[0]*x[1] + x[1]**2 + 9*x[0] - 6*x[1] + 20

    def g(x):
        return x[0]**2 - x[0]*x[1] + x[1]**2 + 7*x[0] - 4*x[1] + 20

    # Analytical Derivative of f(x)
    def fprime(x):
        return np.array([2 * x[0] - x[1] + 9, -x[0] + 2*x[1] - 6])

    def scipy_method(obj_func, x0, J=None, method='BFGS'):
        if J is None:
            J = bound_jacobian(obj_func)
        return sp.optimize.minimize(obj_func, x0, jac=J, method='BFGS')

    def scipy_method_2d(obj_func, x0, method='BFGS'):
        nf = len(obj_func)
        nx = len(x0)
        R = np.zeros((nf,nx))
        for idx, _f in enumerate(obj_func):
            res = scipy_method(_f, x0, method=method)
            R[idx,:] = res.x
        return R

#---------------------------------------------------------------------------

    print('\n -- f -- \n')
    r = scipy_method(f, np.array([1,1]))
    print(r)
    r = bfgs(f, np.array([1,1]))
    print(r)

    print('\n -- g -- \n')
    r = scipy_method(g, np.array([1,1]))
    print(r)

    print('\n -- 2d -- \n')
    r = scipy_method_2d([f,g], np.array([1,1]))
    print(r)

    r = bfgs([f,g], np.array([1,1]), USE_SCIPY_LS=False)
    print(r)
    print('\n')

    r = bfgs([f,g], np.array([1,1]))
    print(r)

    print('\n\n')

    def f(x):
        return x[0]**2 - x[0]*x[1] + x[1]**2 + 7*x[0] - 4*x[1] + 20

    J = bound_jacobian(f)
    ret = sp.optimize.minimize(f, np.array([1,1]), jac=J, method='BFGS')
    print(ret.x)

'''

