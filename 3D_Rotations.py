### 3D Rotations ###
#
# taking function A and rotating it around function B 
# using the disc/washer method to plot an array of points
# 
# 11/18/2015

# some of these need to be installed appart from regular python installation. the urls are here:
import numpy as np 								# http://www.scipy.org/scipylib/download.html
from sympy import Symbol, solve 				# http://www.sympy.org/en/download.html
import matplotlib.pyplot as plt 				# http://matplotlib.org/downloads.html
from mpl_toolkits.mplot3d import Axes3D			# part of ^this one

# set up the two curves - these can be changed manually
def function_a(x):
	return (5*x + 1)

def function_b(x, derivative):
	if derivative:		# need this for when we make perpendicular lines
		return (.5)
	else:
		return (.5*x)

# set up original curves
MIN = 0
MAX = 2
NUM = 10
xvals = np.linspace(MIN, MAX, NUM)
a_yvals = function_a(xvals)
b_yvals = function_b(xvals, derivative=False)

# plot what we have so far and set up for the rest
# my_dpi = 144
# fig = plt.figure(figsize=(700/my_dpi, 700/my_dpi), dpi=my_dpi)
fig =plt.figure()
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
	slope = slope**(-1)
	slope = -slope

	# find which point on curve A lies on the line corresponding to above slope and point
	x = Symbol('x')		# sympy's "Symbol" makes x a variable
	a_x = solve((slope*(x - b_x) + b_y) - (5*x +1), x)	# sympy's "solve" sets expression to zero
	a_x = a_x[0]
	if a_x < MIN or a_x > MAX:
		continue
	a_y = function_a(a_x)

	# radius of circle is dist btwn point on line A and point on line B
	delta_x = np.abs(float(b_x-a_x))
	delta_y = np.abs(float(b_y-a_y))
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
		# bottom and top of circle
		circle_zs.append(magnitude)
		circle_zs.append(-magnitude)

	# double all the points on the x and y axes to account for top and bottom of circle
	circle_xs = np.repeat(circle_xs, 2)
	circle_ys = np.repeat(circle_ys, 2)

	# plot this particular circle and do the next one
	ax.plot(circle_xs, circle_ys, circle_zs)
	#ax.scatter(circle_xs, circle_ys, circle_zs, c="g")

# make sure it's not distorted
diff = MAX+2 - (MIN-2)
ax.set_xlim(MIN-2, MAX+2)
ax.set_ylim(MIN-2, MAX+2)
ax.set_zlim(-diff/2.0, diff/2.0)

# finish
plt.show()