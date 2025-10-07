import cmath
from random import Random
import sympy as sp
import numpy as np

def secant_method(a, b, f):
    """
    Implements the Secant Method for a complex function f(z).
    Initial guesses z0 and z1 are generated randomly within the bounds [a, b] 
    in both real and imaginary parts.
    """
    rand = Random()
    # Secant Method requires two initial guesses, z0 and z1
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
        
        # Check for near-zero denominator (Secant fails)
        denominator = fz1 - fz0
        if abs(denominator) < eps:
            # Perturb z1 slightly to escape the zero-denominator condition
            z1 += complex(1e-4, 1e-4)
            continue
        
        # Secant Method Formula: z_{i+1} = z_i - f(z_i) * (z_i - z_{i-1}) / (f(z_i) - f(z_{i-1}))
        z_new = z1 - fz1 * (z1 - z0) / denominator
        
        # Check convergence using absolute difference
        if abs(z_new - z1) < tol:
            if abs(f(z_new)) < tol: # Check if the function value is also small
                 return z_new
            
        # Update for the next iteration: z_{i-1} -> z_i, z_i -> z_{i+1}
        z0 = z1
        z1 = z_new

    # Return the last calculated point if max iterations reached
    return z1 if abs(f(z1)) < tol else None


def is_new_root(root, found_roots, tol=1e-5):
    """Checks if the found root is distinct from previously found roots."""
    return all(abs(root - r) > tol for r in found_roots)

def format_root(root, precision=4):
    """Formats a complex root into a readable string."""
    a = round(root.real, precision)
    b = round(root.imag, precision)

    if abs(b) < 1e-12:  # If the imaginary part is near zero
        return a
    elif b >= 0:  # If the imaginary part is positive
        return f"{a}+{b}j"
    else:  # If the imaginary part is negative
        return f"{a}{b}j"

# Wrapper function for handling user input and calling the Secant method
def solve_secant(function_str, a, b):
    x = sp.Symbol('x')
    
    # Sympy is used here to safely evaluate the input bounds and function string
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
            # We use the Secant method
            root = secant_method(a_float, b_float, func) 
            if root is not None and np.isfinite(root):
                if is_new_root(root, found_roots):
                    found_roots.append(root)
            attempts += 1
        except Exception as e:
            # Catching errors during the numerical method itself
            # print(f"Secant attempt failed: {e}") # for debugging
            attempts += 1

    if not found_roots:
        return ["No root found within the given bounds and attempts."]

    # Return roots as a list of formatted results
    return [format_root(r) for r in found_roots]