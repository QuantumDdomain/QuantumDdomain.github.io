import sympy as sp

def calculate_first_derivative(expr, xval, hval):
    xval = sp.sympify(xval)
    hval = sp.sympify(hval)
    # Define symbol
    x = sp.symbols('x')
    
    # Convert user string to symbolic expression
    func = sp.sympify(expr)
    
    # Apply 5-point central difference formula for first derivative:
    # f'(x) ≈ [f(x-2h) - 8f(x-h) + 8f(x+h) - f(x+2h)] / (12h)
    derivative = (-func.subs(x, xval + 2*hval) + 8*func.subs(x, xval + hval) -
                  8*func.subs(x, xval - hval) + func.subs(x, xval - 2*hval)) / (12*hval)

    return derivative
