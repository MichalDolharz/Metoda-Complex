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

# Przed wpisaniem tej komendy trzeba zmienić nazwę main.py na MetodaComplex.py
# pyinstaller -F -w --onefile --icon=ikona.ico MetodaComplex.py


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

                if (not(values["xmax"]) and values["xmin"]) or (not(values["xmin"]) and values["xmax"]):
                    sg.Print(
                        f'Wprowadź oba ustawienia wykresu dla osi OX albo pozostaw pola puste dla wartości automatycznych!')
                    continue
                if (not(values["ymax"]) and values["ymin"]) or (not(values["ymin"]) and values["ymax"]):
                    sg.Print(
                        f'Wprowadź oba ustawienia wykresu dla osi OY albo pozostaw pola puste dla wartości automatycznych!')
                    continue

                print("0")

                if not(values["xmax"]):
                    window["xmax"].update(str(cubeConstraints[0][1]))
                    values["xmax"] = cubeConstraints[0][1]
                    # plt.xlim(float(values["xmin"]), float(values["xmax"]))

                print("1")

                if not(values["xmin"]):
                    window["xmin"].update(str(cubeConstraints[0][0]))
                    values["xmin"] = cubeConstraints[0][0]
                    # plt.xlim(float(values["xmin"]), float(values["xmax"]))

                # print("v xmin:", values["xmin"], "    v xmax:", values["xmax"])

                plt.xlim(float(values["xmin"]), float(values["xmax"]))

                print("2")

                if not(values["ymax"]):
                    window["ymax"].update(str(cubeConstraints[1][1]))
                    values["ymax"] = cubeConstraints[1][1]
                    # plt.ylim(float(values["ymin"]), float(values["ymax"]))

                print("3")

                if not(values["ymin"]):
                    window["ymin"].update(str(cubeConstraints[1][0]))
                    values["ymin"] = cubeConstraints[1][0]
                    # plt.ylim(float(values["ymin"]), float(values["ymax"]))

                print("4")

                # print("v ymin:", values["ymin"], "    x ymax:", values["ymax"])

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

                # operacje na kompleksie
                kompleks = Complex()
                kompleks.fill(cubeConstraints, constraintsFuns,
                              objectiveFun, epsilon)
                best_point, step_prog = kompleks.run(
                    objectiveFun, constraintsFuns, cubeConstraints, max_it)
                print("\nZnaleziony optymalny punkt:")
                best_point.display(mode="multirow")
                print("\nWartość funkcji celu dla znalezionego punktu:")
                print(kompleks.getFmin(objectiveFun))

                # rysowanie wykresu
                if len(cubeConstraints) == 2:
                    kompleks.plotPolygon(
                        objectiveFun, constraintsFunsString, cubeConstraints, printing=False)
                    makeKolorki(objectiveFun, values)

                    figure = draw_figure(
                        window['-PLOT_CANV-'].TKCanvas, plt.gcf(), values)

                plt.xlim(float(values["xmin"]), float(values["xmax"]))
                plt.ylim(float(values["ymin"]), float(values["ymax"]))

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
                    objectiveFun, constraintsFunsString, tmp_Cube, printing=False)
                makeKolorki(objectiveFun, values)
                plt.xlim(float(values["xmin"]), float(values["xmax"]))
                plt.ylim(float(values["ymin"]), float(values["ymax"]))
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


def makeKolorki(objectiveFun, values):
    plt.xlim(float(values["xmin"]), float(values["xmax"]))
    plt.ylim(float(values["ymin"]), float(values["ymax"]))
    xmin, xmax = plt.xlim()
    ymin, ymax = plt.ylim()
    x = np.linspace(xmin - 2, xmax + 2)
    y = np.linspace(ymin - 2, ymax + 2)
    X, Y = np.meshgrid(x, y)
    Z = objectiveFun(X, Y)
    Z = np.array(Z)
    Z = np.reshape(Z, (len(x), len(y)))

    plt.contourf(X, Y, Z, extend='both', levels=500, cmap="rainbow", alpha=0.9)
    plt.colorbar()


def main():

    okienko()


main()
