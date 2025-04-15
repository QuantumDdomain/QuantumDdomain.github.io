import numpy as np
import matplotlib.pyplot as plt

def compute_second_derivatives(A, B, h):
    n = len(A) - 1
    M = np.zeros(len(A))
    M[0] = 0
    M[n] = 0

    C = np.zeros((n + 1, n + 1))
    for i in range(n + 1):
        if i == 0 or i == n:
            C[i, i] = 1
        else:
            C[i, i - 1] = (A[i] - A[i - 1]) / 6
            C[i, i] = (A[i + 1] - A[i - 1]) / 3
            C[i, i + 1] = (A[i + 1] - A[i]) / 6

    D = np.zeros(n - 1)
    for i in range(1, n):
        D[i - 1] = (B[i + 1] - B[i]) / (A[i + 1] - A[i]) - (B[i] - B[i - 1]) / (A[i] - A[i - 1])
    
    M[1:n] = np.linalg.solve(C[1:n, 1:n], D)
    return M

def get_piecewise_spline_functions(A, B):
    h = A[1] - A[0]
    M = compute_second_derivatives(A, B, h)
    piecewise_functions = []

    for i in range(len(A) - 1):
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

def run_spline(user_input_x, user_input_y):
    A = np.array([float(x) for x in user_input_x.split(',')])
    B = np.array([float(y) for y in user_input_y.split(',')])

    piecewise_splines = get_piecewise_spline_functions(A, B)

    plt.figure(figsize=(10, 6))

    for spline in piecewise_splines:
        x0, x1 = spline["interval"]
        a, b, c, d = spline["a"], spline["b"], spline["c"], spline["d"]
        x_vals = np.linspace(x0, x1, 200)
        y_vals = a + b * (x_vals - x0) + c * (x_vals - x0)**2 + d * (x_vals - x0)**3

        label = f"S(x) on [{x0}, {x1}]: {a:.2f} + {b:.2f}(x-{x0}) + {c:.2f}(x-{x0})² + {d:.2f}(x-{x0})³"
    plt.plot(x_vals, y_vals, label=label)

    plt.plot(A, B, 'ro', label="Data Points")
    plt.title("Natural Cubic Spline Interpolation")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.grid(True)
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.show()
