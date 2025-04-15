import numpy as np
import sympy as sp

def gauss_jordan_elimination(A, B):
    # Evaluate symbolic input to float using sympy
    A = [[float(sp.sympify(val).evalf()) for val in row] for row in A]
    B = [float(sp.sympify(val).evalf()) for val in B]
    A = np.array(A, dtype=float)
    B = np.array(B, dtype=float)
    n = len(B)
    
    for i in range(n):
        # Partial Pivoting
        max_row = i
        for k in range(i + 1, n):
            if abs(A[k][i]) > abs(A[max_row][i]):
                max_row = k
        if A[max_row][i] == 0:
            raise ValueError("Matrix is singular.")
        A[i], A[max_row] = A[max_row].copy(), A[i].copy()
        B[i], B[max_row] = B[max_row], B[i]

        pivot = A[i][i]
        for j in range(n):
            A[i][j] = A[i][j] / pivot
        B[i] = B[i] / pivot

        for k in range(n):
            if k != i:
                factor = A[k][i]
                for j in range(n):
                    A[k][j] -= factor * A[i][j]
                B[k] -= factor * B[i]

    return B.tolist()
