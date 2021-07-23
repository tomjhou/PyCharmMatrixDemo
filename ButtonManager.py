
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.widgets import Button


class ButtonManager:

    def __init__(self, _is_vertical = True, _is_separate = True):

        self.USE_SEPARATE_BUTTON_PANEL = _is_separate   # Put buttons on separate window
        self.USE_VERTICAL_BUTTON_PANEL = _is_vertical   # Stack buttons vertically instead of horizontally
        self.BUTTON_GAP = 0.01                  # Space (as fraction of screen) between buttons

        if self.USE_SEPARATE_BUTTON_PANEL:
            # Button dimensions are all expressed as fraction of window size
            if self.USE_VERTICAL_BUTTON_PANEL:
                self.BUTTON_Y_COORD = 0.8
                self.BUTTON_HEIGHT = 0.15
                self.BUTTON_WIDTH = 0.8
                self.BUTTON_X_START = 0.1
            else:
                self.BUTTON_Y_COORD = 0.1  # 0.95
                self.BUTTON_HEIGHT = 0.8   # 0.03  # Above about 0.1, buttons disappear - presumably they collide with graphs?
                self.BUTTON_WIDTH = 0.2
                self.BUTTON_X_START = 0.05
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

        if self.USE_SEPARATE_BUTTON_PANEL:
            # Buttons on plot window cause annoying flicker whenever mouse moves over button
            # (even if not clicked). Solve this by putting buttons on their own window

            # Create figure 2 with buttons
            self.fig2 = plt.figure(2)

            screen_y_adj = int(self.screen_y * .95)  # Reduce height about 5% so we don't overlap windows taskbar

            if self.USE_VERTICAL_BUTTON_PANEL:
                # Stack buttons in vertical column - need tall narrow window
                self.fig2.set_size_inches(screen_y_adj / self.dpi / 5, screen_y_adj / self.dpi / 2)
                # Move plot window to the right to avoid overlapping buttons
                self.move_window(self.canvas1, screen_y_adj * .3, 0)
            else:
                # Make short wide button window
                self.fig2.set_size_inches(screen_y_adj / self.dpi / 2, screen_y_adj / self.dpi / 15 )
                # Move plot window to the right to avoid overlapping buttons
                self.move_window(self.canvas1, screen_y_adj * .6, 0)

            self.canvas2 = self.fig2.canvas
            # Put button window at top left of screen
            self.move_window(self.canvas2, 25, 25)

    def set_fig1_size(self):

        screen_y_adj = int(self.screen_y * .95)  # Reduce height about 5% so we don't overlap windows taskbar

        # Make large square window for main plots
        self.fig1.set_size_inches(screen_y_adj / self.dpi, screen_y_adj / self.dpi)

    def add_button(self, text, func):

        return Button2(self.next_button_axis(), text, func)

    def next_button_axis(self):
        # Generate axes for the next button in series (either horizontal or vertical row)
        ax = plt.axes([self.buttonX, self.buttonY, self.BUTTON_WIDTH, self.BUTTON_HEIGHT])

        # Increment coordinates in preparation for next call
        if self.USE_VERTICAL_BUTTON_PANEL:
            self.buttonY = self.buttonY - self.BUTTON_HEIGHT - self.BUTTON_GAP
        else:
            self.buttonX = self.buttonX + self.BUTTON_WIDTH + self.BUTTON_GAP

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
