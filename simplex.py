import matplotlib.pyplot as plt
import numpy as np
from point import Point


class Simplex():
    def __init__(self, cubeConstraints, constraintsFuns):

        # liczba punktow
        pts = int(len(cubeConstraints)) + 2

        self.points = []

        for it in range(0, pts):
            self.points.append(Point(cubeConstraints, constraintsFuns))

    def display(self):

        for it in range(0, len(self.points)):
            print("\nPoint", it+1, end=':')
            (self.points[it]).display()

        print("\n")

    def get(self):

        tmp = []
        for it in range(0, len(self.points)):
            tmp.append((self.points[it]).get())

        return tmp
