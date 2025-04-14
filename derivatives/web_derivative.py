import math

def point_3_dy(fn, x1, h1):  
    result = (fn(x1 + h1) - fn(x1 - h1)) / (2 * h1)
    print(f"3-point first derivative: {result}")  # Debugging
    return result

def point_5_dy(fn, x1, h1):  
    result = (-fn(x1 + 2*h1) + 8*fn(x1 + h1) - 8*fn(x1 - h1) + fn(x1 - 2*h1)) / (12 * h1)
    print(f"5-point first derivative: {result}")  # Debugging
    return result

def d2y(fn, x2, h2):  
    result = (fn(x2 + h2) - 2 * fn(x2) + fn(x2 - h2)) / (h2 ** 2)
    print(f"Second derivative: {result}")  # Debugging
    return result

def calculate_derivatives(expr, xval, hval, method="3", second=False):
    import math
    import builtins
    import types

    # Convert inputs from strings
    x = float(xval)
    h = float(hval)

    # Safe evaluation context
    allowed_names = {k: getattr(math, k) for k in dir(math) if not k.startswith("__")}
    allowed_names.update({
        'abs': abs,
        'pow': pow,
    })

    # Define the function from user input
    def user_func(x):
        return eval(expr, {"__builtins__": {}}, {**allowed_names, "x": x})

    result = {}

    if method == "3":
        result["first"] = point_3_dy(user_func, x, h)
    elif method == "5":
        result["first"] = point_5_dy(user_func, x, h)
    else:
        result["first"] = "Invalid method"

    if second:
        result["second"] = d2y(user_func, x, h)

    print(f"Final result: {result}")  # Debugging
    return result
