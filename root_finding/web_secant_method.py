import sympy as sp

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
                return round(x_temp, 6), iterations + 1

            x0, fx0 = x1, fx1
            x1, fx1 = x_temp, evaluate_function(expr_str, x_temp)
            iterations += 1

        return round(x1, 6), f"⚠️ Maximum iterations reached. Last estimate after {iterations} iterations."

    except Exception as e:
        return None, f"❌ Error during calculation: {e}"
