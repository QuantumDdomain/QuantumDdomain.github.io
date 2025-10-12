import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
import io
import base64
from sympy import nsimplify, pi, sqrt, E
from fractions import Fraction

def approximation(result, to_string=False):
    expr = result
    try:
        f = Fraction(str(expr)).limit_denominator()
    except Exception:
        return str(expr) if to_string else expr
    
    approx_pi = nsimplify(expr, [pi], tolerance=1e-6)
    approx_e  = nsimplify(expr, [E],  tolerance=1e-6)

    sqrt_constants = [2, 3, 5, 7, 10]
    approx_sqrts = [(n, nsimplify(expr, [sqrt(n)], tolerance=1e-6)) for n in sqrt_constants]

    num = f.numerator
    denom = f.denominator

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
    n = len(A)
    x = sp.Symbol('x')
    P = 0

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

def main():
    import js  # type: ignore
    x_input = js.document.getElementById("x_values").value
    y_input = js.document.getElementById("y_values").value

    try:
        A = np.array([float(val) for val in x_input.split(",")])
        B = np.array([float(val) for val in y_input.split(",")])
        assert len(A) == len(B)
    except:
        js.alert("Please enter valid comma-separated numeric values of equal length.")
        return

    polynomial = lagrange_interpolation_symbolic(A, B)

    # Evaluate at midpoint
    x_val = (A[0] + A[-1]) / 2
    y_val = polynomial.subs('x', x_val)

    # Plot
    f_numeric = sp.lambdify('x', polynomial, modules=['numpy'])
    x_numeric = np.linspace(A[0], A[-1], 400)
    y_numeric = f_numeric(x_numeric)

    plt.clf()
    plt.plot(x_numeric, y_numeric)
    plt.plot(x_val, y_val, 'ro', label=f'P({x_val:.2f}) = {y_val:.4f}')
    plt.title("Lagrange Interpolation")
    plt.xlabel("x")
    plt.ylabel("P(x)")
    plt.grid(True)
    plt.legend(fontsize=8)

    # Save to buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode("ascii")

    js.document.getElementById("result").innerHTML = f"""
        <p><strong>Interpolated Polynomial (approximate):</strong><br>{polynomial}</p>
        <p><em>LaTeX view:</em><br>\\({sp.latex(polynomial)}\\)</p>
        <img src="data:image/png;base64,{img_base64}" />
    """
