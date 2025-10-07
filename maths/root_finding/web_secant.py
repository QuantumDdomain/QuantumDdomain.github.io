import cmath
from random import Random
import sympy as sp
import numpy as np

def secant_method(a, b, f):
    """
    Implements the Secant Method for a complex function f(z).
    """
    rand = Random()
    z0 = complex(rand.uniform(a, b), rand.uniform(a, b))
    z1 = complex(rand.uniform(a, b), rand.uniform(a, b))
    
    tol = 1e-5
    eps = 1e-12
    max_iter = 1000
    iter_count = 0

    while True:
        iter_count += 1
        if iter_count > max_iter:
            break

        fz0 = f(z0)
        fz1 = f(z1)
        
        denominator = fz1 - fz0
        if abs(denominator) < eps:
            z1 += complex(1e-4, 1e-4)
            continue
        
        z_new = z1 - fz1 * (z1 - z0) / denominator
        
        if abs(z_new - z1) < tol:
            if abs(f(z_new)) < tol:
                 return z_new
            
        z0 = z1
        z1 = z_new

    return z1 if abs(f(z1)) < tol else None


# --- MODIFIED ROOT FILTERING FUNCTION ---
def is_new_root(root, found_roots, tol=1e-5):
    """
    Checks if the found root is distinct from previously found roots AND
    if it is not the trivial root (z=0).
    """
    # 1. Check if the root is close to the trivial root z=0
    if abs(root) < tol * 10: # Use a slightly larger tolerance for zero check
        return False
        
    # 2. Check if the root is distinct from previously found roots
    return all(abs(root - r) > tol for r in found_roots)

def format_root(root, precision=4):
    """Formats a complex root into a readable string."""
    a = round(root.real, precision)
    b = round(root.imag, precision)

    if abs(b) < 1e-12:
        return a
    elif b >= 0:
        return f"{a}+{b}j"
    else:
        return f"{a}{b}j"

# Wrapper function for handling user input and calling the Secant method
def solve_secant(function_str, a, b):
    x = sp.Symbol('x')
    
    try:
        a_float = float(sp.sympify(a).evalf())
        b_float = float(sp.sympify(b).evalf())
        func_expr = sp.sympify(function_str)
        func = sp.lambdify(x, func_expr, 'numpy')
    except Exception as e:
        return f"Error in function or bounds preparation: {str(e)}"
    
    max_attempts = 100
    found_roots = [] 
    attempts = 0
    
    while attempts < max_attempts:
        try:
            root = secant_method(a_float, b_float, func) 
            if root is not None and np.isfinite(root):
                if is_new_root(root, found_roots):
                    found_roots.append(root)
            attempts += 1
        except Exception as e:
            attempts += 1

    if not found_roots:
        # If no non-zero roots are found, report that.
        return ["No non-zero root found within the given bounds and attempts."]

    return [format_root(r) for r in found_roots]