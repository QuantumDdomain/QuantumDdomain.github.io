import math
from sympy import sympify, lambdify, symbols

def richardson_extrapolation(expr_str, x, r, h):
    x = sympify(x)
    h = sympify(h)
    r = sympify(r)
    x_sym = symbols('x')
    expr = sympify(expr_str)
    f = lambdify(x_sym, expr, 'math')

    def D_r(fn, x, r, h):
        return (fn(x + r*h) - fn(x - r*h)) / (2*r*h)

    return round((D_r(f, x, r, h) - r**2 * D_r(f, x, 1, h)) / (1 - r**2),5)
