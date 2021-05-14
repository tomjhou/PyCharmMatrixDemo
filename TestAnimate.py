import numpy as np
from matplotlib import pyplot as plt
from matplotlib.collections import LineCollection
import matplotlib.animation as animation

lines = []
for i in range(10):
    for j in range(10):
        lines.append([(0, i), (1, j)])

fig, ax = plt.subplots()
colors = np.random.random(len(lines))
col = LineCollection(lines, array=colors, cmap=plt.cm.gray)
ax.add_collection(col)
ax.autoscale()

def update(num, collection):
    colors = [(c, c, c) for c in np.random.random(len(lines))]
    collection.set_color(colors)
    return collection,

ani = animation.FuncAnimation(fig, update, 100, fargs=[col], interval=25, blit=True)
plt.show()
