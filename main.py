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

# Thickness of matrix, input, and output vectors
VECTOR_THICKNESS = 30
ARROW_COLORS_MATCH_CIRCUMFERENCE_CIRCLES = False  # If true, then arrow color matches the color of circumference circles. Otherwise, remains default red/purple

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
    plt.title("Input vectors\n(use mouse to drag vectors)")
    plt.xlabel("First dimension")
    plt.ylabel("Second dimension")
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
    plt.xticks([0, 1], ['Matrix row 1 * unit vector', 'Matrix row 2 * unit vector'])
    plt.ylim([-axisLimit, axisLimit])
    plt.title("Dot product output(s)")
    plt.ylabel("Dot product")
    plt.show(block=False)

    # Create bottom-right output plot with dashed circle
    plt.subplot(224)
    ax2 = plt.gca()
    plt.plot(np.cos(th), np.sin(th), 'k--')  # Make dashed circle
    plt.xlim([-axisLimit, axisLimit])
    plt.ylim([-axisLimit, axisLimit])
    plt.title("Output vector")
    plt.xlabel("First dimension")
    plt.ylabel("Second dimension")
    plt.show(block=False)

    # Need this so that background bitmaps will be up to date
    canvas.draw()

    # Save background bitmaps
    bgBar = canvas.copy_from_bbox(axBar.bbox)
    bg1 = canvas.copy_from_bbox(gv.ax1.bbox)
    bg2 = canvas.copy_from_bbox(ax2.bbox)


if __name__ == '__main__':
    print('\nMatrix demo instructions:\n\n' +
          '"space" toggles animation\n' +
          '"c" toggles circumference dots\n' +
          '"h" toggles projection lines\n' +
          '"u" normalizes input vectors to unit length\n' +
          '"2" toggles 1 vs 2 matrix rows\n' +
          'Left mouse button drags vectors\n' +
          '"x" to exit')

# Determine steps between circumference dots
u = mm.UnitCircleStuff(stepsPerOrbit, dotsPerOrbit, mg.CIRCUMFERENCE_COLOR1, mg.CIRCUMFERENCE_COLOR2)
stepsPerOrbit = u.numsteps  # This might be changed, to be an integer multiple of dotsPerOrbit
print('Total steps {:d}, circumference dots {:d}'.format(u.numsteps, u.numdots))

# Create figure
gObjects = mg.GraphicsObjects()

canvas = gObjects.canvas
canvas_buttons = gObjects.canvas2

# Create plots, and save background bitmaps so we don't have to redraw them over and over.
# This greatly speeds up animation
create_initial_graphics()

mm.quitflag = False

# Write array values with specified y-coordinate
gObjects.textObj.update_array_text(Array1)

# Add vector1 (top row of 2x2 array) to top-right graph
matrixArrows = [mpatches.FancyArrowPatch((0, 0), tuple(Array1[0, :]),
                                         color=mg.MATRIX_ROW1_COLOR,
                                         mutation_scale=VECTOR_THICKNESS)]   # Thickness
gv.ax1.add_patch(matrixArrows[0])
# Add vector2 (bottom row of 2x2 array) to top-right graph
matrixArrows.append(mpatches.FancyArrowPatch((0, 0), tuple(Array1[1, :]),
                                             color=mg.MATRIX_ROW2_COLOR,
                                             mutation_scale=VECTOR_THICKNESS))  # Thickness
gv.ax1.add_patch(matrixArrows[1])

# Generate starting points around unit circle
u.makeCircs(Array1, mg.OUTPUT_VECTOR_COLOR)

currentStep = 0
start = True
cycles = 0

# Create input/output arrows
arrowInput = mpatches.FancyArrowPatch((0, 0), (0, 0),
                                      color=mg.INPUT_VECTOR_COLOR,
                                      mutation_scale=VECTOR_THICKNESS)
arrowOutput = mpatches.FancyArrowPatch((0, 0), (0, 0),
                                       color=mg.OUTPUT_VECTOR_COLOR,
                                       mutation_scale=VECTOR_THICKNESS)
gv.ax1.add_patch(arrowInput)
ax2.add_patch(arrowOutput)


# Add "shadow" and perpendicular "normal" lines to input axis
lineNormal = []
lineShadow = []

########################################################################
#
#  Documentation for add_line (and other artist elements) is here:
#
#  https://matplotlib.org/1.3.0/api/artist_api.html
#
########################################################################

# Normal/shadow for first row
lineNormal.append(gv.ax1.add_line(Line2D([0, 0], [1, 1],
                                         color=(0.5, 0.5, 0.5),
                                         linestyle=':')))  # Dotted line
lineShadow.append(gv.ax1.add_line(Line2D([0, 0], [1, 1],
                                         linewidth=3,
                                         linestyle='--',   # Dashed line
                                         color=mg.SHADOW1_COLOR)))
# Normal/shadow for second row
lineNormal.append(gv.ax1.add_line(Line2D([0, 0], [1, 1],
                                         color=(0.5, 0.5, 0.5),
                                         linestyle=':')))  # Dotted line
lineShadow.append(gv.ax1.add_line(Line2D([0, 0], [1, 1],
                                         linewidth=3,
                                         linestyle='--',   # Dashed line
                                         color=mg.SHADOW2_COLOR)))

# Add shadow lines to output axis
lineOutputX = ax2.add_line(Line2D([0, 0], [1, 1],
                                  linewidth=3,
                                  color=mg.SHADOW1_COLOR))
lineOutputY = ax2.add_line(Line2D([0, 0], [1, 1],
                                  linewidth=3,
                                  color=mg.SHADOW2_COLOR))

# Need to call this the first time or else objects won't draw later
plt.pause(0.01)
localRedrawAxes = False
localAnimate = mg.flagAnimate  # Need local copy of this flag so we can detect when it changes state

while mg.quitflag == 0:
    # V1 is "input" vector in top-right plot
    vector_input = [u.unitVectorX[currentStep], u.unitVectorY[currentStep]]

    # V2 is transformed vector in lower-right plot
    vector_output = np.matmul(Array1, vector_input)

    for v in range(0,2):
        # Get normal vector for matrix row 1
        matrixRowNorm = Array1[v, :] / np.linalg.norm(Array1[v, :])

        # Dot product of input vector with normalized array row 1
        matrixRowDot = np.dot(matrixRowNorm, vector_input)

        # Update position of line indicating normal/perpendicular
        normalXvalues = [vector_input[0], matrixRowNorm[0] * matrixRowDot]
        normalYvalues = [vector_input[1], matrixRowNorm[1] * matrixRowDot]
        lineNormal[v].set_data(normalXvalues, normalYvalues)

        # Update position of line indicating shadow/projection onto unit vector
        # if matrixRowDot < 0:  # Negative dot product, need to draw extra line
        shadowXvalues = [0, matrixRowNorm[0] * matrixRowDot]
        shadowYvalues = [0, matrixRowNorm[1] * matrixRowDot]
        lineShadow[v].set_data(shadowXvalues, shadowYvalues)

    # Update input and output vector text
    if mg.flagCircum:
        # Use rainbow color for text
        gObjects.textObj.update_input_vector(vector_input, u.stepColorList[currentStep])
    else:
        # Input text color matches vector
        gObjects.textObj.update_input_vector(vector_input, mg.INPUT_VECTOR_COLOR)

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

    # Draw top-right "INPUT VECTOR" graph
    canvas.restore_region(bg1)  # Restores static elements and erases background
    arrowInput.set_positions((0, 0), tuple(vector_input))

    if ARROW_COLORS_MATCH_CIRCUMFERENCE_CIRCLES and mg.flagCircum:
        # If showing circumference colors, then make arrows black, which is less distracting
        arrowInput.set_color('k')
        arrowOutput.set_color('k')
    else:
        # IF not showing circumference dots, then arrows are red/purple
        arrowInput.set_color(mg.INPUT_VECTOR_COLOR)
        arrowOutput.set_color(mg.OUTPUT_VECTOR_COLOR)

    if mg.matrixRowsToShow <= 1:
        # 1-D input vector
        #
        # Draw unit arrow and blue arrow for first matrix row,
        gv.ax1.draw_artist(matrixArrows[0])
        gv.ax1.draw_artist(arrowInput)
    else:
        # 2-D input matrix
        if mg.flagCircum:
            # Draw all items including circumference dots
            for p in gv.ax1.patches:
                gv.ax1.draw_artist(p)
        else:
            # Draw unit arrow and both matrix arrows but no circumference dots
            gv.ax1.draw_artist(matrixArrows[0])
            gv.ax1.draw_artist(matrixArrows[1])
            gv.ax1.draw_artist(arrowInput)

    if mg.flagShadow:
        # Draw "shadow" projections
        for v in range(0,mg.matrixRowsToShow):
            gv.ax1.draw_artist(lineNormal[v])
            gv.ax1.draw_artist(lineShadow[v])

    # Draw bottom-right graph elements, if needed
    canvas.restore_region(bg2)  # Restores static elements and erases background

    if mg.matrixRowsToShow > 1:
        arrowOutput.set_positions((0, 0), tuple(vector_output))
    else:
        arrowOutput.set_positions((0, 0), (vector_output[0], 0))

    # Draw output vectors
    if mg.flagShadow:
        # [x1, x2], [y1, y2] draws horizontal line
        lineOutputX.set_data([0, vector_output[0]], [0, 0])

        if  mg.matrixRowsToShow > 1:
            lineOutputY.set_data([vector_output[0], vector_output[0]], [0, vector_output[1]])
        else:
            lineOutputY.set_data([vector_output[0], vector_output[0]], [0, 0])
        ax2.draw_artist(lineOutputX)
        ax2.draw_artist(lineOutputY)

    # Draw purple circle patches
    if mg.flagCircum & (mg.matrixRowsToShow > 1):
        [ax2.draw_artist(p) for p in ax2.patches]
    else:
        ax2.draw_artist(arrowOutput)

    #
    plt.sca(ax2)
    plt.axis('on')

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

        if mg.flagMouseDownOnset:
            # Onset of mouse click

            # Clear flag so we don't come back
            mg.flagMouseDownOnset = False

            if mg.matrixRowsToShow == 1:
                # Adjust row one, since it's the only one showing
                mg.whichRowToAdjust = 0
            else:
                # Determine which row to adjust by
                # calculating distance from mouse cursor
                dx1 = Array1[0,0] - mg.flagX
                dy1 = Array1[0,1] - mg.flagY
                dx2 = Array1[1,0] - mg.flagX
                dy2 = Array1[1,1] - mg.flagY

                if ((dx1*dx1+dy1*dy1) > (dx2*dx2+dy2*dy2)):
                    # Mouse is farther from row 1 vector than 2, so adjust row 2
                    mg.whichRowToAdjust = 1
                else:
                    # Mouse is farther from row 2 vector than row 1, so adjust row 1
                    mg.whichRowToAdjust = 0

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
                    # User is using mouse to draw matrix vectors
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
            # If recalc flag is set, then break out of loop and also update text on circumference button
            gObjects.b_circum.SetTextVisible(mg.matrixRowsToShow > 1)
            # This is needed for button text to update
            canvas_buttons.draw()

            # Clear flag so we don't come back
            mg.flagRecalc = False
            break

        if localAnimate:
            break


    if mg.quitflag:
        break

    if mg.flagAnimate:
        currentStep = currentStep + 1
        if currentStep >= u.numsteps:
            cycles = cycles + 1
            currentStep = currentStep - stepsPerOrbit

if mg.quitflag == 0:
    plt.show()  # This will block until window is closed.
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
