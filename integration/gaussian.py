import sympy as sp
import math

def gaussian_quadrature_1_weighting_factor(a, b, expr):
    x = sp.symbols('x')
    fn = sp.lambdify(x, expr, "math")
    
    W = 1
    X = 1 / 2
    sum = W * fn(a + X * (b - a))
    return (b - a) * sum

def gaussian_quadrature_2_weighting_factor(a, b, expr):
    x = sp.symbols('x')
    fn = sp.lambdify(x, expr, "math")
    
    W = [1/2, 1/2]
    X = [1/2 + math.sqrt(3) / 6, 1/2 - math.sqrt(3) / 6]
    sum = 0
    for i in range(2):
        sum += W[i] * fn(a + X[i] * (b - a))
    return (b - a) * sum

def gaussian_quadrature_3_weighting_factor(a, b, expr):
    x = sp.symbols('x')
    fn = sp.lambdify(x, expr, "math")
    
    W = [5/18, 5/18, 8/18]
    X = [1/2 + math.sqrt(15) / 10, 1/2 - math.sqrt(15) / 10, 1/2]
    sum = 0
    for i in range(3):
        sum += W[i] * fn(a + X[i] * (b - a))
    return (b - a) * sum
