import sympy as sp
from fractions import Fraction

def trapezoidal_rule(X_0, X_N, N, expr):
    # Ensure inputs are sympy expressions
    X_0 = sp.sympify(X_0)
    X_N = sp.sympify(X_N)
    expr = sp.sympify(expr)

    x = sp.symbols('x')
    fn = sp.lambdify(x, expr, "sympy")  # Lambdify using sympy for symbolic math support

    h = (X_N - X_0) / N
    total = 0
    for i in range(N):
        x_i = X_0 + i * h
        x_next = x_i + h
        total += (fn(x_i) + fn(x_next)) * h / 2

    result = float(sp.N(total, 10))  # More precision before rounding
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
    irrational_match = None
    if diff < 0.01:
        irrational_match = f"{closest_name} ≈ {irrationals[closest_name]:.6f}"

    return {
        "decimal": result_rounded,
        "fraction": str(frac_approx),
        "irrational": irrational_match if irrational_match else "No close match"
    }
