# web_lagrange_interpolation.py

import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
import io
import base64

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

    return sp.simplify(P)

def main():
    import js # type: ignore
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
    plt.plot(x_numeric, y_numeric, label=f'P(x): {sp.latex(polynomial)}')
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
        <p><strong>Interpolated Polynomial:</strong><br>{sp.latex(polynomial)}</p>
        <img src="data:image/png;base64,{img_base64}" />
    """
