import numpy as np
import sympy as sp
from sympy import nsimplify, pi, sqrt, E
from fractions import Fraction

def approximation(result, to_string=False):
    """
    Approximates a numerical result to a simplified form using common mathematical constants.
    """
    expr = result
    try:
        f = Fraction(str(expr)).limit_denominator()
    except Exception:
        return str(expr) if to_string else expr
    
    # Try to approximate with pi
    approx_pi = nsimplify(expr, [pi], tolerance=1e-6)
    # Try to approximate with e
    approx_e = nsimplify(expr, [E], tolerance=1e-6)

    # Try to approximate with square roots
    sqrt_constants = [2, 3, 5, 7, 10]
    approx_sqrts = [(n, nsimplify(expr, [sqrt(n)], tolerance=1e-6)) for n in sqrt_constants]

    num = f.numerator
    denom = f.denominator

    # Check which approximation is best
    if 'pi' in str(approx_pi) and len(str(approx_pi)) < 9:
        return str(approx_pi) if to_string else approx_pi
    if 'E' in str(approx_e) and len(str(approx_e)) < 8:
        return str(approx_e) if to_string else approx_e
    if ((num < 100 and denom < 10) or (num < 10 and denom < 100)):
        return str(f) if to_string else f
    for n, approx in approx_sqrts:
        approx_str = str(approx)
        if 'sqrt' in approx_str and len(approx_str) < 14:
            return approx_str if to_string else approx

    return str(expr) if to_string else expr


def lagrange_interpolation_symbolic(A, B):
    """
    Performs Lagrange interpolation on the given data points.
    
    Parameters:
    -----------
    A : array-like
        X coordinates of data points
    B : array-like
        Y coordinates of data points
    
    Returns:
    --------
    sympy expression
        The interpolating polynomial in symbolic form
    """
    n = len(A)
    x = sp.Symbol('x')
    P = 0

    # Build the Lagrange polynomial
    for i in range(n):
        term = 1
        for j in range(n):
            if i != j:
                term *= (x - A[j]) / (A[i] - A[j])
        P += B[i] * term
    
    # Simplify the polynomial and approximate each coefficient
    simplified_poly = sp.simplify(P)
    polynomial = 0
    
    for term in simplified_poly.as_ordered_terms():
        coeff, monomial = term.as_coeff_Mul()
        approx_coeff = approximation(coeff)
        polynomial += approx_coeff * monomial

    return sp.simplify(polynomial)


def evaluate_polynomial(poly_str, x_val):
    """
    Evaluates a polynomial (given as a string) at a specific x value.
    
    Parameters:
    -----------
    poly_str : str
        String representation of the polynomial
    x_val : float
        The x value at which to evaluate the polynomial
    
    Returns:
    --------
    float
        The value of P(x_val)
    """
    x = sp.Symbol('x')
    poly = sp.sympify(poly_str)
    return float(poly.subs(x, x_val))


def get_polynomial_latex(poly):
    """
    Converts a sympy polynomial to LaTeX format for display.
    
    Parameters:
    -----------
    poly : sympy expression
        The polynomial to convert
    
    Returns:
    --------
    str
        LaTeX representation of the polynomial
    """
    return sp.latex(poly)