#
#  Matrix demo
#
#  Multiplies 2x2 matrix by a rotating unit vector
#

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D
import numpy as np

# My files
import matrix_demo_math as mm
import matrix_demo_graphics as mg
import global_vars as gv

# Thickness of matrix, input, and output vectors
VECTOR_THICKNESS = 30
# If true, then arrow color matches the color of circumference circles. Otherwise, remains default red/purple
ARROW_COLORS_MATCH_CIRCUMFERENCE_CIRCLES = False
#  If true, then text color matches the color of circumference circles. Otherwise, remains default red/purple
TEXT_COLORS_MATCH_CIRCUMFERENCE_CIRCLES = False

Array1 = np.array([[1.0, 0.0], [0.0, 1.0]])

stepsPerOrbit = 400  # This determines smoothness of animation
dotsPerOrbit = 40  # Number of circular patches to plot on unit circle

# Determine steps between circumference dots
u = mm.UnitCircleStuff(stepsPerOrbit, dotsPerOrbit, mg.CIRCUMFERENCE_COLOR1, mg.CIRCUMFERENCE_COLOR2)
stepsPerOrbit = u.numsteps  # This might be changed, to be an integer multiple of dotsPerOrbit
print('Total steps {:d}, circumference dots {:d}'.format(u.numsteps, u.numdots))

# Create figure, buttons, and text
gObjects = mg.GraphicsObjects()

canvas = gObjects.fig1.canvas

# Create plots, and save background bitmaps so we don't have to redraw them over and over.
# This greatly speeds up animation
mg.create_initial_graphics(canvas)

mm.quitflag = False

# Write array values with specified y-coordinate
gObjects.textObj.update_array_text(Array1)

# Add vector1 (top row of 2x2 matrix) to top-right graph
matrixArrows = [mpatches.FancyArrowPatch((0, 0), tuple(Array1[0, :]),
                                         color=mg.MATRIX_ROW1_COLOR,
                                         mutation_scale=VECTOR_THICKNESS)]  # Thickness
gv.ax1.add_patch(matrixArrows[0])

# Add vector2 (bottom row of 2x2 matrix) to top-right graph
matrixArrows.append(mpatches.FancyArrowPatch((0, 0), tuple(Array1[1, :]),
                                             color=mg.MATRIX_ROW2_COLOR,
                                             mutation_scale=VECTOR_THICKNESS))  # Thickness
gv.ax1.add_patch(matrixArrows[1])

# Generate starting points around unit circle
u.makeCircs(Array1, mg.OUTPUT_VECTOR_COLOR)

currentStep = 0
currentStepFloat = 0.0
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
gv.ax2.add_patch(arrowOutput)

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
                                         linestyle='--',  # Dashed line
                                         color=mg.SHADOW1_COLOR)))
# Normal/shadow for second row
lineNormal.append(gv.ax1.add_line(Line2D([0, 0], [1, 1],
                                         color=(0.5, 0.5, 0.5),
                                         linestyle=':')))  # Dotted line
lineShadow.append(gv.ax1.add_line(Line2D([0, 0], [1, 1],
                                         linewidth=3,
                                         linestyle='--',  # Dashed line
                                         color=mg.SHADOW2_COLOR)))

# Add shadow lines to output axis
lineOutputX = gv.ax2.add_line(Line2D([0, 0], [1, 1],
                                     linewidth=3,
                                     color=mg.SHADOW1_COLOR))
lineOutputY = gv.ax2.add_line(Line2D([0, 0], [1, 1],
                                     linewidth=3,
                                     color=mg.SHADOW2_COLOR))

# Need to call this the first time or else objects won't draw later
plt.pause(0.01)
localRedrawAxes = False
localAnimate = mg.settings.flagAnimate  # Need local copy of this flag so we can detect when it changes state

while mg.settings.quitflag == 0:
    # V1 is "input" vector in top-right plot
    vector_input = [u.unitVectorX[currentStep], u.unitVectorY[currentStep]]

    # V2 is transformed vector in lower-right plot
    vector_output = np.matmul(Array1, vector_input)

    for v in range(0, 2):
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

    # Update input vector text
    if mg.settings.flagCircum:
        # Use rainbow color for text
        if TEXT_COLORS_MATCH_CIRCUMFERENCE_CIRCLES:
            gObjects.textObj.update_input_vector(vector_input, u.stepColorList[currentStep])
        else:
            gObjects.textObj.update_input_vector(vector_input, mg.INPUT_VECTOR_COLOR)
    else:
        # Input text color matches vector
        gObjects.textObj.update_input_vector(vector_input, mg.INPUT_VECTOR_COLOR)

    # Update output vector text
    gObjects.textObj.update_output_vector(vector_output, mg.settings.matrixRowsToShow)

    # Draw text
    gObjects.textObj.redraw()

    # Bar chart
    canvas.restore_region(gv.bgBar)  # Restores static elements and erases background
    gv.barlist[0].set_height(vector_output[0])
    gv.axBar.draw_artist(gv.barlist[0])

    if mg.settings.matrixRowsToShow > 1:
        gv.barlist[1].set_height(vector_output[1])
        gv.axBar.draw_artist(gv.barlist[1])
    else:
        gv.barlist[1].set_height(0)

    # Now render bar graph to screen
    canvas.blit(gv.axBar.bbox)

    # Draw next circumference dot on input and output x-y plots
    if currentStep % u.stepsPerDot == 0 and cycles == 0:
        currentDot = int(currentStep / u.stepsPerDot)

        # Add new input dot
        circ = u.patchList1[currentDot]
        gv.ax1.add_patch(circ)
        gv.ax1.draw_artist(circ)

        # Add new output dot
        circ = u.patchList2[currentDot]
        gv.ax2.add_patch(circ)
        gv.ax2.draw_artist(circ)

    # Draw top-right "INPUT VECTOR" graph
    canvas.restore_region(gv.bg1)  # Restores static elements and erases background
    arrowInput.set_positions((0, 0), tuple(vector_input))

    if ARROW_COLORS_MATCH_CIRCUMFERENCE_CIRCLES and mg.settings.flagCircum:
        # If showing circumference colors, then make arrows black, which is less distracting
        arrowInput.set_color('k')
        arrowOutput.set_color('k')
    else:
        # IF not showing circumference dots, then arrows are red/purple
        arrowInput.set_color(mg.INPUT_VECTOR_COLOR)
        arrowOutput.set_color(mg.OUTPUT_VECTOR_COLOR)

    if mg.settings.matrixRowsToShow <= 1:
        # 1-D input vector
        #
        # Draw unit arrow and blue arrow for first matrix row,
        gv.ax1.draw_artist(matrixArrows[0])
        gv.ax1.draw_artist(arrowInput)
    else:
        # 2-D input matrix
        if mg.settings.flagCircum:
            # Draw all items including circumference dots
            for p in gv.ax1.patches:
                gv.ax1.draw_artist(p)
        else:
            # Draw unit arrow and both matrix arrows but no circumference dots
            gv.ax1.draw_artist(matrixArrows[0])
            gv.ax1.draw_artist(matrixArrows[1])
            gv.ax1.draw_artist(arrowInput)

    if mg.settings.flagShadow:
        # Draw "shadow" projections
        for v in range(0, mg.settings.matrixRowsToShow):
            gv.ax1.draw_artist(lineNormal[v])
            gv.ax1.draw_artist(lineShadow[v])

    # Draw bottom-right graph elements, if needed
    canvas.restore_region(gv.bg2)  # Restores static elements and erases background

    if mg.settings.matrixRowsToShow > 1:
        arrowOutput.set_positions((0, 0), tuple(vector_output))
        arrowOutput.set_arrowstyle("simple", head_length=min(sum([abs(x) for x in vector_output]), 0.5))
    else:
        # Output (purple) arrow is horizontal
        arrowOutput.set_positions((0, 0), (vector_output[0], 0))
        arrowOutput.set_arrowstyle("simple", head_length=min(abs(vector_output[0]), 0.5))

    # Draw output vectors
    if mg.settings.flagShadow:
        # [x1, x2], [y1, y2] draws horizontal line
        lineOutputX.set_data([0, vector_output[0]], [0, 0])

        if mg.settings.matrixRowsToShow > 1:
            lineOutputY.set_data([vector_output[0], vector_output[0]], [0, vector_output[1]])
        else:
            lineOutputY.set_data([vector_output[0], vector_output[0]], [0, 0])
        gv.ax2.draw_artist(lineOutputX)
        gv.ax2.draw_artist(lineOutputY)

    # Draw purple circle patches
    if mg.settings.flagCircum & (mg.settings.matrixRowsToShow > 1):
        [gv.ax2.draw_artist(p) for p in gv.ax2.patches]
    else:
        gv.ax2.draw_artist(arrowOutput)

    #
    plt.sca(gv.ax2)
    plt.axis('on')

    # Render to screen
    canvas.blit(gv.ax1.bbox)
    canvas.blit(gv.ax2.bbox)

    if localRedrawAxes:
        plt.pause(0.01)  # Need this to redraw entire plot axis when output panel (lower right) is togged on/off
        localRedrawAxes = False

    while not mg.settings.quitflag:

        # Need this to update graphics, and respond to GUI events, e.g. button presses.
        canvas.flush_events()

        if localAnimate and not mg.settings.flagAnimate:
            # Global flag just switched off. Turn off local animation, but also break so we run one more loop
            localAnimate = False
            break
        if not localAnimate and mg.settings.flagAnimate:
            # Global flag just switched on. Copy state to local flag
            localAnimate = True

        if mg.settings.flagMouseDownOnset:
            # Onset of mouse click

            # Clear flag so we don't come back
            mg.settings.flagMouseDownOnset = False

            if mg.settings.matrixRowsToShow == 1:
                # Adjust row one, since it's the only one showing
                mg.settings.whichRowToAdjust = 0
            else:
                # Determine which row to adjust by
                # calculating distance from mouse cursor
                dx1 = Array1[0, 0] - mg.settings.flagX
                dy1 = Array1[0, 1] - mg.settings.flagY
                dx2 = Array1[1, 0] - mg.settings.flagX
                dy2 = Array1[1, 1] - mg.settings.flagY

                if (dx1 * dx1 + dy1 * dy1) > (dx2 * dx2 + dy2 * dy2):
                    # Mouse is farther from row 1 vector than 2, so adjust row 2
                    mg.settings.whichRowToAdjust = 1
                else:
                    # Mouse is farther from row 2 vector than row 1, so adjust row 1
                    mg.settings.whichRowToAdjust = 0

        if mg.settings.flagChangeMatrix:
            mg.settings.flagRecalc = False
            mg.settings.flagChangeMatrix = False
            r = mg.settings.whichRowToAdjust
            if r == -1:
                # Force row1 to be orthogonal to row0
                Array1[1, 0] = -Array1[0, 1]
                Array1[1, 1] = Array1[0, 0]
                #                matrixArrows[0].set_positions((0, 0), tuple(Array1[0, :]))
                matrixArrows[1].set_positions((0, 0), tuple(Array1[1, :]))
            elif r == -2:
                # Force unit vector ... currently not used, but can resurrect
                m1 = np.linalg.norm(Array1[0, :])
                m2 = np.linalg.norm(Array1[1, :])
                Array1[0, :] = Array1[0, :] / m1
                Array1[1, :] = Array1[1, :] / m2
                matrixArrows[0].set_positions((0, 0), tuple(Array1[0, :]))
                matrixArrows[1].set_positions((0, 0), tuple(Array1[1, :]))
            #                u.updateCircs(Array1)
            elif mg.settings.flagX is not None and mg.settings.flagY is not None:
                # Because x, y won't be valid if mouse went out of bounds
                # User is using mouse to draw matrix vectors
                Array1[r, 0] = mg.settings.flagX
                Array1[r, 1] = mg.settings.flagY

                if mg.settings.keep_ortho:
                    # Force other arrow to be 90 degrees counterclockwise from the one being adjusted
                    target = 1 - r
                    Array1[target, 0] = -Array1[r, 1]
                    Array1[target, 1] = Array1[r, 0]
                    matrixArrows[target].set_positions((0, 0), tuple(Array1[target, :]))

                matrixArrows[r].set_positions((0, 0), tuple(Array1[r, :]))
            else:
                # Nothing was changed after all.
                break

            u.updateCircs(Array1)
            gObjects.textObj.update_array_text(Array1)  # Will this take effect without calling redraw()???

            break

        if mg.settings.flagRedrawAxes:
            mg.settings.flagRedrawAxes = False
            localRedrawAxes = True
            break

        if mg.settings.flagRecalc:
            # If recalc flag is set, then break out of loop and also update text on circumference button
            if mg.settings.matrixRowsToShow > 1:
                gObjects.b_circum.state(["!disabled"])
            else:
                gObjects.b_circum.state(["disabled"])

            # Clear flag so we don't come back
            mg.settings.flagRecalc = False
            break

        if localAnimate:
            break

    if mg.settings.quitflag:
        break

    if mg.settings.flagAnimate:
        currentStepFloat = currentStepFloat + mg.settings.animation_speed / 25

        if currentStepFloat >= u.numsteps:
            cycles = cycles + 1
            currentStepFloat = currentStepFloat - stepsPerOrbit

        currentStep = int(currentStepFloat)

if mg.settings.quitflag == 0:
    plt.show()  # This will block until window is closed.
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
