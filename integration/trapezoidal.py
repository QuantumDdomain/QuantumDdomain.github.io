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

def trapezoidal_rule(X_0, X_N, N, expr):
    # Ensure inputs are sympy expressions
    X_0 = sp.sympify(X_0)
    X_N = sp.sympify(X_N)
    expr = sp.sympify(expr)
    
    x = sp.symbols('x')
    fn = sp.lambdify(x, expr, "sympy")  # Using sympy ensures pi, sqrt, etc. are valid

    h = (X_N - X_0) / N
    total = 0
    for i in range(N):
        x_i = X_0 + i * h
        x_next = x_i + h
        total += (fn(x_i) + fn(x_next)) * h / 2
    result = sp.N(total)  # Convert to float at the end
    
    # Return the symbolic output or numeric approximation
    simplified = approximation(result)
    
    # Fallback: if the simplification is long (not mobile-friendly), return decimal
    if len(str(simplified)) > 20:
        return result.evalf(5)
    
    return simplified
