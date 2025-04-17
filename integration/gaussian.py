import sympy as sp
from sympy import nsimplify, pi, sqrt, E
from fractions import Fraction

def approximation(result):
    expr = result
    try:
        f = Fraction(str(expr)).limit_denominator()
    except Exception:
        return expr  # fallback to raw result if conversion fails
    
    approx_pi = nsimplify(expr, [pi], tolerance=1e-6)
    approx_e  = nsimplify(expr, [E],  tolerance=1e-6)

    sqrt_constants = [2, 3, 5, 7, 10]
    approx_sqrts = [(n, nsimplify(expr, [sqrt(n)], tolerance=1e-6)) for n in sqrt_constants]

    num = f.numerator
    denom = f.denominator

    # Check for pi
    if 'pi' in str(approx_pi) and len(str(approx_pi)) < 9:
        return approx_pi

    # Check for e
    if 'E' in str(approx_e) and len(str(approx_e)) < 8:
        return approx_e

    # Check for "nice" fraction
    if ((num < 100 and denom < 10) or (num < 10 and denom < 100)):
        return f

    # Check for square roots
    for n, approx in approx_sqrts:
        approx_str = str(approx)
        if 'sqrt' in approx_str and len(approx_str) < 14:
            return approx

    # Default to raw float
    return expr

def gaussian_quadrature_1_weighting_factor(a, b, expr):
    x = sp.symbols('x')
    fn = sp.lambdify(x, expr, "sympy")
    a = sp.sympify(a)
    b = sp.sympify(b)
    
    # 1-point Gaussian Quadrature (same as the midpoint rule)
    W = 1
    X = 1 / 2
    sum = W * fn(a + X * (b - a))  # Evaluate the function at the midpoint
    result = (b - a) * sp.N(sum)  # Multiply by the width and evaluate numerically
    
    return approximation(result)

def gaussian_quadrature_2_weighting_factor(a, b, expr):
    x = sp.symbols('x')
    fn = sp.lambdify(x, expr, "sympy")
    a = sp.sympify(a)
    b = sp.sympify(b)
    
    # 2-point Gaussian Quadrature
    W = [1/2, 1/2]
    X = [1/2 + sp.sqrt(3) / 6, 1/2 - sp.sqrt(3) / 6]
    sum = 0
    for i in range(2):
        sum += W[i] * fn(a + X[i] * (b - a))  # Evaluate the function at the 2 quadrature points
    result = (b - a) * sp.N(sum)  # Multiply by the width and evaluate numerically
    
    return approximation(result)

def gaussian_quadrature_3_weighting_factor(a, b, expr):
    x = sp.symbols('x')
    fn = sp.lambdify(x, expr, "sympy")
    a = sp.sympify(a)
    b = sp.sympify(b)
    
    # 3-point Gaussian Quadrature
    W = [5/18, 5/18, 8/18]
    X = [1/2 + sp.sqrt(15) / 10, 1/2 - sp.sqrt(15) / 10, 1/2]
    sum = 0
    for i in range(3):
        sum += W[i] * fn(a + X[i] * (b - a))  # Evaluate the function at the 3 quadrature points
    result = (b - a) * sp.N(sum)  # Multiply by the width and evaluate numerically
    
    return approximation(result)
