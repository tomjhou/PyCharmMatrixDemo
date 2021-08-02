import tkinter as tk
from tkinter import ttk

import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.widgets import Button

class ButtonManager:

    def __init__(self, _is_separate = True):

        self.USE_TK = True

        if self.USE_TK:
            root = tk.Tk()
            self.root = root
            root.title(string="Choose")
            frame1 = tk.Frame(root, highlightbackground="black", highlightthickness=1, relief="flat", borderwidth=5)
            frame1.pack(side=tk.TOP, fill=tk.BOTH, padx=20, pady=20)
            root.geometry("+%d+%d" % (5, 5))
        else:
            self.USE_SEPARATE_BUTTON_PANEL = _is_separate   # Put buttons on separate window
            self.BUTTON_GAP = 0.01                  # Space (as fraction of screen) between buttons

            if self.USE_SEPARATE_BUTTON_PANEL:
                # Button dimensions are all expressed as fraction of window size
                self.BUTTON_Y_COORD = 0.8
                self.BUTTON_HEIGHT = 0.15
                self.BUTTON_WIDTH = 0.8
                self.BUTTON_X_START = 0.1
            else:
                # Place buttons at top of plot window. This gives fewer windows, but
                # causes annoying flicker in plots when mouse cursor moves over button.
                # Button dimensions are all expressed as fraction of window size
                self.BUTTON_WIDTH = 0.1
                self.BUTTON_HEIGHT = 0.03   # When > 0.1, buttons disappear - presumably covered by graphs
                self.BUTTON_Y_COORD = 0.95  # Buttons are near top of screen
                self.BUTTON_X_START = 0.15

            self.buttonX = self.BUTTON_X_START
            self.buttonY = self.BUTTON_Y_COORD

        # Create figure 1 for main plots
        self.fig1 = plt.figure(1)
        window = plt.get_current_fig_manager().window
        self.dpi = self.fig1.dpi

        self.backend = mpl.get_backend()

        if self.backend == "Qt5Agg":
            # Hack to get screen size. Temporarily make a full-screen window, get size, then later set "real" size
            window.showMaximized()  # Make fullscreen
            plt.pause(.001)  # Draw items to screen so we can get size
            screen_x, screen_y = self.fig1.get_size_inches() * self.fig1.dpi  # size in pixels
        elif self.backend == "TkAgg":
            screen_x, screen_y = window.wm_maxsize()  # This works for TkAgg, but not Qt5Agg
        else:
            print("Unsupported backend " + self.backend)
            screen_y = 1024

        self.screen_y = screen_y

        self.set_fig1_size()

        self.canvas1 = self.fig1.canvas
        #        canvas1.manager.window.wm_geometry("%dx%d" % (screen_y,screen_y))

        if (not self.USE_TK) and self.USE_SEPARATE_BUTTON_PANEL:
            # Buttons on plot window cause annoying flicker whenever mouse moves over button
            # (even if not clicked). Solve this by putting buttons on their own window

            # Create figure 2, which will contain all the control buttons
            self.fig2 = plt.figure(2)

            screen_y_adj = int(self.screen_y * .95)  # Reduce height about 5% so we don't overlap windows taskbar

            menu_x_pixels = screen_y_adj / 5
            menu_y_pixels = screen_y_adj / 2
            if menu_x_pixels < 250:
                menu_x_pixels = 250

            # Stack buttons in vertical column - need tall narrow window
            self.fig2.set_size_inches(menu_x_pixels / self.dpi, menu_y_pixels / self.dpi)

            self.canvas2 = self.fig2.canvas

            # Put button window at top left of screen
            self.move_window(self.canvas2, 10, 10)
            # Move plot window to the right to avoid overlapping buttons
            self.move_window(self.canvas1, menu_x_pixels + 20, 0)
        else:
            self.move_window(self.canvas1, 250, 0)

    def set_fig1_size(self):

        screen_y_adj = int(self.screen_y * .95)  # Reduce height about 5% so we don't overlap windows taskbar

        # Make large square window for main plots
        self.fig1.set_size_inches(screen_y_adj / self.dpi, screen_y_adj / self.dpi)

    def add_button(self, text, func):

        if self.USE_TK:
            b = ttk.Button(self.root, text=text, command=func)
            b.pack(fill=tk.X, ipadx=10, ipady=10, padx=10, pady=5)
            return b
        else:
            return Button2(self.next_button_axis(), text, func)

    def add_check(self, text, var_int, func):

        if self.USE_TK:
            b = ttk.Checkbutton(self.root, text=text, variable=var_int, command=func)
            b.pack(fill=tk.X, ipadx=10, ipady=10, padx=10, pady=5)
            return b

    def next_button_axis(self):
        # Generate axes for the next button in series (either horizontal or vertical row)
        ax = plt.axes([self.buttonX, self.buttonY, self.BUTTON_WIDTH, self.BUTTON_HEIGHT])

        # Increment coordinates in preparation for next call
        self.buttonY = self.buttonY - self.BUTTON_HEIGHT - self.BUTTON_GAP

        return ax

    def move_window(self, canvas, x, y): # x and y are in pixels

        if self.backend == "Qt5Agg":
            geom = canvas.manager.window.geometry()
            x1,y1,dx,dy = geom.getRect()
            canvas.manager.window.setGeometry(x , y + 50, dx, dy)
        elif self.backend == "TkAgg":
            canvas.manager.window.wm_geometry("+%d+%d" % (x, y))
        else:
            print("Unsupported backend " + self.backend)


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

        if on_clicked_function is not None:
            self.on_clicked(on_clicked_function)

        self.label_text = label

    def SetTextVisible(self, vis):
        if vis:
            self.label.set_text(self.label_text)
            self.set_active(True)
        else:
            self.label.set_text("---")
            self.set_active(False)
