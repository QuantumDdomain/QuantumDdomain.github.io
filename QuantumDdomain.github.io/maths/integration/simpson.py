import sympy as sp

def simpson(X_0, X_N, fn_str, h=0.01):
    x = sp.symbols('x')
    func = sp.sympify(fn_str)
    
    X_0 = sp.sympify(X_0)
    X_N = sp.sympify(X_N)
    h = float(h)

    # Check a few values in the interval for domain validity
    def is_safe(expr, a, b):
        test_points = [a, b, (a + b) / 2]
        for val in test_points:
            try:
                eval_val = expr.subs(x, val).evalf()
                if eval_val.has(sp.zoo, sp.oo, sp.nan) or sp.im(eval_val) != 0:
                    return False
            except:
                return False
        return True

    if not is_safe(func, X_0, X_N):
        return "❌ Error: Function has undefined or complex values in the interval."

    # Ensure even number of intervals
    n = int((X_N - X_0) / h)
    if n % 2 != 0:
        n += 1
    h = (X_N - X_0) / n

    try:
        sum_result = func.subs(x, X_0) + func.subs(x, X_N)
    except Exception as e:
        return f"❌ Error evaluating function at boundaries: {e}"

    xi = X_0 + h
    for i in range(1, n):
        try:
            term = func.subs(x, xi)
            if i % 2 == 0:
                sum_result += 2 * term
            else:
                sum_result += 4 * term
        except Exception as e:
            return f"❌ Error evaluating function at x = {xi}: {e}"
        xi += h

    integral = (h / 3) * sum_result
    return f"{integral.evalf()}"
