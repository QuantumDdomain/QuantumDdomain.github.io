import numpy as np
import matplotlib.pyplot as plt

def lagrange_interpolation(x_points, y_points, x):
    n = len(x_points)
    L = np.zeros(n)
    for i in range(n):
        prd = 1 
        for j in range(n):
            if i != j:
                prd *= (x - x_points[j]) / (x_points[i] - x_points[j])
        L[i] = prd
    
    y = sum(y_points[i] * L[i] for i in range(n))
    return y

def run_lagrange(x_str, y_str, xmin, xmax, show_point=None):
    # Convert input strings to arrays
    x_points = np.array([float(val.strip()) for val in x_str.split(',')])
    y_points = np.array([float(val.strip()) for val in y_str.split(',')])
    
    # Generate plot values
    x_vals = np.linspace(xmin, xmax, 500)
    y_vals = [lagrange_interpolation(x_points, y_points, x) for x in x_vals]
    
    # Plotting
    plt.figure(figsize=(6, 4))
    plt.plot(x_vals, y_vals, label="Lagrange Interpolation")
    plt.scatter(x_points, y_points, color='red', label="Given Points")
    
    result_str = ""
    if show_point is not None:
        interp_value = lagrange_interpolation(x_points, y_points, show_point)
        plt.scatter([show_point], [interp_value], color='green', label=f"Interpolated: {interp_value:.4f}")
        result_str = f"Interpolated value at x = {show_point}: y = {interp_value:.4f}"
    
    plt.xlabel("x")
    plt.ylabel("y")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    
    return result_str
