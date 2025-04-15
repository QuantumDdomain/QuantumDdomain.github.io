import sympy as sp

def trapezoidal_rule(X_0, X_N, N, expr):
    X_0 = sp.sympify(X_0)
    X_N = sp.sympify(X_N)
    # Define the symbolic variable
    x = sp.symbols('x')
    
    # Convert the input expression into a sympy function
    fn = sp.lambdify(x, expr, "math")
    
    h = (X_N - X_0) / N
    sum = 0
    for i in range(N):
        x_i = X_0 + i * h
        x_next = X_0 + (i + 1) * h
        sum += (fn(x_i) + fn(x_next)) * h / 2
    return sum
