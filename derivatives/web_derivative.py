import math

def point_3_dy(fn, x1, h1):  
    return (fn(x1 + h1) - fn(x1 - h1)) / (2 * h1)

def point_5_dy(fn, x1, h1):  
    return (-fn(x1 + 2*h1) + 8*fn(x1 + h1) - 8*fn(x1 - h1) + fn(x1 - 2*h1)) / (12 * h1)    

def d2y(fn, x2, h2):  
    return (fn(x2 + h2) - 2*fn(x2) + fn(x2 - h2)) / (h2 ** 2)

def calculate_derivatives(expr, x_str, h_str, method, do_second):
    x = float(x_str)
    h = float(h_str)

    # Create the function from string
    def fn(x_val):
        return eval(expr, {"x": x_val, "math": math, "sin": math.sin, "cos": math.cos, "tan": math.tan, "exp": math.exp, "log": math.log, "pi": math.pi, "e": math.e})

    results = {}

    if method == "3":
        results["first"] = point_3_dy(fn, x, h)
    elif method == "5":
        results["first"] = point_5_dy(fn, x, h)
    else:
        results["first"] = "Invalid method"

    if do_second:
        results["second"] = d2y(fn, x, h)

    return results
