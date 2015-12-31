# Use code from 3D_Rotations along with the power of opencv to rotate drawings

import cv2
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D	
import os
from scipy import stats					# http://sourceforge.net/projects/scipy/files/


#####################################################
# # Corner Detection
# gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

# gray = np.float32(gray)
# destination = cv2.cornerHarris(gray,2,3,.05)

# destination = cv2.dilate(destination,None)
# img[destination>.01*destination.max()]=[0,0,0]
# img = img[:,:,::-1]		# bgr to rgb

# b = []
# for x in range(shape[0]):
# 	for y in range(shape[1]):
# 		if img.item(x, y, 0) == 0:
# 			if img.item(x, y, 1) == 0:
# 				if img.item(x, y, 2) == 0:
# 					b.append([x, y])
#####################################################



# first we take a picture and find the edges in the objects
filename = os.path.normpath("c:/Users/Henry/Documents/Programs/Github/rotations_project/Arrow.jpg")
img = cv2.imread(filename, 1)
img = img[:,:,::-1]		# bgr to rgb

# edge detection
edges = cv2.Canny(img, 100, 200)

# plot it to show 
plt.title("Edges")
plt.imshow(edges, cmap='gray')
plt.xticks([]), plt.yticks([])
plt.show()

# now we get the dimensions of the picture and start calculating....
shape = edges.shape

xvals = []
yvals = []


# shape outputs (rows, columns) or for our purposes, (y, x)
for row in range(shape[0]):
	for column in range(shape[1]):
		if edges.item(row, column) == 255:		# get the white pixels (edges)
			xvals.append(column)
			yvals.append(row)





slope, intercept, rvalue, pvalue, stderr = stats.linregress(xvals,yvals)
print slope 
print intercept
input()













# set up a 3D graph
fig = plt.figure()
ax = fig.gca(projection='3d')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# this is the main loop. it takes each pixel point on and edge and rotates it around 
# the horizontal line. 3D_Rotations.py for more info on how this is done
while xvals:			# choosing a while loop because I will be deleting pixels in the lists as I go
	x = xvals[0]
	y = yvals[0]

	# find other pixel with same xval
	other_y = None
	for j in range(len(xvals)):
		if (xvals[j] == x) and (j != 0):
			other_y = yvals[j]
			xvals.remove(xvals[j])
			xvals.remove(xvals[0])
			yvals.remove(yvals[j])
			yvals.remove(yvals[0])
			break

	# skip this pixel if it doesnt have a partner
	if not other_y:
		xvals.remove(xvals[0])
		yvals.remove(yvals[0])
		continue

	radius = np.abs(y - other_y)/2.0
	ymiddle = min(y, other_y) + radius
	# make a line segment on xy plane that is circle's diameter
	circle_xs = [x]*100
	circle_ys = np.linspace(ymiddle-radius, ymiddle+radius, 100)

	# z points are a function of x and y, make a circle
	circle_zs = []
	for i in range(len(circle_xs)):
		# new magnitude calculation is faster: solve for z in distance formula
		magnitude = np.sqrt(radius**2 - (circle_ys[i]-ymiddle)**2)

		# bottom and top of circle
		circle_zs.append(-magnitude)
		circle_zs.append(magnitude)

	# double all the points on the x and y axes to account for top and bottom of circle
	circle_xs = np.repeat(circle_xs, 2)
	circle_ys = np.repeat(circle_ys, 2)

	# plot this particular circle and do the next one
	ax.plot(circle_xs, circle_ys, circle_zs, c='g', alpha=.25)

# fix distortion
longest = max(shape[0], shape[1])
ax.set_xlim(0, longest) 
ax.set_ylim(0, longest)
ax.set_zlim(-longest/2.0, longest/2.0)
plt.show()