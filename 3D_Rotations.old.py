### 3D Rotations ###
#
# taking function A and rotating it around function B 
# using the disc/washer method to plot an array of points
# 
# 11/18/2015

# some of0 th1se need to be installed appart from regular python installation. the urls are here:
import numpy as np 								# http://www.scipy.org/scipylib/download.html
from sympy import Symbol, solve 				# http://www.sympy.org/en/download.html
import matplotlib.pyplot as plt 				# http://matplotlib.org/downloads.html
#from matplotlib.patches import Circle 			# part of ^this one
from mpl_toolkits.mplot3d import Axes3D			# also part of that one
#from patches_rotation_funcs import *			# own library

# set up the two curves - these can be changed manually
def function_a(x):		#blue curve - rotated
	y = x**(.5)
	return (y)

def function_b(x, derivative):		#red curve - rotator
	y = np.sin(x)
	yprime = np.cos(x)
	if derivative:		# need this for when we make perpendicular lines
		return (yprime)
	else:
		return (y)

# set up original curves
MIN = 0
MAX = 4
NUM = 100
xvals = np.linspace(MIN, MAX, NUM)

a_yvals = function_a(xvals)
b_yvals = function_b(xvals, derivative=False)

# plot what we have so far and set up for the rest
fig = plt.figure()
ax = fig.gca(projection='3d')
ax.plot(xvals, a_yvals, "b-", alpha=1.0)
ax.plot(xvals, b_yvals, "r-", alpha=1.0)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# take each point on curve B, make perpendicular line to it, find point on curve A 
# that it intersects, draw a circle with this point around B:
for i in range(len(xvals)):

	b_x = xvals[i]
	b_y = b_yvals[i]

	# dont make a circle of radius 0...
	if a_yvals[i] == b_y:
		continue

	# get perpendicular slope to reflection point on curve B 
	slope = function_b(b_x, derivative=True)
	if slope == 0:
		slope = 1000000		# aproximate vertical line
	else:
		slope = slope**(-1)
		slope = -slope

	# find which point on curve A lies on the line corresponding to above slope and point
	x = Symbol('x')		# sympy's "Symbol" makes x a variable
	a_x = solve((slope*(x - b_x) + b_y) - function_a(x), x)	# sympy's "solve" sets expression to zero

	# get rid of complex numbers 
	new = []
	for i in a_x:
		if 'I' not in str(i):
			new.append(i)

	# make a circle for every solution instead of just the first one it finds
	for a_x in new:
		if a_x < MIN or a_x > MAX:
			continue
		a_y = function_a(a_x)

		# radius of circle is dist btwn point on line A and point on line B
		delta_x = np.abs(float(b_x-a_x))
		delta_y = np.abs(float(b_y-a_y))
		radius = np.sqrt((delta_x)**2 + (delta_y)**2)

		# # how i would use the circle pannels if they worked
		# circle = Circle((b_x, b_y), radius=radius)
		# ax.add_patch(circle)
		# #guess =
		# # something is weird - the circles break off at 1....
		# if b_x > 1:
		# 	pathpatch_2d_to_3d(circle, z=0, normal=((b_x-1), function_b(b_x-1, derivative=False), 0))
		# else:
		# 	pathpatch_2d_to_3d(circle, z=0, normal=((b_x-1), function_b(b_x-1, derivative=False), 0))
		# pathpatch_translate(circle, b_x)


		# make a line segment on xy plane that is circle's diameter
		circle_xs = np.linspace(b_x-delta_x, b_x+delta_x, 100) 
		circle_ys = slope*(circle_xs - b_x) + b_y

		# z points are a function of x and y, make a circle
		circle_zs = []
		for i in range(len(circle_xs)):
			# new magnitude calculation is faster: solve for z in distance formula
			magnitude = np.sqrt(radius**2 - (circle_xs[i]-b_x)**2 - (circle_ys[i]-b_y)**2)

			# bottom and top of circle
			circle_zs.append(magnitude)
			circle_zs.append(-magnitude)

		# double all the points on the x and y axes to account for top and bottom of circle
		circle_xs = np.repeat(circle_xs, 2)
		circle_ys = np.repeat(circle_ys, 2)

		# plot this particular circle and do the next one
		ax.plot(circle_xs, circle_ys, circle_zs, c='g', alpha=.25)
		#ax.scatter(circle_xs, circle_ys, circle_zs, c="g")

### make sure it's not distorted
diff = MAX - MIN + 4	# length of one side of cubic graph
diff = diff/2.0			# half so we can start from midpoint
# determine where the middle of the graph is on the y axis 
a_yvalsMIN = min(a_yvals)
a_yvalsMAX = max(a_yvals)
b_yvalsMIN = min(b_yvals)
b_yvalsMAX = max(b_yvals)
YMAX = max(a_yvalsMIN, b_yvalsMIN)
YMIN = min(a_yvalsMAX, b_yvalsMAX)
ymiddle = YMIN + (YMAX - YMIN)/2.0
# set the axis limits to be a nice cube
ax.set_xlim(MIN - 2, MAX + 2)
ax.set_ylim(ymiddle - diff, ymiddle + diff)
ax.set_zlim(-diff, diff)

# finish
plt.show()