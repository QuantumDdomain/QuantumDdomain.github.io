import cmath
from random import Random
import sympy as sp
import numpy as np

# Import the formatting function from your separate file
from symbolic_recognition import numeric_to_symbolic

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
    
    tol = 1e-8  # Increased precision for better accuracy
    eps = 1e-14
    max_iter = 2000  # More iterations for difficult roots
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
            if abs(f(z_new)) < tol * 10:  # Check if the function value is also small
                 return z_new
            
        # Update for the next iteration: z_{i-1} -> z_i, z_i -> z_{i+1}
        z0 = z1
        z1 = z_new

    # Return the last calculated point if max iterations reached
    return z1 if abs(f(z1)) < tol * 10 else None


def is_new_root(root, found_roots, tol=1e-4):
    """Checks if the found root is distinct from previously found roots."""
    return all(abs(root - r) > tol for r in found_roots)


def solve_secant(function_str, a, b, symbolic_output=True):
    """
    Solves for roots using the Secant method with intelligent symbolic recognition.
    
    Args:
        function_str: String representation of the function (e.g., "x**2 - 2")
        a: Lower bound for initial guesses
        b: Upper bound for initial guesses
        symbolic_output: If True, displays roots symbolically (default: True)
    
    Returns:
        List of roots in symbolic form (e.g., ['sqrt(2)', '-sqrt(2)', 'pi'])
    """
    x = sp.Symbol('x')
    
    # Sympy is used here to safely evaluate the input bounds and function string
    try:
        a_float = float(sp.sympify(a).evalf())
        b_float = float(sp.sympify(b).evalf())
        func_expr = sp.sympify(function_str)
        func = sp.lambdify(x, func_expr, 'numpy')
    except Exception as e:
        return [f"Error in function or bounds: {str(e)}"]
    
    max_attempts = 100
    found_roots = [] 
    attempts = 0
    
    while attempts < max_attempts:
        try:
            # Use the Secant method
            root = secant_method(a_float, b_float, func) 
            if root is not None and np.isfinite(root):
                if is_new_root(root, found_roots):
                    found_roots.append(root)
            attempts += 1
        except Exception as e:
            # Continue attempting even if an error occurs
            attempts += 1

    if not found_roots:
        return ["No roots found within the given bounds and attempts."]

    # Sort roots for consistent display (real roots first, then by value)
    found_roots.sort(key=lambda r: (abs(r.imag), r.real))

    # Use intelligent symbolic formatting
    if symbolic_output:
        return [numeric_to_symbolic(r, tolerance=1e-5) for r in found_roots]
    else:
        # Fallback to numeric format
        return [format_root(r) for r in found_roots]


def format_root(root, precision=6):
    """
    Formats a complex root into a readable string (numeric version).
    This is a fallback for when symbolic_output=False.
    """
    a = round(root.real, precision)
    b = round(root.imag, precision)

    if abs(b) < 1e-12:
        return str(a)
    elif b >= 0:
        return f"{a}+{b}j"
    else:
        return f"{a}{b}j"