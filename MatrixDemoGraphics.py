import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.widgets import Button
import numpy as np

import global_vars as gv

# Button dimensions
BUTTON_WIDTH = 0.1
BUTTON_HEIGHT = 0.03  # Above about 0.1, buttons disappear - presumably they collide with graphs?
BUTTON_SPACING_X = BUTTON_WIDTH + 0.01
BUTTON_Y_COORD = 0.95

# Font
FONT_FAMILY = 'monospace'
FONT_SIZE = 16

# Text coordinates, horizontal
TEXT_INPUT_MATRIX_X = 0
TEXT_STAR_X = TEXT_INPUT_MATRIX_X + 0.34 * FONT_SIZE / 12
TEXT_OPERATOR_X_SPACING = 0.05
TEXT_IN_OUT_X_OFFSET = 0.28  # Vertical space between input and output matrices

# Text coordinates, vertical
TEXT_Y_COORD = 0.7  # Height of input matrix text above horizontal axis
TEXT_MATRIX_ROW_Y_SPACING = 0.08  # Vertical space between rows of input matrix
TEXT_IN_OUT_Y_OFFSET = 0     # Vertical space between input and output matrices

INPUT_VECTOR_COLOR  = (1.0, 0, 0.0)  # Red (0, 0, 0)  # Black
OUTPUT_VECTOR_COLOR = (0.5, 0, 0.5)  # Dark purple

CIRCUMFERENCE_COLOR1 = (0.0, 0.0, 0.0)  # Black
CIRCUMFERENCE_COLOR2 = (0.8, 0.8, 0.8)  # Light grey

MATRIX_ROW1_COLOR = (0.25, 0.25, 1.00)  # Light blue
MATRIX_ROW2_COLOR = (0.25, 0.75, 0.25)  # Light green

SHADOW1_COLOR = (0, 0, 0.5)
SHADOW2_COLOR = (0, 0.35, 0)

quitflag = False  # When true, program will exit
flagAnimate = False  # When true, graph will animate
flagChangeMatrix = False  # When true, will update matrix and redraw
flagCircum = False  # When true, will plot ring of red/purple dots on circumference
flagRecalc = False  # When true, will redraw existing graph items
flagRedrawAxes = False  # When true, will redraw existing graph axes
flagShadow = False
flagX = 0  # Indicates mouse x position
flagY = 0  # Indicates mouse y position
matrixRowsToShow = 1
flagShow4 = True
whichRowToAdjust = 0

flagMouseDown = False


# Mouse button press. Use this to start moving vector1 or vector2 in top-right plot
def on_mouse_press(event):
    if event.inaxes != gv.ax1:
        return
    global flagX, flagY, flagMouseDown, whichRowToAdjust, flagChangeMatrix
    if event.button == mpl.backend_bases.MouseButton.LEFT:
        flagMouseDown = True
        flagChangeMatrix = True
        whichRowToAdjust = 0
    if event.button == mpl.backend_bases.MouseButton.RIGHT:
        flagMouseDown = True
        flagChangeMatrix = True
        whichRowToAdjust = 1
    flagX = event.xdata
    flagY = event.ydata


def on_mouse_release(event):
    if event.inaxes != gv.ax1:
        return
    global flagMouseDown, flagChangeMatrix
    flagMouseDown = False
    flagChangeMatrix = False


def on_mouse_move(event):
    if event.inaxes != gv.ax1:
        return
    global flagMouseDown, flagRecalc, flagX, flagY, flagChangeMatrix
    if flagMouseDown:
        flagX = event.xdata
        flagY = event.ydata
        flagChangeMatrix = True


def do_1_vs_2(event=None):
    global matrixRowsToShow, flagRecalc
    matrixRowsToShow = 3 - matrixRowsToShow  # Toggle between 1 and 2 rows
    flagRecalc = True

def do_shadow(event=None):
    global flagShadow, flagRecalc
    flagShadow = 1 - flagShadow
    flagRecalc = True

def do_quit(event=None):
    global quitflag
    quitflag = True


def do_animate(event=None):
    global flagAnimate
    flagAnimate = not flagAnimate


def do_show_circle(event=None):
    global flagCircum, flagShow4
    if flagShow4:
        flagCircum = not flagCircum

# Toggles flagShow4 flag, then triggers recalculation
# This only applies to 2D matrices
def do_toggle_output(event=None):
    global matrixRowsToShow, flagRecalc, flagShow4, flagRedrawAxes, flagCircum
    if matrixRowsToShow > 1:
        flagRecalc = True
        flagShow4 = not flagShow4
        if not flagShow4:
            flagCircum = False
        flagRedrawAxes = True
    else:
        flagRecalc = False
        flagShow4 = False
        flagRedrawAxes = False
        flagCircum = False

# Keyboard press
def on_keypress(event):
    global flagChangeMatrix, whichRowToAdjust
    #    print('key: ', event.key, event.xdata, event.ydata)
    if event.key == "x":
        do_quit()
    if event.key == "a" or event.key == " ":
        do_animate()
    if event.key == "c":
        do_show_circle()
    if event.key == "h":
        do_shadow()
    if event.key == "u":
        flagChangeMatrix = True
        whichRowToAdjust = -1
    if event.key == "2":
        do_1_vs_2()
    if event.key == "4":
        do_toggle_output()


# Format a single floating point number to have 3 digits after decimal
def fmt(n: np.float64):
    return '{:+2.3f}'.format(n)

def fmt_bracket(n: np.float64):
    return '[{:+2.3f}]'.format(n)

# Format a 2D vector as text inside brackets
def fmt_row(r: np.float64):
    return '[' + fmt(r[0]) + ', ' + fmt(r[1]) + ']'


# Handle buttons and text objects. This does NOT manage the plots.
# Plots are created after this object's constructor returns, and create_initial_graphs() is called.
class GraphicsObjects:

    def __init__(self):

        mpl.use('TkAgg')   # Qt5Agg might also be available, but doesn't seem to behave as nicely

        self.backend = mpl.get_backend()
        print("Matplotlib backend is: " + self.backend) # Returns Qt5Agg after installing Qt5 ... if you don't have Qt5, I think it returns TkAgg something

        # Create figure
        fig = plt.figure()
        window = plt.get_current_fig_manager().window
        dpi = fig.dpi

        if self.backend == "Qt5Agg":
            # Need a hack to get screen size. Temporarily make a full-screen window, get its size, then later set "real" size
            window.showMaximized()  # Make window fullscreen
            plt.pause(.001)  # Draw items to screen so we can get size
            screen_x, screen_y = fig.get_size_inches() * fig.dpi  # size in pixels
        else:
            # window.state('zoomed')  # Make window fullscreen, for TkAgg
            screen_x, screen_y = window.wm_maxsize() # Get full scren monitor coordinates for TkAgg. Doesn't work under Qt5Agg

#        window.state('zoomed')
        screen_y = screen_y - 50  # Subtract a small amount or else the toolbar at bottom will mess things up.
        fig.set_size_inches(screen_y / dpi, screen_y / dpi)  # Make square window at max size, but bar at bottom messes up size

        canvas = fig.canvas
        canvas.mpl_connect('button_press_event', on_mouse_press)
        canvas.mpl_connect('button_release_event', on_mouse_release)
        canvas.mpl_connect('key_press_event', on_keypress)
        canvas.mpl_connect('motion_notify_event', on_mouse_move)
        self.fig = fig
        self.canvas = canvas

        self.textObj = TextObjects(self.canvas, self.fig)

        # Test button overlaid on existing graph. Button technically works (responds to mouse clicks),
        # but keeps getting hidden by plot axes. Is there any way to keep button on top?
        #
        # ax_testbutton = self.fig.add_subplot(20, 10, 191)
        # b_testbutton = Button(ax_testbutton, 'Test')

        # Creating new axes puts them below main graphs. Is this behavior guaranteed?

        # Create one new axis for each new button
        position = 0
        ax_animate = plt.axes([0.15 + BUTTON_SPACING_X * position, BUTTON_Y_COORD, BUTTON_WIDTH, BUTTON_HEIGHT])
        self.b_animate = Button(ax_animate, 'Toggle animate (a)')
        self.b_animate.on_clicked(do_animate)

        position = position + 1
        ax_shadow = plt.axes([0.15 + BUTTON_SPACING_X * position, BUTTON_Y_COORD, BUTTON_WIDTH, BUTTON_HEIGHT])
        self.b_shadow = Button(ax_shadow, 'Toggle shadows (h)')
        self.b_shadow.on_clicked(do_shadow)

        position = position + 1
        ax_1_vs_2 = plt.axes([0.15 + BUTTON_SPACING_X * position, BUTTON_Y_COORD, BUTTON_WIDTH, BUTTON_HEIGHT])
        self.b_1_vs_2 = Button(ax_1_vs_2, '1/2-row matrix (2)')
        self.b_1_vs_2.on_clicked(do_1_vs_2)

        position = position + 1
        ax_output = plt.axes([0.15 + BUTTON_SPACING_X * position, BUTTON_Y_COORD, BUTTON_WIDTH, BUTTON_HEIGHT])
        self.b_output = Button(ax_output, 'Toggle output (4)')
        self.b_output.on_clicked(do_toggle_output)

        position = position + 1
        ax_circum = plt.axes([0.15 + BUTTON_SPACING_X * position, BUTTON_Y_COORD, BUTTON_WIDTH, BUTTON_HEIGHT])
        self.b_circum = Button(ax_circum, 'Show circle (c)')
        self.b_circum.on_clicked(do_show_circle)

        ax_quit = plt.axes([0.75, BUTTON_Y_COORD, BUTTON_WIDTH, BUTTON_HEIGHT])
        self.b_quit = Button(ax_quit, 'Quit (x)')
        self.b_quit.on_clicked(do_quit)


class TextObjects:
    def __init__(self, _canvas, _figure):
        self.canvas = _canvas
        self.fig = _figure

        # Create text plot in top left
        plt.subplot(221)
        self.ax_text = plt.gca()
        plt.axis('off')

        # Draw "*" asterisk and "=" equals sign
        self.ax_text.text(TEXT_STAR_X, TEXT_Y_COORD, '*',
                          family=FONT_FAMILY,
                          size=FONT_SIZE
                          )
        self.ax_text.text(TEXT_STAR_X + TEXT_IN_OUT_X_OFFSET, TEXT_Y_COORD - TEXT_IN_OUT_Y_OFFSET, '=',
                          family=FONT_FAMILY,
                          size=FONT_SIZE
                          )

        # Top row of matrix
        self.textObjArrayRow1 = self.ax_text.text(
            TEXT_INPUT_MATRIX_X,
            TEXT_Y_COORD + TEXT_MATRIX_ROW_Y_SPACING / 2,
            '',
            color=MATRIX_ROW1_COLOR,
            family=FONT_FAMILY,
            size=FONT_SIZE)
        # Bottom row of matrix
        self.textObjArrayRow2 = self.ax_text.text(
            TEXT_INPUT_MATRIX_X,
            TEXT_Y_COORD - TEXT_MATRIX_ROW_Y_SPACING / 2,
            '',
            color=MATRIX_ROW2_COLOR,
            family=FONT_FAMILY,
            size=FONT_SIZE)
        # Top number in input vector
        self.textObjInputVector1 = self.ax_text.text(
            TEXT_STAR_X + TEXT_OPERATOR_X_SPACING,
            TEXT_Y_COORD + TEXT_MATRIX_ROW_Y_SPACING / 2,
            '',
            color=INPUT_VECTOR_COLOR,
            family=FONT_FAMILY,
            size=FONT_SIZE
        )
        # Bottom number in input vector
        self.textObjInputVector2 = self.ax_text.text(
            TEXT_STAR_X + TEXT_OPERATOR_X_SPACING,
            TEXT_Y_COORD - TEXT_MATRIX_ROW_Y_SPACING / 2,
            '',
            color=INPUT_VECTOR_COLOR,
            family=FONT_FAMILY,
            size=FONT_SIZE
        )
        # Top number in output vector
        self.textObjOutputVectorRow1 = self.ax_text.text(
            TEXT_STAR_X + TEXT_IN_OUT_X_OFFSET + TEXT_OPERATOR_X_SPACING,
            TEXT_Y_COORD + TEXT_MATRIX_ROW_Y_SPACING / 2 - TEXT_IN_OUT_Y_OFFSET,
            '',
            color=MATRIX_ROW1_COLOR,
            family=FONT_FAMILY,
            size=FONT_SIZE
        )
        # Bottom number in output vector
        self.textObjOutputVectorRow2 = self.ax_text.text(
            TEXT_STAR_X + TEXT_IN_OUT_X_OFFSET + TEXT_OPERATOR_X_SPACING,
            TEXT_Y_COORD - TEXT_MATRIX_ROW_Y_SPACING / 2 - TEXT_IN_OUT_Y_OFFSET,
            '',
            color=MATRIX_ROW2_COLOR,
            family=FONT_FAMILY,
            size=FONT_SIZE
        )

        self.canvas.draw()  # Need this so that text will render to screen, before we capture background
        self.background = self.canvas.copy_from_bbox(self.ax_text.bbox)

    # Write 2x2 array values
    def update_array_text(self, array):
        self.textObjArrayRow1.set_text(fmt_row(array[0, :]))
        self.textObjArrayRow2.set_text(fmt_row(array[1, :]))

    # Write input vector values
    def update_input_vector(self, vector, new_color=INPUT_VECTOR_COLOR):
        self.textObjInputVector1.set_text(fmt_bracket(vector[0]))
        self.textObjInputVector1.set_color(new_color)
        self.textObjInputVector2.set_text(fmt_bracket(vector[1]))
        self.textObjInputVector2.set_color(new_color)

    # Write output vector values
    def update_output_vector(self, vector, elements, new_color=OUTPUT_VECTOR_COLOR):
        self.textObjOutputVectorRow1.set_text(fmt_bracket(vector[0]))
        self.textObjOutputVectorRow1.set_color(MATRIX_ROW1_COLOR)
        if elements > 1:
            self.textObjOutputVectorRow2.set_text(fmt_bracket(vector[1]))
            self.textObjOutputVectorRow2.set_color(MATRIX_ROW2_COLOR)

    def redraw(self):
        #   axText.draw_artist(axText.patch)  # Erase background
        # Restore background of text window (upper left)
        self.canvas.restore_region(self.background)  # Restores static elements and erases background
        # "draw_artist" draws new objects efficiently, without updating entire plot
        self.ax_text.draw_artist(self.textObjArrayRow1)
        self.ax_text.draw_artist(self.textObjOutputVectorRow1)
        if matrixRowsToShow > 1:
            self.ax_text.draw_artist(self.textObjArrayRow2)
            self.ax_text.draw_artist(self.textObjOutputVectorRow2)
        self.ax_text.draw_artist(self.textObjInputVector1)
        self.ax_text.draw_artist(self.textObjInputVector2)

        # Now render to screen
        self.canvas.blit(self.ax_text.bbox)
