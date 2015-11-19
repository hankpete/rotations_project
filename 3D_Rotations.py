### 3D Rotations ###
#
# taking function A and rotating it around function B 
# using the disc/washer method to plot an array of points
# 
# 11/18/2015

import numpy as np
from sympy import Symbol, solve 
import matplotlib.pyplot as plt

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

xvals = np.arange(0, 2, .1)
a_yvals = []
b_yvals = []

for i in xvals:
	a_yvals.append(function_a(i, derivative=False))
	b_yvals.append(function_b(i, derivative=False))


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
plt.xlim(-1, 4)
plt.ylim(-1, 4)
plt.show()