from sympy import nsimplify, pi, sqrt, E, sin, N, I, sympify, Expr
from fractions import Fraction
import numbers

def approximation(result):
    try:
        if isinstance(result, complex):
            real_part = approximation(result.real)
            imag_part = approximation(result.imag)
            if abs(result.imag) < 1e-12:
                return real_part
            return f"{real_part} + ({imag_part}j)"

        expr = float(result)

        f = Fraction(str(expr)).limit_denominator()

        approx_pi = nsimplify(expr, [pi], tolerance=1e-6)
        approx_e = nsimplify(expr, [E], tolerance=1e-6)

        sqrt_constants = [2, 3, 5, 7, 10]
        approx_sqrts = [(n, nsimplify(expr, [sqrt(n)], tolerance=1e-6)) for n in sqrt_constants]

        num = f.numerator
        denom = f.denominator

        if 'pi' in str(approx_pi) and len(str(approx_pi)) < 9:
            return approx_pi

        if 'E' in str(approx_e) and len(str(approx_e)) < 8:
            return approx_e

        if ((num < 100 and denom < 10) or (num < 10 and denom < 100)):
            return f

        for n, approx in approx_sqrts:
            approx_str = str(approx)
            if 'sqrt' in approx_str and len(approx_str) < 14:
                return approx

        return expr
    except Exception as e:
        return result  # Fallback for weird inputs

def to_numeric(value):
    try:
        # 1. Already a number? Handle complex numbers directly
        if isinstance(value, (int, float, complex)):
            return complex(value)
        
        # 2. Handle symbolic expressions like 'pi', 'E', 'sin(x)'
        value_str = str(value).replace("i", "I")  # Replace lowercase 'i' with 'I' for SymPy compatibility
        sym_expr = sympify(value_str)  # sympify to handle pi, sin, etc.

        # Evaluate the symbolic expression to a numeric value
        numeric_value = sym_expr.evalf()
        if numeric_value.is_real:
            return float(numeric_value)
        
        real_part, imag_part = numeric_value.as_real_imag()
        return complex(float(real_part), float(imag_part))

    except Exception as e:
        raise ValueError(f"❌ Error parsing '{value}': {e}")

def secant_method(f, x0, x1, max_iter=100, tol=1e-6):
    x0 = to_numeric(x0)
    x1 = to_numeric(x1)

    for i in range(max_iter):
        f0 = f(x0)
        f1 = f(x1)

        if f0 is None or f1 is None:
            raise ValueError(f"Math error during iteration {i}: Function evaluation returned None.")
        if abs(f1 - f0) < tol:
            raise ValueError(f"Math error during iteration {i}: Function values at guesses are equal.")

        x2 = x1 - f1 * (x1 - x0) / (f1 - f0)

        if abs(x2 - x1) < tol:
            return approximation(x2), i + 1

        x0, x1 = x1, x2

    raise ValueError("Secant method did not converge within the maximum number of iterations.")