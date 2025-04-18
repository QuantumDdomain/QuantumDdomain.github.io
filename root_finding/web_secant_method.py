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

def secant_method(expr_str, x0_str, x1_str, tol=1e-6, max_iter=100):
    x = sp.symbols('x')
    try:
        expr = sp.sympify(expr_str)
        x0 = float(sp.sympify(x0_str))
        x1 = float(sp.sympify(x1_str))
    except Exception as e:
        return None, f"❌ Invalid input: {e}"

    if x0 == x1:
        return None, "❌ Initial guesses x0 and x1 must be different."

    fx0 = evaluate_function(expr_str, x0)
    fx1 = evaluate_function(expr_str, x1)

    iterations = 0
    try:
        while iterations < max_iter:
            denominator = fx1 - fx0
            if abs(denominator) < 1e-12:
                return None, "❌ Division by zero error in denominator."

            x_temp = x1 - fx1 * (x1 - x0) / denominator
            if abs((x_temp - x1) / x_temp) < tol:
                simplified = approximation(x_temp)   
                # Fallback: if the simplification is long (not mobile-friendly), return decimal
                if len(str(simplified)) > 20:
                    return x_temp.evalf(5)               
                return simplified, iterations + 1

            x0, fx0 = x1, fx1
            x1, fx1 = x_temp, evaluate_function(expr_str, x_temp)
            iterations += 1
            simplified = approximation(x1)
    
            # Fallback: if the simplification is long (not mobile-friendly), return decimal
            if len(str(simplified)) > 20:
                return x1.evalf(5)

        return simplified, f"⚠️ Maximum iterations reached. Last estimate after {iterations} iterations."

    except Exception as e:
        return None, f"❌ Error during calculation: {e}"
