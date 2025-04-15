import sympy as sp

def trapezoidal_rule(X_0, X_N, N, expr):
    # Ensure inputs are sympy expressions
    X_0 = sp.sympify(X_0)
    X_N = sp.sympify(X_N)
    expr = sp.sympify(expr)
    
    x = sp.symbols('x')
    fn = sp.lambdify(x, expr, "sympy")  # Using sympy ensures pi, sqrt, etc. are valid

    h = (X_N - X_0) / N
    total = 0
    for i in range(N):
        x_i = X_0 + i * h
        x_next = x_i + h
        total += (fn(x_i) + fn(x_next)) * h / 2
    result = sp.N(total)  # Convert to float at the end
    return round(result,5)

