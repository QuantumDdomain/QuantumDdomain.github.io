import sympy as sp

def calculate_first_derivative(expr, xval, hval):
    # Use sympy to parse the expression and handle it properly
    x = sp.symbols('x')
    func = sp.sympify(expr)
    xval = sp.sympify(xval)
    hval = sp.sympify(hval)

    # 3-Point Formula for first derivative
    derivative = (func.subs(x, xval + hval) - func.subs(x, xval - hval)) / (2 * hval)
    return round(derivative,5)
