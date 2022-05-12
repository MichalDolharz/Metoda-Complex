import matplotlib.pyplot as plt
import numpy as np
from point import Point
from simplex import Simplex


def info(thing):
    print("\033[92m", thing, "\033[0m")


def f1(var):
    #print("f1", end=' ')
    return var[0]+var[1]-2  # <= 0


def f2(var):
    #print("f2", end=' ')
    return np.power(var[0], 2)-var[1]  # <= 0


def f3(var):
    #print("f3", end=' ')
    return -var[2]


def objectiveFun(var):
    x = var[0]
    y = var[1]
    return np.power(x-2, 2) + np.power(y-2, 2)


def main():

    cubeConstraints = [[-5, 5], [-5, 5]]
    constraintsFuns = [f1, f2]

    b = Simplex(cubeConstraints, constraintsFuns)
    b.display()

    print(b.get())

    def f(x): return eval(input("Podaj funkcje, np np.sin(x): "))
    x = int(input("Podaj dla jakiego x: "))
    y = f(x)
    print("Wynik: ", y)


main()
