import sympy as sp

def try_symbolic_output(value, tol=1e-4):
    # Convert the float value to a sympy expression
    value_expr = sp.sympify(value)
    
    # Simplify the expression to its most symbolic form
    simplified_expr = sp.simplify(value_expr)
    
    # Attempt to approximate to a fraction (in terms of pi or other constants)
    if abs(float(simplified_expr) - float(value_expr)) < tol:
        return str(simplified_expr)
    
    # Handle cases where pi or sqrt(x) might be involved
    pi_multiple = sp.pi * sp.Rational(value_expr).limit_denominator()
    sqrt_multiple = sp.sqrt(value_expr).limit_denominator()

    # Check if the result is close to any known symbolic constants
    if abs(value_expr - pi_multiple) < tol:
        return f'{pi_multiple}'
    elif abs(value_expr - sqrt_multiple) < tol:
        return f'{sqrt_multiple}'
    
    # Return the simplified symbolic form, if no close match is found
    return str(simplified_expr)

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
    
    return try_symbolic_output(result)

