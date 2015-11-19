from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

x = np.linspace(-1, 1, 100)
y = np.sqrt(1 - x**2)
z = np.sqrt(1 - x**2)

print x
print y
print z

ax.plot_surface(x, y, z, color='r')

plt.show()
