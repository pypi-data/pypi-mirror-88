# cs107-FinalProject

By MVMT107, group #30

Matthew Egan, Tommy Shay Hill, Victoria DiTomasso, Martha Obasi

### `mvmtAD` is an automatic differentiation package

For further background, examples, and explanation of `mvmtAD`'s functionality, please see our [full documentation](https://github.com/MVMT107/cs107-FinalProject/blob/master/docs/documentation.ipynb).

[![Build Status](https://travis-ci.com/MVMT107/cs107-FinalProject.svg?token=DAKJLdJcYRYRxFHVhhrB&branch=master)](https://travis-ci.com/MVMT107/cs107-FinalProject)

[![codecov](https://codecov.io/gh/MVMT107/cs107-FinalProject/branch/master/graph/badge.svg?token=3X1QDRG7ND)](https://codecov.io/gh/MVMT107/cs107-FinalProject)

### Installation Guide

`mvmtAD` can be installed using pip:

`pip install mvmtAD`

### `mvmtAD` contains three modules:

#### `AD`

Forward mode automatic differentiation module

- `mvmtFloat` class, which implements automated differentiation using operator overloading
- `partials()` function, which accepts a vector of instances of the `mvmtFloat` class and a function that accepts multiple variables and returns the input vector where the derivate attribute of each is the partial derivative of the input function with respect to that variable
- `jacobian()` function, which accepts a vector of instances of the mvmtFloat class and a vector of functions, and returns a matric of dimension (Number of Input Functions) x (Number of Input Variables), containing the partial derivative of each function with respect to each variable

Examples:

```python
from AD import mvmtFloat
import numpy as np

a = mvmtFloat(3, np.array([1,0]))
b = mvmtFloat(7, np.array([0,1]))

print('a=', a)
> a= mvmtFloat with Value: 3, Derivative: [1 0]

print('2*a=', 2*a )
> 2*a= mvmtFloat with Value: 6, Derivative: [2 0]

print('a**2*b=', a**2*b)
> a**2*b= mvmtFloat with Value: 63.0, Derivative: [42.  9.]
```

#### `Roots`

Root-finding

- Single-variable root-finding methods: `root_scalar()`, `bisection()`, `secant()`, `newton()`, `newton_bisection()`
- Multi-variable root-finding methods: `root()`,`Newton()`, `Broyden()`, `Broyden_inverse_update()`

Single-variable examples:

```python
def f(x):
    return x**3 + x**2 - x
    
v=root_scalar(f, bracket=[0.5,1], method='bisection')
print('v=',v)
> v= 0.6180339887498949

w=bisection(f, 0.5, 1, 50)
print('w=',w)
> w= 0.6180339887498949
```

Multi-variable examples:
```python
def f1(x):
    return x[0]**2 - x[1] + x[0]*cos(np.pi*x[0])
    
def f2(x):
    return x[0]*x[1] + exp(-x[1]) - x[0]**(-1)
    
F = [f1,f2]
x,n = root(F, x=[-2,1], method='Newton', epsilon=1e-10, max_iter=100)
print('root: roots = ', x)
> root: roots = [1.00000000e+00 2.11778121e-12]

x,n = Broyden_inverse_update(F, x=[-2,1], epsilon=1e-10)
print('Broyden Inverse Update: roots =', x)
> Broyden Inverse Update: roots = [-0.87106758 1.55934078]
```

#### `bfgs` Optimization

- bfgs(f, initial_guess, [max_iter, eps, USE_SCIPY_LS]): Run the BFGS optimizer

Example:
```python
def f(x):
    return x[0]**2 - x[0]*x[1] + x[1]**2 + 9*x[0] - 6*x[1] + 20

def g(x):
    return x[0]**2 - x[0]*x[1] + x[1]**2 + 7*x[0] - 4*x[1] + 20

r = bfgs([f,g], np.array([1,1]), USE_SCIPY_LS=False)
print(r)
> [[-3.99999988  0.99999966], [-3.33333318  0.33333303]]
```

---

### Broader Impacts and Software Accessibility

Auto differentiation (AD) is a widely applicable technique. It has been used, for example, in the study of chemical engineering processes (Castro 2000) and cancer treatment (Jee 2006), and broadly in machine learning (Baydin 2018). AD partakes in both the positive and negative impacts of those works. In exchange for this AD package being less complex than larger user-contributed code bases, and thus easier for inexperienced users to understand and contribute to, it costs computational power to it over other, more efficient, packages. In regard to software inclusivity, anyone with access to a computer capable of running Python (a free and open-source language) and connection to the internet will have the technological capability to use and contribute to this package. Pull requests will be reviewed and approved by the members of the MVMT107 group.

Users and contributors to this package need some knowledge of Python and Github, for which there are many tutorials available for free online. There are, however, known racial/ethnic disparities in who participates in computer science education (Google Inc & Gallup Inc). We provide some explanation of differentiation, but we recognize that there are disparities in the race/ethnicity and socioeconomic status of students who take advanced math courses (NSF, HSLS:09). Use of and contributions to this package would be welcome from any user, but we recognize that its documentation is written in English and is thus inequitably accessible to English speakers. The key information from the full documentation are written in the README.md files, but we recognize that the full documentation (written as a Jupyter notebook) is not currently compatible with many screen readers and thus not accessible to visually impaired users. We aim to remedy this barrier in the future.

References:

Baydin, Atilim Gunes, et al. “Automatic Differentiation in Machine Learning: A Survey.” *Journal of Machine Learning Research*,vol. 18, no. 153, pp. 1–43. 2018.

Castro, M.C. et al. “Automatic differentiation tools in the dynamic simulation of chemicalengineering processes” *Brazilian Journal of Chemical Engineering* 17(4-7), 373-382. 2000.

Google Inc. & Gallup Inc. ”Diversity Gaps in Computer Science: Exploring the Underrepresentation of Girls, Blacks and Hispanics” 2016. Retrieved from http://goo.gl/PG34aH.

Jee KW. et al. ”Implementation of Automatic Differentiation Tools for Multicriteria IMRT Optimization.” *Automatic Differentiation: Applications, Theory, and Implementations* edited by Martin Bucker et al., vol. 50, Springer-Verlag, 2006, pp. 225–34.

National Science Foundation, National Center for Science and Engineering Statistics, special tabulations (2016) of High School Longitudinal Study of 2009 (HSLS:09), National Center for Education Statistics. Retrieved fromhttps://nsf.gov/statistics/2018/nsb20181/report/sections/elementary-and-secondary-mathematics-and-science-education/high-school-coursetaking-in-mathematics-and-science.
