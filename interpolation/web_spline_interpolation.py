import numpy as np

def compute_second_derivatives(A, B):
    n = len(A) - 1
    M = np.zeros(len(A))
    M[0] = 0
    M[n] = 0

    C = np.zeros((n + 1, n + 1))
    D = np.zeros(n - 1)

    for i in range(n + 1):
        if i == 0 or i == n:
            C[i, i] = 1
        else:
            h_i = A[i] - A[i - 1]
            h_ip1 = A[i + 1] - A[i]
            C[i, i - 1] = h_i / 6
            C[i, i] = (h_i + h_ip1) / 3
            C[i, i + 1] = h_ip1 / 6
            D[i - 1] = ((B[i + 1] - B[i]) / h_ip1) - ((B[i] - B[i - 1]) / h_i)

    M[1:n] = np.linalg.solve(C[1:n, 1:n], D)
    return M

def get_piecewise_spline_functions(A, B):
    A = np.array(A)
    B = np.array(B)
    M = compute_second_derivatives(A, B)
    piecewise_functions = []

    for i in range(len(A) - 1):
        h = A[i + 1] - A[i]
        a_i = B[i]
        b_i = (B[i + 1] - B[i]) / h - (2 * M[i] + M[i + 1]) * h / 6
        c_i = M[i] / 2
        d_i = (M[i + 1] - M[i]) / (6 * h)

        piecewise_functions.append({
            "interval": (A[i], A[i + 1]),
            "a": a_i,
            "b": b_i,
            "c": c_i,
            "d": d_i
        })

    return piecewise_functions
