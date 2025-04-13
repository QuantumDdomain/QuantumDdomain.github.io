import math

def evaluate_function(expr, x):
    allowed_names = {
        k: v for k, v in math.__dict__.items() if not k.startswith("__")
    }
    allowed_names["x"] = x
    return eval(expr, {"__builtins__": {}}, allowed_names)

def newton_raphson_method(func, func_prime, x0, tol=1e-6, max_iter=1000):
    iter_count = 0
    while iter_count < max_iter:
        fx = func(x0)
        fpx = func_prime(x0)
        if abs(fx) < tol:
            return x0, iter_count
        x0 = x0 - fx / fpx
        iter_count += 1
    raise ValueError("Newton-Raphson method did not converge.")

