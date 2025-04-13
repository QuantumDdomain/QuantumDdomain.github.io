import math

# Function evaluator
def evaluate_function(expr, x):
    allowed_names = {
        k: v for k, v in math.__dict__.items() if not k.startswith("__")
    }
    allowed_names["x"] = x
    return eval(expr, {"__builtins__": {}}, allowed_names)

# Bisection method
def bisection_method(expr, a, b, tol=1e-6):
    iterations = 0
    while abs((b - a) / b) > tol:
        c = (a + b) / 2
        f_c = evaluate_function(expr, c)
        if f_c == 0:
            break
        elif evaluate_function(expr, a) * f_c < 0:
            b = c
        else:
            a = c
        iterations += 1
        
        if iterations > 1000:
            raise ValueError("The method did not converge in 1000 iterations.")
    
    return (a + b) / 2, iterations

# Main code
if __name__ == "__main__":
    print("Root Finder using Bisection Method\n")

    func_expr = input("Enter function f(x): ")
    a = float(input("Enter lower bound a: "))
    b = float(input("Enter upper bound b: "))

    try:
        root, iterations = bisection_method(func_expr, a, b)
        print(f"\nRoot found: {root:.6f} in {iterations} iterations")
    except Exception as e:
        print(f"\nError: {e}")
