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

def fixed_point_method(equation_str, x0_str, tol=1e-6, max_iter=1000):
    try:
        x = sp.symbols('x')
        if "=" in equation_str:
            lhs, rhs = equation_str.split("=")
            rhs = rhs.strip()
        else:
            return "❌ Please enter the equation in the form: x = f(x)"

        g = sp.sympify(rhs)
        g_func = sp.lambdify(x, g, "math")
        x0 = float(sp.sympify(x0_str))
    except Exception as e:
        return f"❌ Invalid input: {e}"

    try:
        iter_count = 0
        while iter_count < max_iter:
            x1 = g_func(x0)
            if abs(x1 - x0) < tol:
                simplified = approximation(x1)
    
                # Fallback: if the simplification is long (not mobile-friendly), return decimal
                if len(str(simplified)) > 20:
                    return x1.evalf(5)
                return f"{simplified} found in {iter_count + 1} iterations."
            x0 = x1
            iter_count += 1

        return f"⚠️ Maximum iterations ({max_iter}) reached. Last estimate: {x1}"
    except Exception as e:
        return f"❌ Error during computation: {e}"
