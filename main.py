import streamlit as st
from Str_newton_raphson import newton_raphson_method
from Str_bisection_method import bisection_method

st.title("🧮 Numerical Methods App")

st.sidebar.header("Choose a Method")
method = st.sidebar.selectbox("Select a method:", ["Newton-Raphson Method", "Bisection Method"])

if method == "Newton-Raphson Method":
    newton_raphson_method()
elif method == "Bisection Method":
    bisection_method()
