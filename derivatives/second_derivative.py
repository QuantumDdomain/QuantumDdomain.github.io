import math

def d2y(fn, x2, h2):
    return (fn(x2 + h2) - 2*fn(x2) + fn(x2 - h2)) / (h2 ** 2)

def calculate_second_derivative(expr, x, h):
    def user_func(x):
        return eval(expr, {"__builtins__": None}, {"x": x, "math": math})
    
    return d2y(user_func, x, h)
