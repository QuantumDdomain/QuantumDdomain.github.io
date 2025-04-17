import sympy as sp

def gaussian_quadrature_1_weighting_factor(a, b, expr):
    x = sp.symbols('x')
    fn = sp.lambdify(x, expr, "sympy")
    a = sp.sympify(a)
    b = sp.sympify(b)
    
    # 1-point Gaussian Quadrature (same as the midpoint rule)
    W = 1
    X = 1 / 2
    sum = W * fn(a + X * (b - a))  # Evaluate the function at the midpoint
    result = (b - a) * sp.N(sum)  # Multiply by the width and evaluate numerically
    
    return result

def gaussian_quadrature_2_weighting_factor(a, b, expr):
    x = sp.symbols('x')
    fn = sp.lambdify(x, expr, "sympy")
    a = sp.sympify(a)
    b = sp.sympify(b)
    
    # 2-point Gaussian Quadrature
    W = [1/2, 1/2]
    X = [1/2 + sp.sqrt(3) / 6, 1/2 - sp.sqrt(3) / 6]
    sum = 0
    for i in range(2):
        sum += W[i] * fn(a + X[i] * (b - a))  # Evaluate the function at the 2 quadrature points
    result = (b - a) * sp.N(sum)  # Multiply by the width and evaluate numerically
    
    return result

def gaussian_quadrature_3_weighting_factor(a, b, expr):
    x = sp.symbols('x')
    fn = sp.lambdify(x, expr, "sympy")
    a = sp.sympify(a)
    b = sp.sympify(b)
    
    # 3-point Gaussian Quadrature
    W = [5/18, 5/18, 8/18]
    X = [1/2 + sp.sqrt(15) / 10, 1/2 - sp.sqrt(15) / 10, 1/2]
    sum = 0
    for i in range(3):
        sum += W[i] * fn(a + X[i] * (b - a))  # Evaluate the function at the 3 quadrature points
    result = (b - a) * sp.N(sum)  # Multiply by the width and evaluate numerically
    
    return result
