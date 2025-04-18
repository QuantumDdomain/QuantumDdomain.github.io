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

def evaluate_function(expr_str, x_val):
    x = sp.symbols('x')
    expr = sp.sympify(expr_str)
    return float(expr.subs(x, x_val))

def bisection_method(expr_str, a, b, tol=1e-6):
    a = sp.sympify(a)
    b = sp.sympify(b)
    iterations = 0
    while abs((b - a) / b) > tol:
        c = (a + b) / 2
        f_c = evaluate_function(expr_str, c)
        if f_c == 0:
            break
        elif evaluate_function(expr_str, a) * f_c < 0:
            b = c
        else:
            a = c
        iterations += 1
        if iterations > 1000:
            raise ValueError("The method did not converge in 1000 iterations.")
        result = (a + b) / 2
        result = float(result)

    simplified = approximation(result)
    
    # Fallback: if the simplification is long (not mobile-friendly), return decimal
    if len(str(simplified)) > 20:
        return result.evalf(5)
    
    return simplified,iterations