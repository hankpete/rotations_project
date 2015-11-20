### 3D Rotations ###
#
# taking function A and rotating it around function B 
# using the disc/washer method to plot an array of points
# 
# 11/18/2015

# some of these need to be installed. the urls are here:
import numpy as np 					# http://www.scipy.org/scipylib/download.html
from sympy import Symbol, solve 	# http://www.sympy.org/en/download.html
import matplotlib.pyplot as plt 	# http://matplotlib.org/downloads.html
from mpl_toolkits.mplot3d import Axes3D

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
MIN = 0
MAX = 2
STEP = 10
xvals = np.linspace(MIN, MAX, STEP)
a_yvals = function_a(xvals, derivative=False)
b_yvals = function_b(xvals, derivative=False)

# plot what we have so far and set up for the rest
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot(xvals, a_yvals, "b-")
ax.plot(xvals, b_yvals, "r-")
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# take each point on curve B, make perpendicular line to it, find point on curve A 
# that it intersects, draw a circle with this point around B:
for i in range(len(xvals)):

	b_x = xvals[i]
	b_y = b_yvals[i]

	# get perpendicular slope to reflection point on curve B 
	slope = function_b(b_x, derivative=True)
	slope = -(slope)**(-1)
	
	# find which point on curve A lies on the line corresponding to above slope and point
	x = Symbol('x')		# sympy's "Symbol" makes x a variable
	a_x = solve((slope*(x - b_x) + b_y) - function_a(x, derivative=False), x)	# sympy's "solve" sets expression to zero
	a_x = a_x[0]
	if a_x < MIN or a_x > MAX:
		continue
	a_y = function_a(a_x, derivative=False)

	# radius of circle is dist btwn point on line A and point on line B
	delta_x = float(b_x-a_x)
	delta_y = float(b_y-a_y)
	radius = np.sqrt((delta_x)**2 + (delta_y)**2)

	# make a line segment on xy plane that is circle's diameter
	circle_xs = np.linspace(b_x-delta_x, b_x+delta_x, 100) 
	circle_ys = slope*(circle_xs - b_x) + b_y

	# z points are a function of x and y, make a circle
	circle_zs = []
	for i in range(len(circle_xs)):
		# used distance formula and pythagorean theorem to find z
		magnitude = np.sqrt(float(.5*((2*radius)**2 - (circle_ys[i]-circle_ys[0])**2 - \
			(circle_ys[i]-circle_ys[len(circle_ys)-1])**2 - (circle_xs[i]-circle_xs[0])**2 - (circle_xs[i]-circle_xs[len(circle_xs)-1])**2)))
		circle_zs.append(magnitude)
		circle_zs.append(-magnitude)

	circle_xs = np.repeat(circle_xs, 2)
	circle_ys = np.repeat(circle_ys, 2)

	# plot this particular circle and do the next one
	ax.scatter(circle_xs, circle_ys, circle_zs, c="g")

plt.show()