from sympy import symbols, lambdify, sympify

def euler_method(fx, x_0, y_0, X, h):
    x, y = symbols('x y')
    f_expr = sympify(fx)
    f = lambdify((x, y), f_expr, modules=["math"])

    x_i = float(x_0)
    y_i = float(y_0)
    h = float(h)
    X = float(X)

    n = int((X - x_i) / h)
    for _ in range(n):
        y_i += h * f(x_i, y_i)
        x_i += h

    return y_i
