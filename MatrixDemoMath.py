from enum import Enum
import numpy as np
import matplotlib.patches as mpatches
import colorsys

class ChangeType(Enum):
    none = 0
    V1 = 1
    V2 = 2


class PlotType(Enum):
    Copy = 0
    Dot1 = 1
    Dot2 = 2

class CircleColorType(Enum):
    Rainbow = 0
    Shaded = 1
    Flat = 2

# Create list of points on unit circle corresponding to steps and dots
class UnitCircleStuff:
    def __init__(self, _steps, _numdots, circumferenceColor1, circumferenceColor2):
        self.stepsPerDot = round(_steps / _numdots)
        self.numsteps = self.stepsPerDot * _numdots
        self.numdots = _numdots

        # Define 2 * pi
        pi2 = 2*np.pi

        # Create list of points on unit circle, one per step
        self.unitVectorAngles = np.linspace(0, pi2, self.numsteps + 1)
        self.unitVectorX = np.cos(self.unitVectorAngles)
        self.unitVectorY = np.sin(self.unitVectorAngles)

        # Create list of points on unit circle, one per dot
        dotAngles = np.linspace(0, pi2, _numdots + 1)
        self.dotsX = np.cos(dotAngles)
        self.dotsY = np.sin(dotAngles)

        self.dotColorList = []
        self.stepColorList = []
        self.colorType = CircleColorType.Shaded

        # Create list of red circular patches on unit circle
        self.patchList1 = []
        for i in range(0, self.numdots):
            if self.colorType == CircleColorType.Rainbow:
                new_color = colorsys.hsv_to_rgb(i/self.numdots,1,1)
            elif self.colorType == CircleColorType.Shaded:
                new_color = [0, 0, 0]  # Must use array instead of tuple, as tuple is not mutable
                for j in range(0, 3):
                    scale = (self.dotsX[i]+1)/2  # Convert [-1,1] range to [0,1]
                    new_color[j] = circumferenceColor1[j] * scale + circumferenceColor2[j] * (1 - scale)
            elif self.colorType == CircleColorType.Flat:
                new_color = circumferenceColor1

            self.dotColorList.append(new_color)
            self.patchList1.append(mpatches.Circle((self.dotsX[i], self.dotsY[i]), 0.05, color=new_color))

        for i in range(0, self.numsteps):
            if self.colorType == CircleColorType.Rainbow:
                new_color = colorsys.hsv_to_rgb(i/self.numsteps,1,1)
            elif self.colorType == CircleColorType.Shaded:
                new_color = [0, 0, 0]  # Must use array instead of tuple, as tuple is not mutable
                for j in range(0, 3):
                    scale = (self.unitVectorX[i]+1)/2  # Convert [-1,1] range to [0,1]
                    new_color[j] = circumferenceColor1[j] * scale + circumferenceColor2[j]  * (1 - scale)
            elif self.colorType == CircleColorType.Flat:
                new_color = circumferenceColor1

            self.stepColorList.append(new_color)

    # Create NEW list of OUTPUT purple circular patches corresponding to INPUT patches after matrix multiplication
    def makeCircs(self, Array1, outputColor):
        self.patchList2 = []
        for i in range(0, self.numdots):
            v = [self.dotsX[i], self.dotsY[i]]
            x2 = np.dot(Array1[0, :], v)
            y2 = np.dot(Array1[1, :], v)
            new_color = outputColor
            if self.colorType != CircleColorType.Flat:
                new_color = self.dotColorList[i]
            self.patchList2.append(mpatches.Circle((x2, y2), 0.05, color=new_color))

    # Update EXISTING list of output patches with new array
    def updateCircs(self, Array1):
        for i in range(0, self.numdots):
            v = [self.dotsX[i], self.dotsY[i]]
            x2 = np.dot(Array1[0, :], v)
            y2 = np.dot(Array1[1, :], v)
            self.patchList2[i].center = x2, y2
