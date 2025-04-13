import streamlit as st
from Str_newton_raphson import run_newton_raphson_app
from Str_bisection_method import run_bisection_app

st.title("🧮 Numerical Methods App")

st.sidebar.header("Choose a Method")
method = st.sidebar.selectbox("Select a method:", ["Newton-Raphson Method", "Bisection Method"])

if method == "Newton-Raphson Method":
    run_newton_raphson_app()
elif method == "Bisection Method":
    run_bisection_app()
