import math
from sympy import sympify, lambdify, symbols,nsimplify, pi, sqrt, E
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

def richardson_extrapolation(expr_str, x, r, h):
    x = sympify(x)
    h = sympify(h)
    r = sympify(r)
    x_sym = symbols('x')
    expr = sympify(expr_str)
    f = lambdify(x_sym, expr, 'math')

    def D_r(fn, x, r, h):
        return (fn(x + r*h) - fn(x - r*h)) / (2*r*h)
    derivative = (D_r(f, x, r, h) - r**2 * D_r(f, x, 1, h)) / (1 - r**2)

    simplified = approximation(derivative)
    
    # Fallback: if the simplification is long (not mobile-friendly), return decimal
    if len(str(simplified)) > 20:
        return derivative.evalf(5)
    
    return simplified
