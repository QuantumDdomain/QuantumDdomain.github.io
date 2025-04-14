from sympy import symbols, sympify, lambdify

def runge_kutta_combined(fx, x_0, y_0, X, h, method_order=2):
    x, y = symbols('x y')
    f_expr = sympify(fx)
    f = lambdify((x, y), f_expr, modules=["math"])

    x_i = float(x_0)
    y_i = float(y_0)
    X = float(X)
    h = float(h)

    n = int((X - x_i) / h)

    for _ in range(n):
        if method_order == 2:
            temp = y_i
            k1 = h * f(x_i, temp)
            k2 = h * f(x_i + h, temp + k1)
            y_i = temp + ((k1 + k2) / 2)

        elif method_order == 3:
            k1 = h * f(x_i, y_i)
            k2 = h * f(x_i + h / 2, y_i + k1 / 2)
            k3 = h * f(x_i + h, y_i - k1 + 2 * k2)
            y_i += ((k1 + 4 * k2 + k3) / 6)

        elif method_order == 4:
            k1 = h * f(x_i, y_i)
            k2 = h * f(x_i + h / 2, y_i + k1 / 2)
            k3 = h * f(x_i + h / 2, y_i + k2 / 2)
            k4 = h * f(x_i + h, y_i + k3)
            y_i += ((k1 + 2 * (k2 + k3) + k4) / 6)

        else:
            raise ValueError("Invalid method order. Choose 2, 3, or 4.")

        x_i += h

    return y_i
