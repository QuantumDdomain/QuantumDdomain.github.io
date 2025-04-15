from sympy import symbols, sympify, lambdify

def runge_kutta_combined(fx, x_0, y_0, X, h, method_order=2):
    x_0 = sympify(x_0)  # Ensure x_0 is treated as a sympy expression
    y_0 = sympify(y_0)  # Ensure y_0 is treated as a sympy expression
    h  = sympify(h)    # Ensure h is treated as a sympy expression
    X = sympify(X)  # Ensure X is treated as a sympy expression
    # Define symbols for x and y
    x, y = symbols('x y')

    # Parse the function fx (expecting a string)
    f_expr = sympify(fx)
    
    # Convert the parsed function into a callable function
    f = lambdify((x, y), f_expr, modules=["math"])

    # Convert input values to floats
    x_i = float(x_0)
    y_i = float(y_0)
    X = float(X)
    h = float(h)

    # Calculate the number of iterations based on step size
    n = int((X - x_i) / h)

    # Apply the selected Runge-Kutta method
    for _ in range(n):
        if method_order == 2:
            # Second-order method (Heun's method)
            temp = y_i
            k1 = h * f(x_i, temp)
            k2 = h * f(x_i + h, temp + k1)
            y_i = temp + ((k1 + k2) / 2)

        elif method_order == 3:
            # Third-order method (modified third-order method)
            k1 = h * f(x_i, y_i)
            k2 = h * f(x_i + h / 2, y_i + k1 / 2)
            k3 = h * f(x_i + h, y_i - k1 + 2 * k2)
            y_i += ((k1 + 4 * k2 + k3) / 6)

        elif method_order == 4:
            # Fourth-order method (classic Runge-Kutta)
            k1 = h * f(x_i, y_i)
            k2 = h * f(x_i + h / 2, y_i + k1 / 2)
            k3 = h * f(x_i + h / 2, y_i + k2 / 2)
            k4 = h * f(x_i + h, y_i + k3)
            y_i += ((k1 + 2 * (k2 + k3) + k4) / 6)

        else:
            raise ValueError("Invalid method order. Choose 2, 3, or 4.")

        # Update the value of x
        x_i += h

    # Return the final value of y after all iterations
    return y_i
