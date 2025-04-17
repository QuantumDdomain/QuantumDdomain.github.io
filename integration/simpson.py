import sympy as sp
from fractions import Fraction

def simpsonI_rule(X_0, X_N, N, expr):
    X_0 = sp.sympify(X_0)
    X_N = sp.sympify(X_N)
    x = sp.symbols('x')
    fn = sp.lambdify(x, expr, "sympy")
    
    h = (X_N - X_0) / N
    total = 0
    for i in range(int(N / 2)):
        x_2i = X_0 + (2 * i) * h
        x_2i_plus_1 = X_0 + (2 * i + 1) * h
        x_2i_plus_2 = X_0 + (2 * i + 2) * h
        total += h * (fn(x_2i) + 4 * fn(x_2i_plus_1) + fn(x_2i_plus_2)) / 3

    result = float(sp.N(total, 10))  # More precise
    result_rounded = round(result, 5)

    # Fractional approximation
    frac_approx = Fraction(result).limit_denominator(1000)

    # Check for known irrational matches
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
