import sympy as sp

def gaussian_quadrature_n_weighting_factor(a, b, expr, n):
    x = sp.symbols('x')

    # Convert the expression to a sympy expression
    fn = sp.sympify(expr)

    # Ensure that a and b are treated as numbers or sympy expressions
    a = sp.sympify(a)
    b = sp.sympify(b)

    # Get Gauss-Legendre nodes and weights for n-point quadrature
    nodes, weights = get_gauss_legendre_nodes_weights(n)

    # Transform nodes and weights to the interval [a, b]
    transformed_nodes = [(a + b) / 2 + (b - a) / 2 * node for node in nodes]
    transformed_weights = [(b - a) / 2 * weight for weight in weights]

    # Apply Gaussian quadrature formula
    total = sum(wi * fn.subs(x, xi) for xi, wi in zip(transformed_nodes, transformed_weights))

    return total.evalf()

def get_gauss_legendre_nodes_weights(n):
    # Use symbolic Legendre polynomial to get nodes and weights
    x = sp.symbols('x')
    poly = sp.legendre(n, x)
    
    # Solve for the roots of the Legendre polynomial
    nodes = sp.solveset(poly, x, domain=sp.Interval(-1, 1))

    weights = []
    for node in nodes:
        # Compute weights
        poly_diff = sp.diff(poly, x)
        weight = 2 / ((1 - node**2) * poly_diff.subs(x, node)**2)
        weights.append(weight)

    # Return nodes and weights as floats
    return [float(node) for node in nodes], [float(weight) for weight in weights]
