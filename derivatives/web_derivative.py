import math

def parse_function(expr):
    def func(x):
        return eval(expr, {"x": x, "math": math, **math.__dict__})
    return func

def derivative_3_point(f, x, h):
    return (f(x + h) - f(x - h)) / (2 * h)

def derivative_5_point(f, x, h):
    return (-f(x + 2*h) + 8*f(x + h) - 8*f(x - h) + f(x - 2*h)) / (12 * h)

def second_derivative(f, x, h):
    return (f(x + h) - 2*f(x) + f(x - h)) / (h ** 2)

def calculate_derivatives(expr, x_val, h_val, method="3", do_second=False):
    f = parse_function(expr)
    x = float(x_val)
    h = float(h_val)

    result = {}

    if method == "3":
        result["first"] = derivative_3_point(f, x, h)
    elif method == "5":
        result["first"] = derivative_5_point(f, x, h)

    if do_second:
        result["second"] = second_derivative(f, x, h)

    return result
