import sympy as sp

def fixed_point_method(equation_str, x0_str, tol=1e-6):
    try:
        x = sp.symbols('x')
        # Extract the right-hand side of the equation x = f(x)
        if "=" in equation_str:
            lhs, rhs = equation_str.split("=")
            rhs = rhs.strip()
        else:
            return "❌ Please enter the equation in the form: x = f(x)"

        g = sp.sympify(rhs)
        g_func = sp.lambdify(x, g, "math")
        x0 = float(sp.sympify(x0_str))
    except Exception as e:
        return f"❌ Invalid input: {e}"

    try:
        while True:
            iter_count = 0
            x1 = g_func(x0)
            if abs(x1 - x0) < tol:
                return f"{x1:.6f} found in {iter_count + 1} iterations."
            x0 = x1
            iter_count += 1

        return f"⚠️ Maximum iterations reached. Last estimate: {x1:.6f}"
    except Exception as e:
        return f"❌ Error during computation: {e}"
