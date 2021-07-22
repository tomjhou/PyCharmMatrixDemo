import matplotlib.pyplot as plt
import matplotlib as mpl
import pylab
from matplotlib.widgets import Button
import numpy as np

import global_vars as gv

USE_SEPARATE_BUTTON_PANEL = True   # Put buttons on separate window
USE_VERTICAL_BUTTON_PANEL = True   # Stack buttons vertically instead of horizontally
BUTTON_GAP = 0.01                  # Space (as fraction of screen) between buttons

if USE_SEPARATE_BUTTON_PANEL:
    # Button dimensions are all expressed as fraction of window size
    if USE_VERTICAL_BUTTON_PANEL:
        BUTTON_Y_COORD = 0.8
        BUTTON_HEIGHT = 0.15
        BUTTON_WIDTH = 0.8
        BUTTON_X_START = 0.1
    else:
        BUTTON_Y_COORD = 0.1 # 0.95
        BUTTON_HEIGHT = 0.8 # 0.03  # Above about 0.1, buttons disappear - presumably they collide with graphs?
        BUTTON_WIDTH = 0.2
        BUTTON_X_START = 0.05
else:
    # Place buttons at top of plot window. This gives fewer windows, but
    # causes annoying flicker in plots when mouse cursor moves over button.
    # Button dimensions are all expressed as fraction of window size
    BUTTON_WIDTH = 0.1
    BUTTON_HEIGHT = 0.03  # When > 0.1, buttons disappear - presumably covered by graphs
    BUTTON_Y_COORD = 0.95 # Buttons are near top of screen
    BUTTON_X_START = 0.15


# Font
FONT_FAMILY = 'monospace'
# This will be scaled to screen size once that is determined
FONT_SIZE = 15

# Text coordinates, horizontal
TEXT_INPUT_MATRIX_X = 0
TEXT_STAR_X = TEXT_INPUT_MATRIX_X + 0.34 * FONT_SIZE / 12
TEXT_OPERATOR_X_SPACING = 0.05
TEXT_IN_OUT_X_OFFSET = 0.27  # Horizontal space between input and output text

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
flagAnimate = True  # When true, graph will animate
flagChangeMatrix = False  # When true, will update matrix and redraw
flagCircum = False  # When true, will plot ring of red/purple dots on circumference
flagRecalc = False  # When true, will redraw existing graph items
flagRedrawAxes = False  # When true, will redraw existing graph axes
flagShadow = True
flagMouseDown = False
flagMouseDownOnset = False
flagX = 0  # Indicates mouse x position
flagY = 0  # Indicates mouse y position
matrixRowsToShow = 1
whichRowToAdjust = 0


# Mouse button press. Use this to start moving vector1 or vector2 in top-right plot
def on_mouse_press(event):
    if event.inaxes != gv.ax1:
        return
    global flagX, flagY, flagMouseDown, flagMouseDownOnset, whichRowToAdjust, flagChangeMatrix

    # Left mouse press initiates dragging of matrix.
    if event.button == mpl.backend_bases.MouseButton.LEFT:
        flagMouseDown = True
        flagMouseDownOnset = True
        flagChangeMatrix = True
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
    flagCircum = not flagCircum


# Keyboard press
def on_keypress(event):
    global flagChangeMatrix, whichRowToAdjust
    #    print('key: ', event.key, event.xdata, event.ydata)
    if event.key == "x":
        do_quit()
    if event.key == " ":
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


# Format a single floating point number to have 3 decimals
def fmt(n: np.float64):
    return '{:+2.3f}'.format(n)


# Format a single floating point number to have 3 decimals and brackets
def fmt_bracket(n: np.float64):
    return '[{:+2.3f}]'.format(n)


# Format a 2D vector as text inside brackets
def fmt_row(r: np.float64):
    return '[' + fmt(r[0]) + ', ' + fmt(r[1]) + ']'


# Implements a Button that can be disabled by hiding text
# I would have preferred to grey it out, but this is much easier to implement
class Button2(Button):
    """
    """

    def __init__(self, ax, label, on_clicked_function = None, image=None,
                 color='0.85', hovercolor='0.95'):
        """
        """
        Button.__init__(self, ax, label, image, color, hovercolor)

        if on_clicked_function != None:
            self.on_clicked(on_clicked_function)

        self.label_text = label

    def SetTextVisible(self, vis):
        if vis:
            self.label.set_text(self.label_text)
            self.set_active(True)
        else:
            self.label.set_text("---")
            self.set_active(False)

# Handle buttons and text objects. This does NOT manage the plots.
# Plots are created after this object's constructor returns, and create_initial_graphs() is called.
class GraphicsObjects:

    def __init__(self):
        global FONT_SIZE

#        mpl.use('TkAgg')   # TkAgg doesn't need installing, and is fast, but has annoying flicker.
        mpl.use('Qt5Agg')  # Qt5Agg needs to be installed, has slightly less flicker, but may be slower on some machines.

        self.backend = mpl.get_backend()
        print("Matplotlib backend is: " + self.backend) # Returns Qt5Agg after installing Qt5 ... if you don't have Qt5, I think it returns TkAgg something

        mpl.rcParams['toolbar'] = 'None'

        # Create figure 1
        fig = plt.figure(1)
        window = plt.get_current_fig_manager().window
        self.dpi = fig.dpi

        if self.backend == "Qt5Agg":
            # Hack to get screen size. Temporarily make a full-screen window, get size, then later set "real" size
            window.showMaximized()  # Make fullscreen
            plt.pause(.001)  # Draw items to screen so we can get size
            screen_x, screen_y = fig.get_size_inches() * fig.dpi  # size in pixels
        elif self.backend == "TkAgg":
            screen_x, screen_y = window.wm_maxsize() # This works for TkAgg, but not Qt5Agg
        else:
            print("Unsupported backend " + self.backend)

        screen_y_adj = int(screen_y * .95)  # Reduce height about 5% so we don't overlap windows taskbar
        fig.set_size_inches(screen_y_adj / self.dpi, screen_y_adj / self.dpi)  # Make square window at max size

        canvas = fig.canvas
#        canvas.manager.window.wm_geometry("%dx%d" % (screen_y,screen_y))
        self.fig = fig
        self.canvas = canvas

        # Font was optimized for screen height of 1440 pixels. Adjust accordingly if screen is different
        FONT_SIZE = int(FONT_SIZE * screen_y / 1400)
        # Create text objects
        self.textObj = TextObjects(self.canvas, self.fig)
        canvas.mpl_connect('key_press_event', on_keypress)
        canvas.mpl_connect('button_press_event', on_mouse_press)
        canvas.mpl_connect('button_release_event', on_mouse_release)
        canvas.mpl_connect('motion_notify_event', on_mouse_move)

        if USE_SEPARATE_BUTTON_PANEL:
            # Buttons on plot window cause annoying flicker whenever mouse moves over button
            # (even if not clicked). Solve this by putting buttons on their own window

            # Create figure 2 with buttons
            fig2 = plt.figure(2)

            if USE_VERTICAL_BUTTON_PANEL:
                # Stack buttons in vertical column - need tall narrow window
                fig2.set_size_inches(screen_y_adj / self.dpi / 5, screen_y_adj / self.dpi / 2)
                # Move plot window to the right to avoid overlapping buttons
                self.move_window(canvas, screen_y_adj * .3, 0)
            else:
                # Make short wide button window
                fig2.set_size_inches(screen_y_adj / self.dpi / 2, screen_y_adj / self.dpi / 15 )
                # Move plot window to the right to avoid overlapping buttons
                self.move_window(canvas, screen_y_adj * .6, 0)

            self.canvas2 = fig2.canvas
            # Put button window at top left of screen
            self.move_window(self.canvas2, 25, 25)
            self.canvas2.mpl_connect('key_press_event', on_keypress)

        self.buttonX = BUTTON_X_START
        self.buttonY = BUTTON_Y_COORD

        # Create row of buttons
        self.b_animate = Button2(self.next_button_axis(), 'Toggle animate\n(space bar)', do_animate)
        #self.b_shadow = Button2(self.next_button_axis(), 'Toggle projections\n(h)', do_shadow) # This isn't used much
        self.b_1_vs_2 = Button2(self.next_button_axis(), 'Toggle 1 vs 2 row matrix\n (2)', do_1_vs_2)
        self.b_circum = Button2(self.next_button_axis(), 'Toggle Circumference\n (c)', do_show_circle)
        self.b_circum.SetTextVisible(False) # The toggle-circumference button starts disabled
        self.b_quit = Button2(self.next_button_axis(), 'Quit\n(x)', do_quit)

        plt.figure(1)

    def move_window(self, canvas, x, y): # x and y are in pixels

        if self.backend == "Qt5Agg":
            geom = canvas.manager.window.geometry()
            x1,y1,dx,dy = geom.getRect()
            canvas.manager.window.setGeometry(x , y + 50, dx, dy)
        elif self.backend == "TkAgg":
            canvas.manager.window.wm_geometry("+%d+%d" % (x, y))
        else:
            print("Unsupported backend " + self.backend)


    def next_button_axis(self):
        # Generate axes for the next button in series (either horizontal or vertical row)
        ax = plt.axes([self.buttonX, self.buttonY, BUTTON_WIDTH, BUTTON_HEIGHT])

        # Increment coordinates in preparation for next call
        if USE_VERTICAL_BUTTON_PANEL:
            self.buttonY = self.buttonY - BUTTON_HEIGHT - BUTTON_GAP
        else:
            self.buttonX = self.buttonX + BUTTON_GAP

        return ax

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

        self.set_row1_position()

        self.canvas.draw()  # Need this so that text will render to screen, before we capture background
        self.background = self.canvas.copy_from_bbox(self.ax_text.bbox)

    # Shift y-coordinates of text so that text always looks centered.
    # Specifically, if showing 2 rows, then top is moved up slightly from center
    def set_row1_position(self):
        if matrixRowsToShow > 1:
            self.textObjArrayRow1.set_y(TEXT_Y_COORD + TEXT_MATRIX_ROW_Y_SPACING / 2 - TEXT_IN_OUT_Y_OFFSET)
            self.textObjOutputVectorRow1.set_y(TEXT_Y_COORD + TEXT_MATRIX_ROW_Y_SPACING / 2 - TEXT_IN_OUT_Y_OFFSET)
        else:
            self.textObjArrayRow1.set_y(TEXT_Y_COORD - TEXT_IN_OUT_Y_OFFSET)
            self.textObjOutputVectorRow1.set_y(TEXT_Y_COORD - TEXT_IN_OUT_Y_OFFSET)

    # Write 2x2 array values
    def update_array_text(self, array):
        self.set_row1_position()
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
        self.set_row1_position()
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
