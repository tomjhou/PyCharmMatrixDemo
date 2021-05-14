from enum import Enum
import numpy as np
import matplotlib.patches as mpatches


class ChangeType(Enum):
    none = 0
    V1 = 1
    V2 = 2


class PlotType(Enum):
    Copy = 0
    Dot1 = 1
    Dot2 = 2

# Create list of points on unit circle corresponding to steps and dots
class UnitCircleStuff:
    def __init__(self, _steps, _numdots, inputColor):
        self.stepsPerDot = round(_steps / _numdots)
        self.steps = self.stepsPerDot * _numdots
        self.numdots = _numdots

        # Define 2 * pi
        pi2 = 2*np.pi

        # Create list of points on unit circle, one per step
        self.unitVectorAngles = np.linspace(0, pi2, self.steps + 1)
        self.unitVectorX = np.cos(self.unitVectorAngles)
        self.unitVectorY = np.sin(self.unitVectorAngles)

        # Create list of points on unit circle, one per dot
        dotAngles = np.linspace(0, pi2, _numdots + 1)
        self.dotsX = np.cos(dotAngles)
        self.dotsY = np.sin(dotAngles)

        # Create list of red circular patches on unit circle
        self.patchList1 = []
        for i in range(0, self.numdots):
            self.patchList1.append(mpatches.Circle((self.dotsX[i], self.dotsY[i]), 0.05, color=inputColor))

    # Create NEW list of OUTPUT purple circular patches corresponding to INPUT patches after matrix multiplication
    def makeCircs(self, Array1, outputColor):
        self.patchList2 = []
        for i in range(0, self.numdots):
            v = [self.dotsX[i], self.dotsY[i]]
            x2 = np.dot(Array1[0, :], v)
            y2 = np.dot(Array1[1, :], v)
            self.patchList2.append(mpatches.Circle((x2, y2), 0.05, color=outputColor))

    # Update EXISTING list of output patches with new array
    def updateCircs(self, Array1):
        for i in range(0, self.numdots):
            v = [self.dotsX[i], self.dotsY[i]]
            x2 = np.dot(Array1[0, :], v)
            y2 = np.dot(Array1[1, :], v)
            self.patchList2[i].center = x2, y2
