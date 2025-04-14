import math

# D(x) = (D(rh) - r^n *D(h))/(1 - r^n) 
# Richardson's Extrapolation

f1 = lambda x: math.sin(x)

def D_r(fn ,x ,r ,h ) :
    return (fn(x + r*h) -fn(x - r*h))/(2*r*h)

def richardson_extrapolation(fn ,x ,r ,h ):
    return (D_r(fn ,x ,r ,h ) - (r**2)*D_r(fn ,x ,1 ,h ))/(1 - r**2) 

x = 0.5
h = 0.1

print()

a = richardson_extrapolation(f1 ,x ,2 ,h )
b = richardson_extrapolation(f1 ,x ,0.01 ,h )

print(a)
print(b)