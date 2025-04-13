import math

def evaluate_function(expr, x):
    allowed_names = {
        k: v for k, v in math.__dict__.items() if not k.startswith("__")
    }
    allowed_names["x"] = x
    return eval(expr, {"__builtins__": {}}, allowed_names)

def bisection_method(expr, a, b, tol=1e-6):
    iterations = 0
    while abs((b - a) / b) > tol:
        c = (a + b) / 2
        f_c = evaluate_function(expr, c)
        if f_c == 0:
            break
        elif evaluate_function(expr, a) * f_c < 0:
            b = c
        else:
            a = c
        iterations += 1
        if iterations > 1000:
            raise ValueError("The method did not converge in 1000 iterations.")
    return (a + b) / 2, iterations
