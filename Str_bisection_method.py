import streamlit as st
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
    return (a + b) / 2, iterations

# Streamlit UI
st.title("📌 Root Finder using Bisection Method")

st.markdown("Enter a mathematical expression in **x**, and the interval [a, b].")

func_expr = st.text_input("Function f(x):", value="x**3 + 4*x**2 - 10")
a = st.number_input("Lower bound (a):", value=1.0)
b = st.number_input("Upper bound (b):", value=2.0)

if st.button("Find Root"):
    try:
        root, iterations = bisection_method(func_expr, a, b)
        st.success(f"✅ Root found: {root:.6f} in {iterations} iterations")
    except Exception as e:
        st.error(f"❌ Error: {e}")
