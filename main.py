import matplotlib.pyplot as plt
import numpy as np
from point import Point
from complex import Complex
from interface import *
from math import *
import PySimpleGUI as sg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from funcParser import getFunction
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


def clear_canvas(figure):
    figure.get_tk_widget().forget()
    plt.close('all')


def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    widget = figure_canvas_agg.get_tk_widget()
    figure_canvas_agg.draw()
    widget.pack(side='top', fill='both', expand=1)
    return figure_canvas_agg

def okienko():
    cubeConstraints = []
    constraintsFuns_print = []
    constraintsFuns = []
    figure = None
    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        try:
            if event == sg.WIN_CLOSED:  # if user closes window or clicks cancel
                break
            if event == "Dodaj-kostka":
                
                print('Dodano ograniczenie kostki')
                cubeConstraints.append([float(values['LowerConstr']), float(values['UpperConstr'])])
                cubeConstr_list_print = make_cubeConstr_list(cubeConstraints)
                window['List-kostka'].update(cubeConstr_list_print)
                
            if event == "Dodaj-funkcja":
                if str(values['-funConstr-']) == "":
                    print("Nie wprowadzono ograniczenia funkcyjnego")
                    continue
                print('Dodano ograniczenie funkcyjne')
                constraintsFuns.append(getFunction(values['-funConstr-']))
                constraintsFuns_print.append(str(values['-funConstr-']))
                window['List-funkcje'].update(constraintsFuns_print)

            if event == "Uruchom":
                if(figure):
                    clear_canvas(figure)
                # window['logi'].update('')
                plt.clf()
                print("Uruchomiono algorytm")

                # constraintsFuns = [f1, f2]
                epsilon = float(values['-epsilon-'])
                kompleks = Complex()
                objectiveFun = getFunction(values['combo-objFun'])
                kompleks.fill(cubeConstraints, constraintsFuns, objectiveFun, epsilon)
                best_point = kompleks.run(objectiveFun, constraintsFuns, cubeConstraints)
                kompleks.plotPolygon(objectiveFun, print=False)
                figure = draw_figure(window['-PLOT_CANV-'].TKCanvas, plt.gcf())
                best_point.display()
                makeKolorki(objectiveFun)
                print("")
                # window['logi'].update()

            if event == 'Usun-kostka' and values['List-kostka']:
                #
                #
                # TU JEST KURWA PROBLEM
                #
                #
                #
                print("Usunięto ogr. kostki ", values['List-kostka'][0])
                id = constraintsFuns_print.index(values['List-kostka'][0])
                constraintsFuns_print.remove(values['List-kostka'][0])
                constraintsFuns.pop(id)
                window['List-kostka'].update(constraintsFuns_print)

            if event == 'Usun-funkcja' and values['List-funkcje']:
                print("Usunięto ogr. funkcyjne ", values['List-funkcje'][0])
                id = constraintsFuns_print.index(values['List-funkcje'][0])
                constraintsFuns_print.remove(values['List-funkcje'][0])
                constraintsFuns.pop(id)
                window['List-funkcje'].update(constraintsFuns_print)

            if event == "Wyczysc-logi":
                window['logi'].update('')

        except Exception as e:
                tb = traceback.format_exc()
                sg.Print(f'An error happened.  Here is the info:', e, tb)
                # sg.popup_error(f'AN EXCEPTION OCCURRED!', e, tb)
            
    window.close()

def makeKolorki(objectiveFun):
    xmin,xmax = plt.xlim()
    ymin,ymax = plt.ylim()
    x = np.linspace(xmin - 2, xmax + 2)
    y = np.linspace(ymin - 2, ymax + 2)
    X, Y = np.meshgrid(x, y)
    Z = objectiveFun([X,Y])
    Z = np.array(Z)
    Z = np.reshape(Z, (len(x), len(y)))
    plt.contourf(X, Y, Z, extend='both', levels=10)
    plt.colorbar()


def main():
    
    okienko()

    # cubeConstraints = [[-5, 5], [-5, 5]]#, [-1, 1]]  # , [-5, 5]]
    # constraintsFuns = [f1, f2]#, f3]

    # epsilon = 0.001
    # # objectiveFun = getFunction("(x1-2)^2 + (x2-2)^2")
    # kompleks = Complex()
    # kompleks.fill(cubeConstraints, constraintsFuns, objectiveFun, epsilon)
    # kompleks.plotPolygon(objectiveFun)
    # best_point = kompleks.run(objectiveFun, constraintsFuns, cubeConstraints)
    # best_point.display()
    # kompleks.plotPolygon(objectiveFun, print=True)
    


main()
