import sympy as sp

def simpsonI_rule(X_0, X_N, N, expr):
    # Ensure inputs are sympy expressions
    X_0 = sp.sympify(X_0)
    X_N = sp.sympify(X_N)
    expr = sp.sympify(expr)

    x = sp.symbols('x')
    fn = sp.lambdify(x, expr, "sympy")  # Using sympy ensures pi, sqrt, etc. are valid

    h = (X_N - X_0) / N
    total = fn(X_0) + fn(X_N)
    
    # Odd indices (multiplying by 4)
    for i in range(1, N, 2):
        total += 4 * fn(X_0 + i * h)
    
    # Even indices (multiplying by 2)
    for i in range(2, N - 1, 2):
        total += 2 * fn(X_0 + i * h)

    # Multiply by h/3 as per Simpson's rule
    total *= h / 3
    result = sp.N(total)  # Convert to numeric result at the end
    
    # Attempt to return a symbolic result
    return result
