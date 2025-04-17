from sympy import symbols, lambdify, sympify, nsimplify, pi, sqrt, E
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

def euler_method(fx, x_0, y_0, X, h):
    x_0 = sympify(x_0)  # Ensure x_0 is treated as a sympy expression
    y_0 = sympify(y_0)  # Ensure y_0 is treated as a sympy expression
    h  = sympify(h)    # Ensure h is treated as a sympy expression
    X = sympify(X)  # Ensure X is treated as a sympy expression
    # Define symbols
    x, y = symbols('x y')

    # Parse the input function (fx is a string)
    f_expr = sympify(fx)  # Convert string to sympy expression

    # Convert the sympy expression to a lambda function for faster evaluation
    f = lambdify((x, y), f_expr, modules=["math"])

    # Ensure the inputs are treated as floats
    x_i = float(x_0)
    y_i = float(y_0)
    h = float(h)
    X = float(X)

    # Calculate the number of iterations
    n = int((X - x_i) / h)
    
    # Apply the Euler method to calculate y at each step
    for _ in range(n):
        y_i += h * f(x_i, y_i)
        x_i += h

    # Return the final value of y
    return approximation(y_i)
