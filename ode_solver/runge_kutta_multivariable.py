import sympy as sp
from sympy import nsimplify, pi, sqrt, E
from fractions import Fraction

# Simplify numeric results into "nice" forms
def approximation(result):
    expr = result
    try:
        f = Fraction(str(expr)).limit_denominator()
    except Exception:
        return expr

    approx_pi = nsimplify(expr, [pi], tolerance=1e-6)
    approx_e  = nsimplify(expr, [E],  tolerance=1e-6)
    sqrt_constants = [2, 3, 5, 7, 10]
    approx_sqrts = [(n, nsimplify(expr, [sqrt(n)], tolerance=1e-6)) for n in sqrt_constants]
    num, denom = f.numerator, f.denominator

    if 'pi' in str(approx_pi) and len(str(approx_pi)) < 9:
        return approx_pi
    if 'E' in str(approx_e) and len(str(approx_e)) < 8:
        return approx_e
    if (num < 100 and denom < 10) or (num < 10 and denom < 100):
        return f
    for _, approx in approx_sqrts:
        if 'sqrt' in str(approx) and len(str(approx)) < 14:
            return approx
    return expr

# General RK4 solver for n variables
def runge_kutta_multivariable(function_strs, x0, y0_list, X, h):
    x = sp.symbols('x')
    y_symbols = sp.symbols('y0:'+str(len(function_strs)))
    funcs = [sp.lambdify((x,)+y_symbols, sp.sympify(s), 'math') for s in function_strs]
    x_i, y_i = x0, list(y0_list)
    steps = int((X - x0) / h)
    n_vars = len(funcs)
    for _ in range(steps):
        k = [[0]*n_vars for _ in range(4)]
        # Stage calculations
        k[0] = [h * funcs[i](x_i, *y_i) for i in range(n_vars)]
        for stage in [1,2]:
            xi = x_i + h*stage/2
            yi = [y_i[j] + k[stage-1][j]/2 for j in range(n_vars)]
            k[stage] = [h * funcs[i](xi, *yi) for i in range(n_vars)]
        xi = x_i + h
        yi = [y_i[j] + k[2][j] for j in range(n_vars)]
        k[3] = [h * funcs[i](xi, *yi) for i in range(n_vars)]
        y_i = [y_i[i] + (k[0][i] + 2*(k[1][i]+k[2][i]) + k[3][i])/6 for i in range(n_vars)]
        x_i += h
    return [approximation(val) for val in y_i]