import sympy as sp
import math
from fractions import Fraction

def get_result_with_extras(value):
    result = float(sp.N(value, 10))
    result_rounded = round(result, 5)

    # Fractional approximation
    frac_approx = Fraction(result).limit_denominator(1000)

    # Check for known irrational approximations
    irrationals = {
        "π": float(sp.pi),
        "e": float(sp.E),
        "√2": float(sp.sqrt(2)),
        "√3": float(sp.sqrt(3)),
        "ln(2)": float(sp.ln(2)),
        "ln(10)": float(sp.ln(10))
    }

    closest_name = min(irrationals, key=lambda k: abs(irrationals[k] - result))
    diff = abs(irrationals[closest_name] - result)
    irrational_match = f"{closest_name} ≈ {irrationals[closest_name]:.6f}" if diff < 0.01 else "No close match"

    return {
        "decimal": result_rounded,
        "fraction": str(frac_approx),
        "irrational": irrational_match
    }

def gaussian_quadrature_1_weighting_factor(a, b, expr):
    x = sp.symbols('x')
    fn = sp.lambdify(x, expr, "sympy")
    a = sp.sympify(a)
    b = sp.sympify(b)

    W = 1
    X = 1 / 2
    val = (b - a) * fn(a + X * (b - a))
    return get_result_with_extras(val)

def gaussian_quadrature_2_weighting_factor(a, b, expr):
    x = sp.symbols('x')
    fn = sp.lambdify(x, expr, "sympy")
    a = sp.sympify(a)
    b = sp.sympify(b)

    W = [1/2, 1/2]
    X = [1/2 + math.sqrt(3) / 6, 1/2 - math.sqrt(3) / 6]
    total = sum(W[i] * fn(a + X[i] * (b - a)) for i in range(2))
    val = (b - a) * total
    return get_result_with_extras(val)

def gaussian_quadrature_3_weighting_factor(a, b, expr):
    x = sp.symbols('x')
    fn = sp.lambdify(x, expr, "sympy")
    a = sp.sympify(a)
    b = sp.sympify(b)

    W = [5/18, 5/18, 8/18]
    X = [1/2 + math.sqrt(15) / 10, 1/2 - math.sqrt(15) / 10, 1/2]
    total = sum(W[i] * fn(a + X[i] * (b - a)) for i in range(3))
    val = (b - a) * total
    return get_result_with_extras(val)
