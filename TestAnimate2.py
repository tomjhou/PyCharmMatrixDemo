
# Implementation of matplotlib function
from random import randint, choice
import time
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


back_color = "black"
colors = ['red', 'green', 'blue', 'purple']
width, height = 4, 4

fig, ax = plt.subplots()
ax.set(xlim =[0, width], ylim =[0, height])

fig.canvas.draw()

def update():
    x = randint(0, width - 1)
    y = randint(0, height - 1)

    arti = mpatches.Rectangle(
        (x, y), 1, 1,
        facecolor = choice(colors),
        edgecolor = back_color
    )
    ax.add_artist(arti)

    start = time.time()
    ax.draw_artist(arti)
    fig.canvas.blit(ax.bbox)
    print("Time :", start, ", duration ", time.time() - start)

timer = fig.canvas.new_timer(interval = 25)
timer.add_callback(update)
timer.start()

ax.set_title('matplotlib.axes.Axes.draw_artist()\
 function Example')

plt.show()
