import numpy as np
import matplotlib.pyplot as plt

def compute_second_derivatives(A, B):
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
    piecewise_functions = []
    M = compute_second_derivatives(A, B)
    for i in range(len(A) - 1):
        xi_1 = A[i]
        xi = A[i + 1]
        hi = xi - xi_1

        fi_1 = B[i]
        fi = B[i + 1]
        Mi_1 = M[i]
        Mi = M[i + 1]

        a = (Mi - Mi_1) / (6 * hi)
        b = Mi_1 / 2
        c = (fi - fi_1) / hi - (2 * hi * Mi_1 + hi * Mi) / 6
        d = fi_1

        piecewise_functions.append({
            "interval": (xi_1, xi),
            "a": a,
            "b": b,
            "c": c,
            "d": d,
            "shift": xi_1
        })

    return piecewise_functions

def run_spline(x_str, y_str):
    x_points = np.array([float(val.strip()) for val in x_str.split(',')])
    y_points = np.array([float(val.strip()) for val in y_str.split(',')])

    splines = get_piecewise_spline_functions(x_points, y_points)

    x_vals = np.linspace(x_points[0], x_points[-1], 500)
    y_vals = np.zeros_like(x_vals)

    plt.figure(figsize=(8, 6))
    for spline in splines:
        xi_1, xi = spline["interval"]
        a, b, c, d = spline["a"], spline["b"], spline["c"], spline["d"]
        shift = spline["shift"]

        # Evaluate spline function over the interval
        for j, x in enumerate(x_vals):
            if xi_1 <= x <= xi:
                y_vals[j] = a * (x - shift) ** 3 + b * (x - shift) ** 2 + c * (x - shift) + d

        plt.plot(x_vals, y_vals, label=f"Spline: {xi_1}-{xi}")

    plt.scatter(x_points, y_points, color='red', label="Data Points", zorder=5)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
