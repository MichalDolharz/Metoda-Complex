import matplotlib.pyplot as plt
import numpy as np
from point import Point
from complex import Complex
from interface import *
from math import *
import PySimpleGUI as sg


def info(thing):
    print("\033[92m", thing, "\033[0m")


def f1(var):
    # print("f1", end=' ')
    # print("f1 var[0]:", var[0])
    # print("f1 var[1]:", var[1])
    return 0.33*var[0]+var[1]-3  # <= 0
    # return var[0]+var[1]-2  # <= 0


def f2(var):
    # print("f2", end=' ')
    # print("f2 var[0]:", var[0])
    # print("f2 var[1]:", var[1])
    return 0.3*np.power(var[0], 2)-var[1]  # <= 0
    # return np.power(var[0], 2)-var[1]  # <= 0


def f3(var):
    # print("f3", end=' ')
    return var[2]  # <= 0


def objectiveFun(var):
    x = var[0]
    y = var[1]
    #z = var[2]
    return np.power(x-2, 2) + np.power(y-2, 2)  # + np.power(z-2, 2)


def f(var):
    return var[0] + var[1]


def objFunction(x):
    # eval() wykonuje funkcje zapisana w stringu o ile się da.
    # To oznacza, ze zamiast podania funkcji
    # mozna napisac dowolna instrukcje pythona,
    # a to niebezpieczne i trzeba to jakos zabezpieczyc.
    return eval(input("Podaj funkcje, np np.sin(x): "))


def okienko():
    sg.theme('Dark')

    objFun_layout = [
        [sg.InputText(size=(40, 50)), sg.Text("<= 0"), sg.Submit("Ustaw")]]
    objFun = sg.Frame("Funkcja celu", layout=objFun_layout)

    cubeConstr_layout = [[sg.InputText(size=(5, 0)),
                          sg.Text("<= x <= "),
                          sg.InputText(size=(5, 0))],
                         [sg.Submit("Dodaj", key="Dodaj-kostka"),
                         sg.Push(),
                         sg.Submit("Usuń", key="Usun-kostka")]]
    cubeConstraints = sg.Frame(
        "Ograniczenia kostki", layout=cubeConstr_layout)

    constraintFun_layout = [[sg.InputText(),
                             sg.Text("<= 0"), ],
                            [sg.Submit("Dodaj", key="Dodaj-funkcja"),
                             sg.Push(),
                             sg.Submit("Usuń", key="Usun-funkcja")]]
    constraintsFun = sg.Frame("Ograniczenia funkcyjne",
                              layout=constraintFun_layout)

    algorithm_layout = [[sg.Text("Epsilon"), sg.HSeparator(), sg.InputText(size=(10))],
                        [sg.Text("Max. iteracji"), sg.HSeparator(),
                         sg.InputText(size=(10))],
                        [sg.Submit("Uruchom")]]
    algorithm = sg.Frame("Parametry algorytmu",
                         layout=algorithm_layout, size=(200, 100))

    logs_layout = [[sg.Output()]]
    logs = sg.Frame("Komunikaty", layout=logs_layout)

    chart_sett_layout = [[sg.Text("Oś X: od "),
                          sg.InputText(size=(5, 0)),
                          sg.Text(" do "),
                          sg.InputText(size=(5, 0))],
                         [sg.Text("Oś Y: od "),
                          sg.InputText(size=(5, 0)),
                          sg.Text(" do "),
                          sg.InputText(size=(5, 0))]]
    chart_sett = sg.Frame("Ustawienia wykresu", layout=chart_sett_layout)

    matplotlib_layout = [[sg.Text('Tu ebdzie wykres')]]
    matplotlib_ = sg.Frame("Wykres", matplotlib_layout)

    matplotlib_sett_layout = [[sg.Text('Tu będą kroki')]]
    matplotlib_sett = sg.Frame("Przeglądanie kroków", matplotlib_sett_layout)

    Column1_1 = [[cubeConstraints], [algorithm]]
    Column1_2 = [[constraintsFun], [chart_sett]]
    Column1 = [[objFun], [sg.Column(Column1_1), sg.Column(Column1_2)], [logs]]
    Column2 = [[matplotlib_], [matplotlib_sett]]

    #Column1 = [[objFun], [cubeConstraints, constraintsFun], [algorithm, chart_sett], [logs]]
    #Column2 = [[matplotlib_], [matplotlib_sett]]

    layout = [[sg.Column(Column1, size=(500, 600)), sg.Column(Column2)]]

    # Create the Window
    window = sg.Window('Metoda Complex', layout)

    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:  # if user closes window or clicks cancel
            break
        if event == "Dodaj-kostka":
            print('Dodano ograniczenie kostki')

    window.close()


def main():

    cubeConstraints = [[-5, 5], [-5, 5], [-5, 5]]  # , [-5, 5]]
    constraintsFuns = [f1, f2, f3]

    epsilon = 0.001

    # kompleks = Complex()
    # kompleks.fill(cubeConstraints, constraintsFuns, objectiveFun, epsilon)
    # kompleks.plotPolygon(objectiveFun)
    # best_point = kompleks.run(objectiveFun, constraintsFuns, cubeConstraints)
    # best_point.display()
    # kompleks.plotPolygon(objectiveFun)

    okienko()


main()
