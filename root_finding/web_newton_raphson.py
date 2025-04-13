import math

def evaluate_function(expr, x):
    allowed_names = {
        k: v for k, v in math.__dict__.items() if not k.startswith("__")
    }
    allowed_names["x"] = x
    return eval(expr, {"__builtins__": {}}, allowed_names)

def newton_raphson_method(expr, x0, tol=1e-6, max_iter=1000):
    iterations = 0
    while iterations < max_iter:
        f_x0 = evaluate_function(expr, x0)
        f_prime_x0 = (evaluate_function(expr, x0 + tol) - f_x0) / tol  # Numerical derivative
        x1 = x0 - f_x0 / f_prime_x0
        if abs(x1 - x0) < tol:
            return x1, iterations
        x0 = x1
        iterations += 1
    raise ValueError("Method did not converge.")
