import streamlit as st
from str_bisection_method import bisection_method
from str_newton_raphson import newton_raphson_method

st.sidebar.title("Numerical Methods")
option = st.sidebar.selectbox("Select a method", ["Bisection Method", "Newton-Raphson Method"])

if option == "Bisection Method":
    bisection_method()
elif option == "Newton-Raphson Method":
    newton_raphson_method()
