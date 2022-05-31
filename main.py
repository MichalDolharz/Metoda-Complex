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
    constraintsFuns = []
    constraintsFunsString = []
    cubeConstr_list_print = []
    constraintsFuns_print = []
    figure = None
    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        try:

            if event == sg.WIN_CLOSED:  # if user closes window or clicks cancel
                break
            if event == "Dodaj-kostka":
                if len(cubeConstr_list_print) == 5:
                    sg.Print(f'Wprowadzono już limit ograniczeń kostki!')
                    continue
                if str(values['LowerConstr']) == "" or str(values['UpperConstr']) == "":
                    sg.Print(f'Nie wprowadzono ograniczenia/ń zmiennej!')
                    continue
                print('Dodano ograniczenie kostki')
                cubeConstraints.append(
                    [float(values['LowerConstr']), float(values['UpperConstr'])])
                cubeConstr_list_print = (make_cubeConstr_list(cubeConstraints))
                window['List-kostka'].update(cubeConstr_list_print)

            if event == "Dodaj-funkcja":
                if len(constraintsFuns_print) == 5:
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

                # if values["xmax"] == "" and values["xmin"] == "" and values["ymax"] == "" and values["ymin"] == "":
                #     window["xmin"].update(float(cubeConstraints[0][0]))
                #     window["xmax"].update(float(cubeConstraints[0][1]))
                #     window["ymin"].update(float(cubeConstraints[1][0]))
                #     window["ymax"].update(float(cubeConstraints[1][1]))
                #     plt.xlim(cubeConstraints[0][0], cubeConstraints[0][1])
                #     plt.ylim(cubeConstraints[1][0], cubeConstraints[1][1])
                if (values["xmax"] == "" and values["xmin"]) or (values["xmin"] == "" and values["xmax"]):
                    sg.Print(f'Wprowadź oba ustawienia wykresu dla osi OX albo pozostaw puste dla automatycznych!')
                    continue
                if (values["ymax"] == "" and values["ymin"]) or (values["ymin"] == "" and values["ymax"]):
                    sg.Print(f'Wprowadź oba ustawienia wykresu dla osi OY albo pozostaw puste dla automatycznych!')
                    continue
                if values["xmax"] == "":
                    window["xmax"].update(float(cubeConstraints[0][1]))
                    # print(values["xmax"], "typ: ", type(values["xmax"]))
                    # print(float(values["xmax"]), "typ: ", type(float(values["xmax"])))
                    plt.xlim(float(values["xmin"]), float(values["xmax"]))
                if values["xmin"] == "":
                    print("cos")
                    window["xmin"].update(float(cubeConstraints[0][0]))
                    plt.xlim(float(values["xmin"]), float(values["xmax"]))
                if values["ymax"] == "":
                    window["ymax"].update(float(cubeConstraints[1][1]))
                    plt.ylim(float(values["ymin"]), float(values["ymax"]))
                if values["ymin"] == "":
                    window["ymin"].update(float(cubeConstraints[1][0]))
                    plt.ylim(float(values["ymin"]), float(values["ymax"]))
                

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
                print("\n")
                print("Znaleziony optymalny punkt:")
                best_point.display(mode="multirow")
                print("\n")
                print("Wartość funkcji celu dla znalezionego punktu:")
                print(kompleks.getFmin(objectiveFun))

                # rysowanie wykresu
                if len(cubeConstraints) == 2:
                    kompleks.plotPolygon(
                        objectiveFun, constraintsFunsString, cubeConstraints, print=False)
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
                # window['-wys-krok-'].update('')

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
                # window['-wys-krok-'].update(krok)

                step_prog[krok_minus].plotPolygon(
                    objectiveFun, constraintsFunsString, tmp_Cube, print=False)
                makeKolorki(objectiveFun)
                # plt.xlim(float(values["xmin"]), float(values["xmax"]))
                # plt.ylim(float(values["ymin"]), float(values["ymax"]))
                figure = draw_figure(
                    window['-PLOT_CANV-'].TKCanvas, plt.gcf(), values)

            # usuwanie zaznaczonego przedziału w liscie ogr. kostki
            if event == 'Usun-kostka' and values['List-kostka']:
                print("Usunięto ogr. kostki ", values['List-kostka'][0])
                id = cubeConstr_list_print.index(values['List-kostka'][0])
                cubeConstraints.pop(id)
                cubeConstr_list_print = make_cubeConstr_list(cubeConstraints)
                window['List-kostka'].update(cubeConstr_list_print)

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
