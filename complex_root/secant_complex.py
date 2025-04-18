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


def secant_method(f, x0, x1, max_iter=100, tol=1e-6):

    for i in range(max_iter):
        f0 = f(x0)
        f1 = f(x1)

        # Check if function values at the guesses are equal
        if f0 is None or f1 is None:
            raise ValueError(f"Math error during iteration {i}: Function evaluation returned None.")
        if abs(f1 - f0) < tol:
            raise ValueError(f"Math error during iteration {i}: Function values at guesses are equal.")

        # Calculate the new approximation
        x2 = x1 - f1 * (x1 - x0) / (f1 - f0)

        # Check for convergence
        if abs(x2 - x1) < tol:
            x2_real = approximation(x2.real)
            x2_imag = approximation(x2.imag)
            x2_real_str = str(x2_real)
            x2_imag_str = str(x2_imag)
            x2_str =  x2_real_str +" "+"+"+" "+"("+ x2_imag_str + "j"+")"

            return x2_str, i + 1

        # Update guesses for the next iteration
        x0, x1 = x1, x2

    raise ValueError("Secant method did not converge within the maximum number of iterations.")