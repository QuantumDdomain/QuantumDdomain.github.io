import cmath
from random import Random
import sympy as sp
import numpy as np

def muller_method(a, b, f):
    rand = Random()
    z0 = complex(rand.uniform(a, b), rand.uniform(a, b))
    z1 = complex(rand.uniform(a, b), rand.uniform(a, b))
    z2 = complex(rand.uniform(a, b), rand.uniform(a, b))
    tol = 1e-5
    eps = 1e-12
    max_iter = 1000
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
        if abs(f(z2)) < tol:
            break

        z0, z1 = z1, z2

    return z2

def is_new_root(root, found_roots,tol = 1e-5):
    return all(abs(root - r) > tol for r in found_roots)

def format_root(root, precision=4):
    a = round(root.real, precision)
    b = round(root.imag, precision)

    # Return root as a tuple or string without quotes inside the list
    if abs(b) < 1e-12:  # If the imaginary part is near zero, return only the real part
        return a
    elif b >= 0:  # If the imaginary part is positive
        return f"{a}+{b}j"
    else:  # If the imaginary part is negative
        return f"{a}{b}j"

# Wrapper function for handling user input and calling the Muller method
def solve_muller(function_str, a, b):
    x = sp.Symbol('x')
    a = sp.sympify(a)
    b = sp.sympify(b)
    max_attempts = 100
    found_roots = [] 
    attempts = 0
    while attempts < max_attempts:
        try:
            func_expr = sp.sympify(function_str)
            func = sp.lambdify(x, func_expr, 'numpy')
            root = muller_method(float(a.evalf()), float(b.evalf()), func)
            if root is not None and np.isfinite(root):
                if is_new_root(root, found_roots):
                    found_roots.append(root)
            attempts += 1
        except Exception as e:
            return f"Error: {str(e)}"

    # Return roots as a list of formatted results (not as strings)
    return [format_root(r) for r in found_roots]
