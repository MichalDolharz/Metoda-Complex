import matplotlib.pyplot as plt
import numpy as np
from point import Point
from simplex import Simplex
from math import *


def info(thing):
    print("\033[92m", thing, "\033[0m")


def f1(var):
    #print("f1", end=' ')
    #print("f1 var[0]:", var[0])
    #print("f1 var[1]:", var[1])
    return var[0]+var[1]-2  # <= 0


def f2(var):
    #print("f2", end=' ')
    #print("f2 var[0]:", var[0])
    #print("f2 var[1]:", var[1])
    return np.power(var[0], 2)-var[1]  # <= 0


def f3(var):
    #print("f3", end=' ')
    return -var[2]


def objectiveFun(var):
    x = var[0]
    y = var[1]
    return np.power(x-2, 2) + np.power(y-2, 2)


def f(var):
    return var[0] + var[1]


def objFunction(x):
    # eval() wykonuje funkcje zapisana w stringu o ile się da.
    # To oznacza, ze zamiast podania funkcji
    # mozna napisac dowolna instrukcje pythona,
    # a to niebezpieczne i trzeba to jakos zabezpieczyc.
    return eval(input("Podaj funkcje, np np.sin(x): "))


def main():

    cubeConstraints = [[-5, 5], [-5, 5]]
    constraintsFuns = [f1, f2]

    b = Simplex()
    b.fill(cubeConstraints, constraintsFuns, objectiveFun)
    b.display()
    #print(b.objFunValue(f, [1, 2]))
    #print("main ", b.centroid(f))

    print(b.get())

    b.plot2()

    # x = int(input("Podaj wartosc x: "))
    # y = f(x)
    # print("Wynik: ", y)


main()
