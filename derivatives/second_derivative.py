import sympy as sp

def calculate_second_derivative(expr, xval, hval):
    # Use sympy to parse the expression
    x = sp.symbols('x')
    func = sp.sympify(expr)

    # 5-Point Formula for second derivative
    second_derivative = (func.subs(x, xval + hval) - 2*func.subs(x, xval) + func.subs(x, xval - hval)) / (hval**2)
    return second_derivative
