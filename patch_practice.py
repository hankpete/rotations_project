# patch practice

import matplotlib.pyplot as plt
from matplotlib.patches import Circle, PathPatch
from mpl_toolkits.mplot3d import Axes3D 
from patches_rotation_funcs import *

fig = plt.figure()
ax=fig.gca(projection='3d')

circle = Circle((.5, .5), 1)
ax.add_patch(circle)
pathpatch_2d_to_3d(circle, z=0, normal=(1,3,0))


ax.set_xlim3d(-2, 2)
ax.set_ylim3d(-2, 2)
ax.set_zlim3d(-2, 2)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

plt.show()

