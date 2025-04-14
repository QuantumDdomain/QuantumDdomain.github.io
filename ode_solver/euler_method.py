from sympy import symbols, lambdify, sympify

def euler_method(fx, x_0, y_0, X, h):
    # Define symbols
    x, y = symbols('x y')

    # Parse the input function (fx is a string)
    f_expr = sympify(fx)  # Convert string to sympy expression

    # Convert the sympy expression to a lambda function for faster evaluation
    f = lambdify((x, y), f_expr, modules=["math"])

    # Ensure the inputs are treated as floats
    x_i = float(x_0)
    y_i = float(y_0)
    h = float(h)
    X = float(X)

    # Calculate the number of iterations
    n = int((X - x_i) / h)
    
    # Apply the Euler method to calculate y at each step
    for _ in range(n):
        y_i += h * f(x_i, y_i)
        x_i += h

    # Return the final value of y
    return y_i
