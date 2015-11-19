### 3D Rotations ###
#
# taking function A and rotating it around function B 
# using the disc/washer method to plot an array of points
# 
# 11/18/2015

# these all need to be installed. the urls are here:
import numpy as np 					# http://www.scipy.org/scipylib/download.html
from sympy import Symbol, solve 	# http://www.sympy.org/en/download.html
import matplotlib.pyplot as plt 	# http://matplotlib.org/downloads.html

# set up the two curves - these can be changed manually
def function_a(x, derivative):
	if derivative:
		return (2)
	else:
		return (2*x + 1)

def function_b(x, derivative):
	if derivative:
		return (1)
	else:
		return (x)

# set up original curves
xvals = np.linspace(0, 2, 100)
a_yvals = function_a(xvals, derivative=False)
b_yvals = function_b(xvals, derivative=False)

# take each point on curve B, make perpendicular line to it, find point on curve A 
# that it intersects, draw a circle with this point around B:
for i in range(len(xvals)):

	b_x = xvals[i]
	b_y = b_yvals[i]

	# get perpendicular slope to reflection point on curve B 
	slope = function_b(b_x, derivative=True)
	slope = -(slope)**(-1)
	new_line_ys = []
	for l in xvals:
		new_line_ys.append((slope*(l - b_x) + b_y))
	plt.plot(xvals, new_line_ys, "y-") 
	
	# find which point on curve A lies on the line corresponding to above slope and point
	x = Symbol('x')
	print b_x, solve((slope*(x - b_x) + b_y) - function_a(x, derivative=False), x)



plt.plot(xvals, a_yvals, "b-")
plt.plot(xvals, b_yvals, "r-")
plt.xlim(0, 2)
plt.ylim(0, 2)
plt.show()