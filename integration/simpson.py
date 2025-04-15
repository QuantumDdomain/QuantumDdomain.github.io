import sympy as sp

def simpsonI_rule(X_0, X_N, N, expr):
    X_0 = sp.sympify(X_0)
    X_N = sp.sympify(X_N)
    # Define the symbolic variable
    x = sp.symbols('x')
    
    # Convert the input expression into a sympy function
    fn = sp.lambdify(x, expr, "sympy")
    
    h = (X_N - X_0) / N
    sum = 0
    for i in range(int(N / 2)):
        x_2i = X_0 + (2 * i) * h
        x_2i_plus_1 = X_0 + (2 * i + 1) * h
        x_2i_plus_2 = X_0 + (2 * i + 2) * h
        sum += h * (fn(x_2i) + 4 * fn(x_2i_plus_1) + fn(x_2i_plus_2)) / 3
    return sp.N(sum)
