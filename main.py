# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D
import numpy as np

# My files
import MatrixDemoMath as mm
import MatrixDemoGraphics as mg
import global_vars as gv

Array1 = np.array([[1.0, 0.0], [0.0, 1.0]])

axisLimit = 2  # Coordinate limits for x-y plots
stepsPerOrbit = 150  # This determines smoothness of animation
dotsPerOrbit = 40  # Number of circular patches to plot on unit circle

global ax2, axBar, bgBar, bg1, bg2, barlist


# Create initial x-y, text, and bar plots, then save backgrounds
def create_initial_graphics():
    global ax2, axBar, bgBar, bg1, bg2, barlist

    # Create top-right plot with dashed unit circle
    th = np.linspace(0, 2 * np.pi, 201)
    plt.subplot(222)
    gv.ax1 = plt.gca()
    plt.plot(np.cos(th), np.sin(th), 'k--')  # Make dashed circle
    plt.xlim([-axisLimit, axisLimit])
    plt.ylim([-axisLimit, axisLimit])
    plt.show(block=False)

    linex = np.linspace(-1, 1, 9)
    lines = []
    for i in range(0,9):
#        plt.plot([-axisLimit, axisLimit], [linex[i], linex[i]], '--', color="grey")
#        plt.plot([linex[i], linex[i]], [-axisLimit, axisLimit], '--', color="grey")
        lines.append([(-axisLimit, linex[i]), (axisLimit, linex[i])])
        lines.append([(linex[i], -axisLimit), (linex[i], axisLimit)])

    # Create bottom-left bar plot
    plt.subplot(223)
    axBar = plt.gca()
    barlist = plt.bar([0, 1], [0, 0])
    barlist[0].set_color('b')
    barlist[1].set_color('g')
    plt.xticks([0, 1], ['x', 'y'])
    plt.ylim([-axisLimit, axisLimit])
    plt.show(block=False)

    # Create bottom-right output plot with dashed circle
    plt.subplot(224)
    ax2 = plt.gca()
    plt.plot(np.cos(th), np.sin(th), 'k--')  # Make dashed circle
    plt.xlim([-axisLimit, axisLimit])
    plt.ylim([-axisLimit, axisLimit])
    plt.show(block=False)

    # Need this so that background bitmaps will be up to date
    canvas.draw()

    # Save background bitmaps
    bgBar = canvas.copy_from_bbox(axBar.bbox)
    bg1 = canvas.copy_from_bbox(gv.ax1.bbox)
    bg2 = canvas.copy_from_bbox(ax2.bbox)


if __name__ == '__main__':
    print('\nMatrix demo instructions:\n\n' +
          '"a" toggles animation\n' +
          '"c" toggles circular ring of dots\n' +
          '"u" normalizes matrix rows to have unit length\n' +
          '"2" toggles between 1 or 2 matrix rows\n' +
          '"4" toggles output x-y plot\n' +
          'Left mouse button drag moves vector1\n' +
          'Right mouse button drag moves vector2\n' +
          '"x" to exit')

# Determine steps between circumference dots
u = mm.UnitCircleStuff(stepsPerOrbit, dotsPerOrbit, mg.INPUT_VECTOR_COLOR)
stepsPerOrbit = u.steps  # This might be changed, to be an integer multiple of dotsPerOrbit
print('Total steps {:d}, circumference dots {:d}'.format(u.steps, u.numdots))

# Create figure
gObjects = mg.GraphicsObjects()

canvas = gObjects.canvas

# Create static objects, and save background bitmaps so we don't have to redraw them over and over.
# This greatly speeds up animation
create_initial_graphics()

mm.quitflag = False

# Write array values with specified y-coordinate
gObjects.textObj.update_array_text(Array1)

# Add vector1 (top row of 2x2 array) to top-right graph
matrixArrows = [mpatches.FancyArrowPatch((0, 0), tuple(Array1[0, :]), color='b', mutation_scale=20)]
gv.ax1.add_patch(matrixArrows[0])
# Add vector2 (bottom row of 2x2 array) to top-right graph
matrixArrows.append(mpatches.FancyArrowPatch((0, 0), tuple(Array1[1, :]), color='g', mutation_scale=20))
gv.ax1.add_patch(matrixArrows[1])

# Generate starting points around unit circle
u.makeCircs(Array1, mg.OUTPUT_VECTOR_COLOR)

currentStep = 0
start = True
cycles = 0

# Create arrows
arrowInput = mpatches.FancyArrowPatch((0, 0), (0, 0), color=mg.INPUT_VECTOR_COLOR, mutation_scale=10)
arrowOutput = mpatches.FancyArrowPatch((0, 0), (0, 0), color=mg.OUTPUT_VECTOR_COLOR, mutation_scale=10)
gv.ax1.add_patch(arrowInput)
ax2.add_patch(arrowOutput)
if not mg.flagShow4:
    plt.sca(ax2)
    plt.axis('off')

# Add "shadow" and perpendicular "normal" lines to input axis
lineNormal = gv.ax1.add_line(Line2D([0, 0], [1, 1], color=mg.INPUT_VECTOR_COLOR))
lineShadow = gv.ax1.add_line(Line2D([0, 0], [1, 1], color='b'))

# Add shadow lines to output axis
lineOutputX = ax2.add_line(Line2D([0, 0], [1, 1], color='b'))
lineOutputY = ax2.add_line(Line2D([0, 0], [1, 1], color='g'))

# Need to call this the first time or else objects won't draw later
plt.pause(0.01)
localRedrawAxes = False
localAnimate = mg.flagAnimate  # Need local copy of this flag so we can detect when it changes state

while mg.quitflag == 0:
    # V1 is "input" vector in top-right plot
    vector_input = [u.unitVectorX[currentStep], u.unitVectorY[currentStep]]

    # V2 is transformed vector in lower-right plot
    vector_output = np.matmul(Array1, vector_input)

    # Get normal vector for matrix row 1
    matrixRow1Norm = Array1[0, :] / np.linalg.norm(Array1[0, :])

    # Dot product of input vector with normalized array row 1
    matrixRow1Dot = np.dot(matrixRow1Norm, vector_input)
    # Update position of line indicating normal/perpendicular
    normalXvalues = [vector_input[0], matrixRow1Norm[0] * matrixRow1Dot]
    normalYvalues = [vector_input[1], matrixRow1Norm[1] * matrixRow1Dot]
    lineNormal.set_data(normalXvalues, normalYvalues)
    # Update position of line indicating shadow/projection onto unit vector
    if matrixRow1Dot < 0:
        # Negative dot product, need to draw extra line
        shadowXvalues = [0, matrixRow1Norm[0] * matrixRow1Dot]
        shadowYvalues = [0, matrixRow1Norm[1] * matrixRow1Dot]
    else:
        # Zero or positive dot product, no need to draw shadow, as it would just overlap line
        shadowXvalues = [0, 0]
        shadowYvalues = [0, 0]
    lineShadow.set_data(shadowXvalues, shadowYvalues)

    # Update input and output vector text
    gObjects.textObj.update_input_vector(vector_input)
    gObjects.textObj.update_output_vector(vector_output, mg.matrixRowsToShow)
    gObjects.textObj.redraw()

    # Bar chart
    canvas.restore_region(bgBar)  # Restores static elements and erases background
    barlist[0].set_height(vector_output[0])
    axBar.draw_artist(barlist[0])
    if mg.matrixRowsToShow > 1:
        barlist[1].set_height(vector_output[1])
        axBar.draw_artist(barlist[1])
    else:
        barlist[1].set_height(0)

    # Now render to screen
    canvas.blit(axBar.bbox)

    # Draw next circumference dot on input and output x-y plots
    if currentStep % u.stepsPerDot == 0 and cycles == 0:
        currentDot = int(currentStep / u.stepsPerDot)

        # Add new input dot
        circ = u.patchList1[currentDot]
        gv.ax1.add_patch(circ)
        gv.ax1.draw_artist(circ)

        # Add new output dot
        circ = u.patchList2[currentDot]
        ax2.add_patch(circ)      # This is needed for draw_artist to work. However, patch may now show up extraneously, e.g. when mouse rolls over button
        ax2.draw_artist(circ)

    # Draw top-right graph
    canvas.restore_region(bg1)  # Restores static elements and erases background
    arrowInput.set_positions((0, 0), tuple(vector_input))

    if mg.matrixRowsToShow <= 1:
        # Draw unit arrow and first matrix row, but nothing else
        gv.ax1.draw_artist(matrixArrows[0])
        gv.ax1.draw_artist(arrowInput)
        gv.ax1.draw_artist(lineNormal)
        gv.ax1.draw_artist(lineShadow)
    else:
        if mg.flagShow4 and mg.flagCircum:
            # Draw all items including circumference dots
            for p in gv.ax1.patches:
                gv.ax1.draw_artist(p)
        else:
            # Draw unit arrow and both matrix arrows but no circumference dots
            gv.ax1.draw_artist(matrixArrows[0])
            gv.ax1.draw_artist(matrixArrows[1])
            gv.ax1.draw_artist(arrowInput)

    # Draw bottom-right graph elements, if needed
    if mg.flagShow4 and mg.matrixRowsToShow > 1:
        canvas.restore_region(bg2)  # Restores static elements and erases background
        arrowOutput.set_positions((0, 0), tuple(vector_output))

        # Draw output vectors
        lineOutputX.set_data([0, vector_output[0]], [0, 0])
        lineOutputY.set_data([vector_output[0], vector_output[0]], [0, vector_output[1]])
        ax2.draw_artist(lineOutputX)
        ax2.draw_artist(lineOutputY)

        # Draw purple circle patches
        if mg.flagCircum:
            [ax2.draw_artist(p) for p in ax2.patches]
        else:
            ax2.draw_artist(arrowOutput)

        #
        plt.sca(ax2)
        plt.axis('on')
    else:
        ax2.draw_artist(ax2.patch)  # Erase background
        plt.sca(ax2)
        plt.axis('off')

    # Render to screen
    canvas.blit(gv.ax1.bbox)
    canvas.blit(ax2.bbox)

    if localRedrawAxes:
        plt.pause(0.01) # Need this to redraw entire plot axis when output panel (lower right) is togged on/off
        localRedrawAxes = False

    while not mg.quitflag:

        # Need this to update graphics, and respond to GUI events, e.g. button presses.
        canvas.flush_events()

        if localAnimate and not mg.flagAnimate:
            # Global flag just switched off. Turn off local animation, but also break so we run one more loop
            localAnimate = False
            break
        if not localAnimate and mg.flagAnimate:
            # Global flag just switched on. Copy state to local flag
            localAnimate = True

        if mg.flagChangeMatrix:
            mg.flagRecalc = False
            mg.flagChangeMatrix = False
            if mg.flagX is not None and mg.flagY is not None:  # Because x, y won't be valid if mouse went out of bounds
                r = mg.whichRowToAdjust
                if r == -1:
                    # User hit letter "u", so we normalize matrix rows to unit length
                    m1 = np.linalg.norm(Array1[0, :])
                    m2 = np.linalg.norm(Array1[1, :])
                    Array1[0, :] = Array1[0, :] / m1
                    Array1[1, :] = Array1[1, :] / m2
                    matrixArrows[0].set_positions((0, 0), tuple(Array1[0, :]))
                    matrixArrows[1].set_positions((0, 0), tuple(Array1[1, :]))
                else:
                    Array1[r, 0] = mg.flagX
                    Array1[r, 1] = mg.flagY
                    matrixArrows[r].set_positions((0, 0), tuple(Array1[r, :]))
                u.updateCircs(Array1)
                gObjects.textObj.update_array_text(Array1)  # Will this take effect without calling redraw()???
                break

        if mg.flagRedrawAxes:
            mg.flagRedrawAxes = False
            localRedrawAxes = True
            break

        if mg.flagRecalc:
            mm.flagRecalc = False
            break

        if localAnimate:
            break


    if mg.quitflag:
        break

    if mg.flagAnimate:
        currentStep = currentStep + 1
        if currentStep >= u.steps:
            cycles = cycles + 1
            currentStep = currentStep - stepsPerOrbit

if mg.quitflag == 0:
    plt.show()  # This will block until window is closed.
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
