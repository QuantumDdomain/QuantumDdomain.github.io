import math

def point_3_dy(fn, x1, h1):
    return (fn(x1 + h1) - fn(x1 - h1)) / (2 * h1)

def calculate_first_derivative(expr, x, h):
    def user_func(x):
        return eval(expr, {"__builtins__": None}, {"x": x, "math": math})
    
    return point_3_dy(user_func, x, h)
