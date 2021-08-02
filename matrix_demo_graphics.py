import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
import matplotlib as mpl
import pylab

import numpy as np

import global_vars as gv

import button_manager as bm

axisLimit = 2  # Coordinate limits for x-y plots

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
TEXT_IN_OUT_Y_OFFSET = 0  # Vertical space between input and output matrices

INPUT_VECTOR_COLOR = (1.0, 0, 0.0)  # Red (0, 0, 0)  # Black
OUTPUT_VECTOR_COLOR = (0.5, 0, 0.5)  # Dark purple

CIRCUMFERENCE_COLOR1 = (0.0, 0.0, 0.0)  # Black
CIRCUMFERENCE_COLOR2 = (0.8, 0.8, 0.8)  # Light grey

MATRIX_ROW1_COLOR = (0.25, 0.25, 1.00)  # Light blue
MATRIX_ROW2_COLOR = (0.25, 0.75, 0.25)  # Light green

SHADOW1_COLOR = (0, 0, 0.5)
SHADOW2_COLOR = (0, 0.35, 0)

class Settings():

    def __init__(self):
        self.quitflag = False  # When true, program will exit
        self.flagAnimate = True  # When true, graph will animate
        self.flagChangeMatrix = False  # When true, will update matrix and redraw
        self.flagCircum = False  # When true, will plot ring of red/purple dots on circumference
        self.flagRecalc = False  # When true, will redraw existing graph items
        self.flagRedrawAxes = False  # When true, will redraw existing graph axes
        self.flagShadow = True
        self.flagMouseDown = False
        self.flagMouseDownOnset = False
        self.flagX = 0  # Indicates mouse x position
        self.flagY = 0  # Indicates mouse y position
        self.matrixRowsToShow = 1
        self.whichRowToAdjust = 0
        self.keep_ortho = 0

settings = Settings()

# Create initial x-y, text, and bar plots, then save backgrounds
def create_initial_graphics(canvas):
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
    for i in range(0, 9):
        #        plt.plot([-axisLimit, axisLimit], [linex[i], linex[i]], '--', color="grey")
        #        plt.plot([linex[i], linex[i]], [-axisLimit, axisLimit], '--', color="grey")
        lines.append([(-axisLimit, linex[i]), (axisLimit, linex[i])])
        lines.append([(linex[i], -axisLimit), (linex[i], axisLimit)])

    # Create bottom-left bar plot
    plt.subplot(223)
    gv.axBar = plt.gca()
    gv.barlist = plt.bar([0, 1], [0, 0])
    gv.barlist[0].set_color('b')
    gv.barlist[1].set_color('g')
    plt.xticks([0, 1], ['Matrix row 1 * unit vector', 'Matrix row 2 * unit vector'])
    plt.ylim([-axisLimit, axisLimit])
    plt.title("Dot product output(s)")
    plt.ylabel("Dot product")
    plt.show(block=False)

    # Create bottom-right output plot with dashed circle
    plt.subplot(224)
    gv.ax2 = plt.gca()
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
    gv.bgBar = canvas.copy_from_bbox(gv.axBar.bbox)
    gv.bg1 = canvas.copy_from_bbox(gv.ax1.bbox)
    gv.bg2 = canvas.copy_from_bbox(gv.ax2.bbox)


# Mouse button press. Use this to start moving vector1 or vector2 in top-right plot
def on_mouse_press(event):
    if event.inaxes != gv.ax1:
        return

    # Left mouse press initiates dragging of matrix.
    if event.button == mpl.backend_bases.MouseButton.LEFT:
        settings.flagMouseDown = True
        settings.flagMouseDownOnset = True
        settings.flagChangeMatrix = True
        settings.flagX = event.xdata
        settings.flagY = event.ydata


def on_mouse_release(event):
    if event.inaxes != gv.ax1:
        return

    settings.flagMouseDown = False
    settings.flagChangeMatrix = False


def on_mouse_move(event):
    if event.inaxes != gv.ax1:
        return

    if settings.flagMouseDown:
        settings.flagX = event.xdata
        settings.flagY = event.ydata
        settings.flagChangeMatrix = True


def do_1_vs_2(event=None):
    settings.matrixRowsToShow = 3 - settings.matrixRowsToShow  # Toggle between 1 and 2 rows
    settings.flagRecalc = True


def do_shadow(event=None):
    settings.flagShadow = 1 - settings.flagShadow
    settings.flagRecalc = True


def do_quit(event=None):
    settings.quitflag = True


def do_animate(event=None):
    settings.flagAnimate = not settings.flagAnimate


def do_show_circle(_event=None):
    settings.flagCircum = not settings.flagCircum
    settings.flagRecalc = True


# This is only called if using matplotlib buttons. For tk buttons, see method within GraphicsObjects
def do_orthogonal(_event=None):
    settings.flagChangeMatrix = True
    settings.whichRowToAdjust = -1


def on_keydown(e):
    if e.char == ' ':
        do_animate()


# Keyboard press
# no longer used
def on_keypress(event):
    global flagChangeMatrix, whichRowToAdjust
    #    print('key: ', event.key, event.xdata, event.ydata)
    if event.key == " ":
        do_animate()


# Format a single floating point number to have 3 decimals
def fmt(n: np.float64):
    return '{:+2.3f}'.format(n)


# Format a single floating point number to have 3 decimals and brackets
def fmt_bracket(n: np.float64):
    return '[{:+2.3f}]'.format(n)


# Format a 2D vector as text inside brackets
def fmt_row(r: np.float64):
    return '[' + fmt(r[0]) + ', ' + fmt(r[1]) + ']'


#
# Create main windows and canvases for plots and buttons.
#
# Actual plots are created after this object's constructor returns, and create_initial_graphs() is called.
class GraphicsObjects:

    def __init__(self):
        global FONT_SIZE

        mpl.use('TkAgg')  # TkAgg doesn't need installing. Works well.
        #        mpl.use('Qt5Agg')  # Qt5Agg needs to be installed. Has annoying tendency to resize windows after user move

        self.backend = mpl.get_backend()
        print(
            "Matplotlib backend is: " + self.backend)  # Returns Qt5Agg after installing Qt5 ... if you don't have Qt5, I think it returns TkAgg something

        mpl.rcParams['toolbar'] = 'None'

        self.ButtonMgr = bm.ButtonManager()

        # Create row of buttons. current axis will either be 1 or 2
        self.b_animate = self.ButtonMgr.add_button('Toggle animate', do_animate)
        # self.b_shadow = self.ButtonMgr.add_button('Toggle projections\n(h)', do_shadow) # This isn't used much
        self.b_1_vs_2 = self.ButtonMgr.add_button('Toggle 1 vs 2 row matrix', do_1_vs_2)
        self.b_circum = self.ButtonMgr.add_button('Toggle Circumference', do_show_circle)

        if self.ButtonMgr.USE_TK:
            self.var_ortho = tk.IntVar()
            self.b_orthogonal = self.ButtonMgr.add_check('Keep orthogonal', self.var_ortho, self.do_orthogonal_tk)
        else:
            self.b_orthogonal = self.ButtonMgr.add_button('Make orthogonal', do_orthogonal)

        self.b_quit = self.ButtonMgr.add_button('Quit', do_quit)

        #        self.b_fix = self.ButtonMgr.add_button('Reset size', self.reset_size)

        # The toggle-circumference button starts disabled
        if self.ButtonMgr.USE_TK:
            self.b_circum.state(["disabled"])
            self.var_ortho.set(0)
        else:
            self.b_circum.SetTextVisible(False)

        # Make fig 1 the current axis again
        plt.figure(1)

        # Font was optimized for screen height of 1440 pixels. Adjust accordingly if screen is different
        FONT_SIZE = int(FONT_SIZE * self.ButtonMgr.screen_y / 1400)

        fig1 = self.ButtonMgr.fig1

        # Create text objects
        self.textObj = TextObjects(fig1)

        # Main plot windows need to respond to mouse events (for dragging vectors)
        fig1.canvas.mpl_connect('button_press_event', on_mouse_press)
        fig1.canvas.mpl_connect('button_release_event', on_mouse_release)
        fig1.canvas.mpl_connect('motion_notify_event', on_mouse_move)

        # Windows should respond to key press events
        fig1.canvas.mpl_connect('key_press_event', on_keypress)

        if self.ButtonMgr.USE_TK:
            self.ButtonMgr.root.bind("<KeyPress>", on_keydown)
        else:
            fig2 = self.ButtonMgr.fig2
            if fig2 is not None:
                # Key press events
                fig2.canvas.mpl_connect('key_press_event', on_keypress)

        plt.figure(1)

    def reset_size(self, event):
        self.ButtonMgr.set_fig1_size()

    def do_orthogonal_tk(self):
        # This will handle transient change
        settings.flagChangeMatrix = self.var_ortho.get()

        # This will keep permanent toggle, so that future changes to row0 are reflected in row1
        settings.keep_ortho = self.var_ortho.get()
        settings.whichRowToAdjust = -1


class TextObjects:
    def __init__(self, _figure):

        self.fig = _figure
        self.canvas = _figure.canvas

        # Create text plot in top left
        plt.subplot(221)
        self.ax_text = plt.gca()
        plt.axis('off')

        # Draw "*" asterisk and "=" equals sign
        self.make_ax_text(TEXT_STAR_X, TEXT_Y_COORD, '*')
        self.make_ax_text(TEXT_STAR_X + TEXT_IN_OUT_X_OFFSET, TEXT_Y_COORD - TEXT_IN_OUT_Y_OFFSET, '=')

        # Top, bottom row of matrix
        self.textObjArrayRow1 = self.make_ax_text(TEXT_INPUT_MATRIX_X, TEXT_Y_COORD + TEXT_MATRIX_ROW_Y_SPACING / 2, '',
                                                  color=MATRIX_ROW1_COLOR)
        self.textObjArrayRow2 = self.make_ax_text(TEXT_INPUT_MATRIX_X, TEXT_Y_COORD - TEXT_MATRIX_ROW_Y_SPACING / 2, '',
                                                  color=MATRIX_ROW2_COLOR)

        # Top, bottom of input vector
        self.textObjInputVector1 = self.make_ax_text(TEXT_STAR_X + TEXT_OPERATOR_X_SPACING,
                                                     TEXT_Y_COORD + TEXT_MATRIX_ROW_Y_SPACING / 2, '',
                                                     color=INPUT_VECTOR_COLOR)
        self.textObjInputVector2 = self.make_ax_text(TEXT_STAR_X + TEXT_OPERATOR_X_SPACING,
                                                     TEXT_Y_COORD - TEXT_MATRIX_ROW_Y_SPACING / 2, '',
                                                     color=INPUT_VECTOR_COLOR)

        # Top, bottom of output vector. Color is set later?
        self.textObjOutputVectorRow1 = self.make_ax_text(TEXT_STAR_X + TEXT_IN_OUT_X_OFFSET + TEXT_OPERATOR_X_SPACING,
                                                         TEXT_Y_COORD + TEXT_MATRIX_ROW_Y_SPACING / 2 - TEXT_IN_OUT_Y_OFFSET,
                                                         '')
        self.textObjOutputVectorRow2 = self.make_ax_text(TEXT_STAR_X + TEXT_IN_OUT_X_OFFSET + TEXT_OPERATOR_X_SPACING,
                                                         TEXT_Y_COORD - TEXT_MATRIX_ROW_Y_SPACING / 2 - TEXT_IN_OUT_Y_OFFSET,
                                                         '')

        self.set_row1_position()

        self.canvas.draw()  # Need this so that text will render to screen, before we capture background
        self.background = self.canvas.copy_from_bbox(self.ax_text.bbox)

    def make_ax_text(self, x, y, txt, color=None):
        return self.ax_text.text(x, y, txt, color=color, family=FONT_FAMILY, size=FONT_SIZE)

    # Shift y-coordinates of text so that text always looks centered.
    # Specifically, if showing 2 rows, then top is moved up slightly from center
    def set_row1_position(self):
        if settings.matrixRowsToShow > 1:
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
        self.textObjOutputVectorRow1.set_color(OUTPUT_VECTOR_COLOR)  # MATRIX_ROW1_COLOR)
        if elements > 1:
            self.textObjOutputVectorRow2.set_text(fmt_bracket(vector[1]))
            self.textObjOutputVectorRow2.set_color(OUTPUT_VECTOR_COLOR)  # MATRIX_ROW2_COLOR)

    def redraw(self):
        #   axText.draw_artist(axText.patch)  # Erase background
        # Restore background of text window (upper left)
        self.canvas.restore_region(self.background)  # Restores static elements and erases background
        # "draw_artist" draws new objects efficiently, without updating entire plot
        self.ax_text.draw_artist(self.textObjArrayRow1)
        self.ax_text.draw_artist(self.textObjOutputVectorRow1)
        if settings.matrixRowsToShow > 1:
            self.ax_text.draw_artist(self.textObjArrayRow2)
            self.ax_text.draw_artist(self.textObjOutputVectorRow2)
        self.ax_text.draw_artist(self.textObjInputVector1)
        self.ax_text.draw_artist(self.textObjInputVector2)

        # Now render to screen
        self.canvas.blit(self.ax_text.bbox)
