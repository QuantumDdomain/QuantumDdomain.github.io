import streamlit as st
import math

# Define functions
def fn_1(x):
    return math.exp(2 * x) - math.exp(x) - 2

def fn_2(x):
    return x**3 + 4 * x**2 - 10

# Bisection Method
def bisection_method(fn, a, b, tol=1e-6):
    iterations = 0
    while abs((b - a) / b) > tol:
        c = (a + b) / 2
        if fn(c) == 0:
            break
        elif fn(a) * fn(c) < 0:
            b = c
        else:
            a = c
        iterations += 1
    return (a + b) / 2, iterations

# Streamlit App
def run_bisection():
    st.title("🔍 Root Finding using Bisection Method")

    st.markdown("### Select the function:")
    func_choice = st.selectbox("Choose a function:", ("f(x) = e^(2x) - e^x - 2", "f(x) = x³ + 4x² - 10"))

    a = st.number_input("Enter lower bound (a):", value=0.0)
    b = st.number_input("Enter upper bound (b):", value=1.0)
    tol = st.number_input("Enter tolerance:", value=1e-6, format="%.1e")

    if st.button("Find Root"):
        if func_choice == "f(x) = e^(2x) - e^x - 2":
            fn = fn_1
        else:
            fn = fn_2

        try:
            root, iterations = bisection_method(fn, a, b, tol)
            st.success(f"✅ Root found: {root:.6f} in {iterations} iterations")
        except Exception as e:
            st.error(f"⚠️ Error: {e}")
