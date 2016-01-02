#########################
### Rotations Project ###

# take a function A and rotate it around function B, plot the results.
# use approximations of derivitives and intersections to rotate each point on
# line A perpendicularly around line B

# Henry Peterson 1-1-16
#######################

from numpy import *   # for user input
import numpy as np    # because I like using 'np.'
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


# get equations of the two curves, must be in python syntax
function_a = raw_input("Function to be rotated: ")    #blue
function_b = raw_input("Function to provide axis of rotation: ")    #red

# set up domain
MIN = float(raw_input("Min x value: "))
MAX = float(raw_input("Max x value: "))
NUM = 500
xvals = np.linspace(MIN, MAX, NUM)

# set up original curves by populating lists with eval() outputs
a_yvals = []
b_yvals = []
for x in xvals:
    a_yvals.append(eval(function_a))
    b_yvals.append(eval(function_b))

# plot what we have so far and set up for the rest
fig = plt.figure()
ax = fig.gca(projection='3d')
ax.plot(xvals, a_yvals, "b-", alpha=1.0)
ax.plot(xvals, b_yvals, "r-", alpha=1.0)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# take each point on curve B, approximate tangent line to it, make perpendicular line to the tangent,
# find point on curve A that it intersects, draw a circle with this point around B:
for i in range(len(xvals)):
    
    b_x = xvals[i]
    b_y = b_yvals[i]
    
    # dont make a circle of radius 0...
    if a_yvals[i] == b_y:
        continue
    
    # get perpendicular slope to reflection point on curve B 
    # use approx of slope 
    if i>=1:
        tan_slope = (b_yvals[i]-b_yvals[i-1])/(xvals[i]-xvals[i-1])
    else:
        tan_slope = (b_yvals[i]-b_yvals[i+1])/(xvals[i]-xvals[i+1])
        
    # find approx where perp_line and rotating line intersect
    solutions = []
    if tan_slope == 0:    # must make it so that flat lines work too
        solutions.append(b_x)
    else:
        # perpendicular is neg recip
        slope = tan_slope**(-1)
        slope = -slope
        perp_line = slope*(xvals - b_x) + b_y
        
        # check when difference in yvals changes sign, approx intersection
        positive = None
        for j in range(len(xvals)):
            diff = perp_line[j]-a_yvals[j]
            old_positive = positive
            if diff>0:
                positive = True
            elif diff==0:
                solutions.append(xvals[j])
            else:
                positive = False

            if old_positive != None:
                if old_positive != positive:
                    solutions.append(xvals[j])

    # make a circle for every solution
    for a_x in solutions:
        
        # for eval() to work it must be an 'x'
        x = a_x
        a_y = eval(function_a)
        
        # calc radius, plot line of circle diameter otherwise 
        if tan_slope == 0:    # again, making sure it works for vertical lines
            radius = np.abs(a_y - b_y)
            circle_xs = [a_x]*100
            circle_ys = np.linspace(b_y-radius, b_y+radius, 100)
        else:
            # radius of circle is dist btwn point on line A and point on line B
            delta_x = np.abs(float(b_x-a_x))
            delta_y = np.abs(float(b_y-a_y))
            radius = np.sqrt((delta_x)**2 + (delta_y)**2)

            # make a line segment on xy plane that is circle's diameter
            circle_xs = np.linspace(b_x-delta_x, b_x+delta_x, 100) 
            circle_ys = slope*(circle_xs - b_x) + b_y
        
        # z points are a function of x and y, make a circle
        circle_zs = []
        for k in range(len(circle_xs)):
            # solve for z in distance formula
            magnitude = np.sqrt(radius**2 - (circle_xs[k]-b_x)**2 - (circle_ys[k]-b_y)**2)

            # bottom and top of circle
            circle_zs.append(magnitude)
            circle_zs.append(-magnitude)

        # double all the points on the x and y axes to account for top and bottom of circle
        circle_xs = np.repeat(circle_xs, 2)
        circle_ys = np.repeat(circle_ys, 2)
        
    
        # plot this particular circle and do the next one
        ax.plot(circle_xs, circle_ys, circle_zs, c='g', alpha=.1)

### make sure it's not distorted
diff = MAX - MIN + 4    # length of one side of cubic graph
diff = diff/2.0         # half so we can start from midpoint
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