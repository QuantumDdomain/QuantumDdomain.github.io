import sympy as sp

def evaluate_function(expr_str, x_val):
    x = sp.symbols('x')
    expr = sp.sympify(expr_str)
    return float(expr.subs(x, x_val))

def bisection_method(expr_str, a, b, tol=1e-6):
    iterations = 0
    while abs((b - a) / b) > tol:
        c = (a + b) / 2
        f_c = evaluate_function(expr_str, c)
        if f_c == 0:
            break
        elif evaluate_function(expr_str, a) * f_c < 0:
            b = c
        else:
            a = c
        iterations += 1
        if iterations > 1000:
            raise ValueError("The method did not converge in 1000 iterations.")
    return (a + b) / 2, iterations
