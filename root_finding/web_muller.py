import cmath
from random import Random
import sympy as sp


def muller_method(a, b, f):
    rand = Random()
    z0 = complex(rand.uniform(a, b), rand.uniform(a, b))
    z1 = complex(rand.uniform(a, b), rand.uniform(a, b))
    z2 = complex(rand.uniform(a, b), rand.uniform(a, b))
    tol = 1e-6
    eps = 1e-12
    max_iter = 100
    iter_count = 0

    while True:
        iter_count += 1
        if iter_count > max_iter:
            break

        temp = z2
        h0 = z1 - z0
        h1 = z2 - z1

        if abs(h0) < eps or abs(h1) < eps:
            z2 += complex(1e-4, 1e-4)
            continue

        del0 = (f(z1) - f(z0)) / h0
        del1 = (f(z2) - f(z1)) / h1
        a_coeff = (del1 - del0) / (h1 + h0)
        b_coeff = a_coeff * h1 + del1
        c_coeff = f(z2)

        rad = cmath.sqrt(b_coeff**2 - 4 * a_coeff * c_coeff)
        den = b_coeff + rad if abs(b_coeff + rad) > abs(b_coeff - rad) else b_coeff - rad

        if abs(den) < eps:
            z2 += complex(1e-4, 1e-4)
            continue

        z2 = z2 - (2 * c_coeff) / den
        if abs(z2 - temp) < tol:
            break

        z0, z1 = z1, z2

    return z2

# Wrapper function for handling user input and calling the Muller method
def solve_muller(function_str, a, b):
    x = sp.Symbol('x')
    a = sp.sympify(a)
    b = sp.sympify(b)
    try:
        func_expr = sp.sympify(function_str)
        func = sp.lambdify(x, func_expr, 'numpy')
        result = muller_method(float(a.evalf()), float(b.evalf()), func)
        real_part = 0.0 if abs(result.real) < 1e-4 else result.real
        imag_part = 0.0 if abs(result.imag) < 1e-4 else result.imag
        return f" {real_part:.6f} + {imag_part:.6f}j"
        return f" {result}"
    except Exception as e:
        return f"Error: {str(e)}"