import matplotlib.pyplot as plt
import numpy as np
from point import Point


class Simplex():
    def __init__(self, cubeConstraints, constraintsFuns):

        # liczba punktow
        pts = int(len(cubeConstraints)) + 2

        self.points = []

        for it in range(0, pts):
            self.points.append(Point(cubeConstraints, constraintsFuns, it))

    # wyswietla wszystkie wierzcholki

    def display(self):

        for point in self.points:
            print("\nPoint ID-" + str(point.id), end=':')
            point.display()
        print("\n")

    # zwraca tablice punktow
    def get(self):

        tmp = []
        for it in range(0, len(self.points)):
            tmp.append((self.points[it]).get())

        return tmp

    # oblicza wartosc funkcji celu w kazdym wierzcholku
    # def convergence(self, objFun):
    #    for point in points

    # oblicza centroid, czyli "umowny" srodek obszaru simplexu
    # def centroid():
