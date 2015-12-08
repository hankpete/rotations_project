#Rotations Project

##A project in python whose goal is to rotate a curve about another curve and plot it in many ways.

####Here are some examples of 3D_Rotations.py outputs:
y = x rotated about y = x^2:
![Alt text](figure_1.png?raw=true "y = x rotated about y = x^2")
y = x rotated about y = sin(pi*x):
![Alt text](figure_2.png?raw=true "y = x rotated about y = sin(pi*x)")

####Here is what opencv_rotate.py can do so far:
The original image was a simple curve drawn with MS Paint. Here are its edges found by opencv:
![Alt text](figure_1.png?raw=true "Edges of Curve")
The code then takes those edges and rotates each point on them about a horizontal line slicking through the curve:
![Alt text](figure_2.png?raw=true "Rotated Curve")

####Plans
The opencv code is still a work in progress and the next step would be to make the rotator line 
more sensible and also the picking of points more efficient. 