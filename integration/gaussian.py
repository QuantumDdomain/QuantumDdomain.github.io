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

def gaussian_quadrature_1_weighting_factor(a, b, expr):
    x = sp.symbols('x')
    fn = sp.lambdify(x, expr, "sympy")
    a = sp.sympify(a)
    b = sp.sympify(b)
    
    W = 1
    X = 1 / 2
    sum = W * fn(a + X * (b - a))
    result = (b - a) * sp.N(sum)
    
    return try_symbolic_output(result)

def gaussian_quadrature_2_weighting_factor(a, b, expr):
    x = sp.symbols('x')
    fn = sp.lambdify(x, expr, "sympy")
    a = sp.sympify(a)
    b = sp.sympify(b)
    
    W = [1/2, 1/2]
    X = [1/2 + sp.sqrt(3) / 6, 1/2 - sp.sqrt(3) / 6]
    sum = 0
    for i in range(2):
        sum += W[i] * fn(a + X[i] * (b - a))
    result = (b - a) * sp.N(sum)
    
    return try_symbolic_output(result)

def gaussian_quadrature_3_weighting_factor(a, b, expr):
    x = sp.symbols('x')
    fn = sp.lambdify(x, expr, "sympy")
    a = sp.sympify(a)
    b = sp.sympify(b)
    
    W = [5/18, 5/18, 8/18]
    X = [1/2 + sp.sqrt(15) / 10, 1/2 - sp.sqrt(15) / 10, 1/2]
    sum = 0
    for i in range(3):
        sum += W[i] * fn(a + X[i] * (b - a))
    result = (b - a) * sp.N(sum)
    
    return try_symbolic_output(result)

