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
    x_val = sp.sympify(x_val)
    return sp.N(expr.subs(x, x_val))  # Keeps complex parts

def newton_raphson_method(expr_str, x0, tol=1e-6, max_iter=1000):
    x = sp.symbols('x')
    expr = sp.sympify(expr_str)
    derivative_expr = sp.diff(expr, x)

    # ✅ Convert x0 to symbolic (if it's passed as a string like "1 + I")
    x0 = sp.sympify(x0)

    iterations = 0
    while iterations < max_iter:
        f_x0 = sp.N(expr.subs(x, x0))
        f_prime_x0 = sp.N(derivative_expr.subs(x, x0))

        if f_prime_x0 == 0:
            raise ZeroDivisionError("Derivative is zero. No solution found.")

        x1 = x0 - f_x0 / f_prime_x0

        if abs(x1 - x0) < tol:
            simplified = approximation(x1)
    
            # Fallback: if the simplification is long (not mobile-friendly), return decimal
            if len(str(simplified)) > 20:
                return x1.evalf(5)
            return simplified, iterations

        x0 = x1
        iterations += 1

    raise ValueError("Method did not converge.")