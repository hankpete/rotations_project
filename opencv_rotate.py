# Use code from 3D_Rotations along with the power of opencv to rotate drawings

import cv2
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D	
import os

# first we take a picture and find the edges in the objects
filename = os.path.normpath("c:/Users/Henry/Documents/Programs/Github/rotations_project/Curve.jpg")
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

# for some reason .shape outputs (y, x) coordinates
for y in range(shape[0]):
	for x in range(shape[1]):
		if edges.item(y, x) != 0:
			 xvals.append(x)
			 yvals.append(y)

# # testing corner detection
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

# set up a 3D graph
fig = plt.figure()
ax = fig.gca(projection='3d')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# our current calculations for the horizontal line running through the shape
distance = (max(yvals) - min(yvals))/2.0
ymiddle = min(yvals) + distance

# this is the main loop. it takes each pixel point on and edge and rotates it around 
# the horizontal line. 3D_Rotations.py for more info on how this is done
for i in range(len(xvals)):
	x = xvals[i]
	y = yvals[i]

	radius = np.abs(y - ymiddle)
	# make a line segment on xy plane that is circle's diameter
	circle_xs = [x]*50
	circle_ys = np.linspace(ymiddle-radius, ymiddle+radius, 50)

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

# plt.subplot(121)
# plt.title("Edges")
# plt.imshow(edges, cmap='gray')
# plt.xticks([]), plt.yticks([])

# # plt.subplot(122)
# # plt.title("Corners")
# # plt.imshow(img)
# # #plt.xticks([]), plt.yticks([])

# plt.show()