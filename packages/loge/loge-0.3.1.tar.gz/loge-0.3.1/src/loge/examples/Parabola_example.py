import matplotlib.pyplot as figure
import numpy as np

#! ####*Quadratic function y = ax^2 + bx + c*

#%img parabola.png

#! Quadratic function coefficients

possible_a_list = [-10.0, -2.0, 5.0, 20.0 ]
a = possible_a_list[3] #<< - set a coefficient

b = 9 #<< - set b coefficient
c = -40 #<< - set c coefficient

# The roots (zeros) calculateing
delta = b**2 - 4*a*c #%requ
if delta >= 0:
    #! ###There are roots :) 
    x1 = (-b + delta**0.5) / (2 * a) #%requ - first root
    x2 = (-b - delta**0.5) / (2 * a) #%requ - second root
else:
    #! ###Roots not exist :(
    x1 = 'not exist'
    x2 = 'not exist'

# Our quadratic function plot
xi_from = -3 #<< - plot form x value
xi_to = 4 #<< - plot to x value
xi = np.arange(xi_from, xi_to, 1)
yi = a * xi**2 + b * xi + c
figure.grid()
figure.plot(xi, yi) #%plt
figure.clf()
