import streamlit as st
from sympy import symbols, sympify, diff, lambdify
import math

x = symbols('x')  # Define symbol globally

# Function to parse and differentiate user input
def get_function_and_derivative(expr_str):
    try:
        expr = sympify(expr_str)  # Convert string to sympy expression
        derivative = diff(expr, x)
        f = lambdify(x, expr, modules=["math"])
        f_prime = lambdify(x, derivative, modules=["math"])
        return f, f_prime
    except Exception as e:
        raise ValueError(f"Invalid function: {e}")

# Newton-Raphson Method
def newton_raphson_method(f, f_prime, x0, tol=1e-6, max_iter=100):
    iterations = 0
    while iterations < max_iter:
        fx = f(x0)
        fpx = f_prime(x0)
        if fpx == 0:
            raise ValueError("Derivative is zero. Newton-Raphson method fails.")
        x_new = x0 - fx / fpx
        if abs((x_new - x0) / x_new) < tol:
            return x_new, iterations + 1
        x0 = x_new
        iterations += 1
    raise ValueError("Maximum iterations exceeded without convergence.")

# Streamlit UI
st.title("🧮 Newton-Raphson Method (General Function)")
st.markdown("Enter a function in terms of `x`, and an initial guess.")

expr_input = st.text_input("Function f(x):", value="x**3 + 4*x**2 - 10")
x0 = st.number_input("Initial guess (x₀):", value=1.0)

if st.button("Find Root"):
    try:
        f, f_prime = get_function_and_derivative(expr_input)
        root, iterations = newton_raphson_method(f, f_prime, x0)
        st.success(f"✅ Root found: {root:.6f} in {iterations} iterations")
    except Exception as e:
        st.error(f"❌ Error: {e}")
