import sympy as sp

def evaluate_function(expr_str, x_val):
    x = sp.symbols('x')
    expr = sp.sympify(expr_str)
    return float(expr.subs(x, x_val))

def newton_raphson_method(expr_str, x0, tol=1e-6, max_iter=1000):
    x = sp.symbols('x')
    expr = sp.sympify(expr_str)
    derivative_expr = sp.diff(expr, x)

    iterations = 0
    while iterations < max_iter:
        f_x0 = float(expr.subs(x, x0))
        f_prime_x0 = float(derivative_expr.subs(x, x0))

        if f_prime_x0 == 0:
            raise ZeroDivisionError("Derivative is zero. No solution found.")

        x1 = x0 - f_x0 / f_prime_x0

        if abs(x1 - x0) < tol:
            return x1, iterations

        x0 = x1
        iterations += 1

    raise ValueError("Method did not converge.")
