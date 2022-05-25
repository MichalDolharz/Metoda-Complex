import matplotlib.pyplot as plt
import numpy as np
from point import Point
from complex import Complex
from interface import *
from math import *
import PySimpleGUI as sg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from funcParser import getFunction, getFunctionString
import traceback


def info(thing):
    print("\033[92m", thing, "\033[0m")


def f1(var):
    # print("f1", end=' ')
    # print("f1 var[0]:", var[0])
    # print("f1 var[1]:", var[1])
    return var[0]+var[1]-2  # <= 0
    # return var[0]+var[1]-2  # <= 0


def f2(var):
    # print("f2", end=' ')
    # print("f2 var[0]:", var[0])
    # print("f2 var[1]:", var[1])
    return np.power(var[0], 2)-var[1]  # <= 0
    # return np.power(var[0], 2)-var[1]  # <= 0


def f1x(x1=0, x2=0, x3=0, x4=0, x5=0):
    # print("f1", end=' ')
    # print("f1 var[0]:", var[0])
    # print("f1 var[1]:", var[1])
    return x1+x2-2  # <= 0
    # return var[0]+var[1]-2  # <= 0


def f2x(x1=0, x2=0, x3=0, x4=0, x5=0):
    # print("f2", end=' ')
    # print("f2 var[0]:", var[0])
    # print("f2 var[1]:", var[1])
    return np.power(x1, 2)-x2  # <= 0
    # return np.power(var[0], 2)-var[1]  # <= 0


def f3x(x1=0, x2=0, x3=0, x4=0, x5=0):
    # print("f3", end=' ')
    return x3+x2-2  # <= 0


def objectiveFun(var):
    x = var[0]
    y = var[1]
    #z = var[2]
    return np.power(x-2, 2) + np.power(y-2, 2)  # + np.power(z-2, 2)


def objectiveFunx(x1=0, x2=0, x3=0, x4=0, x5=0):
    x = x1
    y = x2
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


def clear_canvas(figure):
    figure.get_tk_widget().forget()
    plt.close('all')


def draw_figure(canvas, figure, values):
    # plt.xlim(float(values["xmin"]), float(values["xmax"]))
    # plt.ylim(float(values["ymin"]), float(values["ymax"]))
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    widget = figure_canvas_agg.get_tk_widget()
    figure_canvas_agg.draw()
    widget.pack(side='top', fill='both', expand=1)
    return figure_canvas_agg


def okienko():
    cubeConstraints = []
    constraintsFuns_print = []
    constraintsFuns = []
    constraintsFunsString = []
    figure = None
    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        try:

            if event == sg.WIN_CLOSED:  # if user closes window or clicks cancel
                break
            if event == "Dodaj-kostka":
                if len(values["List-kostka"]) == 5:
                    sg.Print(f'Wprowadzono już limit ograniczeń kostki!')
                    continue
                if str(values['LowerConstr']) == "" or str(values['UpperConstr']) == "":
                    sg.Print(f'Nie wprowadzono ograniczenia/ń zmiennej!')
                    continue
                print('Dodano ograniczenie kostki')
                cubeConstraints.append(
                    [float(values['LowerConstr']), float(values['UpperConstr'])])
                cubeConstr_list_print = make_cubeConstr_list(cubeConstraints)
                window['List-kostka'].update(cubeConstr_list_print)

            if event == "Dodaj-funkcja":
                if len(values["List-funkcje"]) == 5:
                    sg.Print(f'Wprowadzono już limit ograniczeń funkcyjnych!')
                    continue
                if str(values['-funConstr-']) == "":
                    sg.Print(f'Nie wprowadzono ograniczenia funkcyjnego!')
                    continue
                print('Dodano ograniczenie funkcyjne')
                constraintsFuns_print.append(values['-funConstr-'])
                constraintsFunsString.append(
                    getFunctionString(values['-funConstr-']))
                # constraintsFuns.append(getFunction(values['-funConstr-']))

                window['List-funkcje'].update(constraintsFuns_print)

            # Uruchomnienie algorytmu
            if event == "Uruchom":
                if(figure):
                    clear_canvas(figure)

                plt.clf()

                print("Uruchomiono algorytm")

                if values["xmax"] == "" and values["xmin"] == "" and values["ymax"] == "" and values["ymin"] == "":
                    window["xmin"].update(float(cubeConstraints[0][0]))
                    window["xmax"].update(float(cubeConstraints[0][1]))
                    window["ymin"].update(float(cubeConstraints[1][0]))
                    window["ymax"].update(float(cubeConstraints[1][1]))
                    plt.xlim(cubeConstraints[0][0], cubeConstraints[0][1])
                    plt.ylim(cubeConstraints[1][0], cubeConstraints[1][1])

                if len(cubeConstraints) < 5:
                    tmp_Cube = cubeConstraints[:]
                    while not (len(tmp_Cube) == 5):
                        tmp_Cube.append([0, 0])

                # przypisywanie wartości z okna do zmiennych
                epsilon = float(values['-epsilon-'])
                max_it = float(values['-max-it-'])

                # parsowanie funkcji
                objectiveFun = getFunction(values['combo-objFun'])
                constraintsFuns = []
                for ogr in constraintsFuns_print:
                    constraintsFuns.append(getFunction(ogr))
                # cubeConstraints = [[-5, 5], [-5, 5]]
                # constraintsFuns = [f1x, f2x]

                # operacje na kompleksie
                kompleks = Complex()
                kompleks.fill(cubeConstraints, constraintsFuns,
                              objectiveFun, epsilon)
                best_point, step_prog = kompleks.run(
                    objectiveFun, constraintsFuns, cubeConstraints, max_it)
                best_point.display()
                print("\n")
                print("fmin", kompleks.getFmin(objectiveFun))

                # rysowanie wykresu
                kompleks.plotPolygon(
                    objectiveFun, constraintsFunsString, tmp_Cube, print=False)
                # plt.xlim(float(values["xmin"]), float(values["xmax"]))
                # plt.ylim(float(values["ymin"]), float(values["ymax"]))

                makeKolorki(objectiveFun)

                figure = draw_figure(
                    window['-PLOT_CANV-'].TKCanvas, plt.gcf(), values)

                # ustawienia wykresu
                # xmin,xmax = plt.xlim()
                # ymin,ymax = plt.ylim()
                # window["xmin"].update(xmin)
                # window["xmax"].update(xmax)
                # window["ymin"].update(ymin)
                # window["ymax"].update(ymax)

                # kroki i slajder init
                stepKompleks = Complex()
                window["slider-kroki"].update(range=(0, 0))
                window["slider-kroki"].update(range=(0, len(step_prog)))
                window['-kroki-'].update(len(step_prog))
                window['-wys-krok-'].update('')

            # obsluga poruszania slajderem
            if event == "slider-kroki":
                if(figure):
                    clear_canvas(figure)

                plt.clf()
                # if not (ax_complex  == None):
                #     ax_complex.cla()
                krok = int(values['slider-kroki'])
                krok_minus = krok - 1
                # print("Wyświetlam krok", krok)
                window['-wys-krok-'].update(krok)

                step_prog[krok_minus].plotPolygon(
                    objectiveFun, constraintsFunsString, tmp_Cube, print=False)
                makeKolorki(objectiveFun)
                # plt.xlim(float(values["xmin"]), float(values["xmax"]))
                # plt.ylim(float(values["ymin"]), float(values["ymax"]))
                figure = draw_figure(
                    window['-PLOT_CANV-'].TKCanvas, plt.gcf(), values)

            # usuwanie zaznaczonego przedziału w liscie ogr. kostki
            if event == 'Usun-kostka' and values['List-kostka']:
                #
                #
                # TU JEST PROBLEM
                #
                #
                #
                print("Usunięto ogr. kostki ", values['List-kostka'][0])
                id = constraintsFuns_print.index(values['List-kostka'][0])
                constraintsFuns_print.remove(values['List-kostka'][0])
                constraintsFuns.pop(id)
                window['List-kostka'].update()

            # usuwanie zaznaczonej funkcji w liscie ogr. funkc.
            if event == 'Usun-funkcja' and values['List-funkcje']:
                print("Usunięto ogr. funkcyjne ", values['List-funkcje'][0])
                id = constraintsFuns_print.index(values['List-funkcje'][0])
                constraintsFuns_print.remove(values['List-funkcje'][0])
                constraintsFunsString.pop(id)
                window['List-funkcje'].update(constraintsFuns_print)

            # czyszczenie okna z outputem
            if event == "Wyczysc-logi":
                window['logi'].update('')

        except Exception as e:
            tb = traceback.format_exc()
            sg.Print(f'An error happened.  Here is the info:', e, tb)
            # sg.popup_error(f'AN EXCEPTION OCCURRED!', e, tb)

    window.close()


def makeKolorki(objectiveFun):
    xmin, xmax = plt.xlim()
    ymin, ymax = plt.ylim()
    x = np.linspace(xmin - 2, xmax + 2)
    y = np.linspace(ymin - 2, ymax + 2)
    X, Y = np.meshgrid(x, y)
    Z = objectiveFun(X, Y)
    Z = np.array(Z)
    Z = np.reshape(Z, (len(x), len(y)))
    plt.contourf(X, Y, Z, extend='both', levels=500, cmap="rainbow")
    plt.colorbar()


def main():

    okienko()

    # cubeConstraints = [[-5, 5], [-5, 5], [-5, 5]]#, [-1, 1]]  # , [-5, 5]]
    # constraintsFuns = [f1x, f2x, f3x]
    # step_prog = []

    # epsilon = 0.001
    # max_it = 5000
    # # objectiveFun = getFunction("(x1-2)^2 + (x2-2)^2")
    # kompleks = Complex()
    # kompleks.fill(cubeConstraints, constraintsFuns, objectiveFunx, epsilon)
    # kompleks.plotPolygon(objectiveFunx)
    # best_point, step_prog = kompleks.run(objectiveFunx, constraintsFuns, cubeConstraints, max_it)
    # best_point.display()
    # print("kompleks")
    # kompleks.display()
    # kompleks.plotPolygon(objectiveFunx, print=True)
    # for it in range(0, len(step_prog)):
    #     print(step_prog[it])


main()
