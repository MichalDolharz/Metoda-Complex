from xmlrpc.server import SimpleXMLRPCDispatcher
import matplotlib.pyplot as plt
import numpy as np


def info(thing):
    print("\033[92m", thing, "\033[0m")


def f1(var):
    return var[0]+var[1]-2  # <= 0


def f2(var):
    return np.power(var[0], 2)-var[1]  # <= 0


def f3(var):
    return -var[2]


def startingPoints(cubeConstraints, funConstraints, pointsToGenerate):

    # liczba wspolrzednych
    points = int(len(cubeConstraints))

    # liczba funkcji ograniczen
    functions = int(len(funConstraints))

    # przygotowanie list
    variables = [None] * points
    result = [None] * functions

    # zmienna do zliczania liczby prob generowania wspolrzednych
    counter = 0

    # losowanie wspolrzednych punktu do skutku
    while True:

        # flaga wyjscia z petli
        exitFlag = True

        # zwiekszenie licznika prob
        counter += 1

        # losowanie wspolrzednych
        for it in range(0, points):

            # poczatek zakresu losowania
            startValue = cubeConstraints[it][0]

            # koniec zakresu losowania
            endValue = cubeConstraints[it][1]

            # losowanie
            variables[it] = np.random.uniform(startValue, endValue)

        # print("Wylosowano: x=", variables[0], " y=", variables[1])
        '''fig, ax = plt.subplots()

        n = np.linspace(-5, 5, 100)
        fun1 = []
        fun2 = []
        fun3 = []

        z = [0] * 100

        for i in n:
            fun1.append(i**2)
            fun2.append(2-i)
            # fun3.append(i+1)

        ax = plt.axes(projection='3d')
        ax.plot3D(n, fun1, z)
        ax.plot3D(n, fun2, z)
        #ax.plot3D(n, fun3, z)
        ax.scatter3D(variables[0], variables[1], variables[2])
        ax.grid(True)

        plt.show()'''

        # sprawdzenie, czy wylosowane wspolrzedne znajduja sie w obszarze ograniczonym funkcjami
        for it in range(0, functions):
            result[it] = funConstraints[it](variables)

            # pierwsza funkcja, ktora zwroci wartosc spoza obszaru powoduje powtorzenie losowania wspolrzednych
            if result[it] > 0:
                # print("losowanie nieudane: f", it+1, " result: ", result[it], " aaa: ", result[0])
                nextFlag = False
                break

        # zabezpieczenie przed nieplanowanym zapetleniem programu
        if counter >= 100:
            info("za dużo iteracji")
            break

        # jezeli wylosowane wspolrzedne sa poprawne, to sa zwracane
        if exitFlag:

            '''
            fig, ax = plt.subplots()

            n = np.linspace(-5, 5, 100)
            fun1 = []
            fun2 = []

            for i in n:
                fun1.append(i**2)
                fun2.append(2-i)

            ax.plot(n, fun1)
            ax.plot(n, fun2)
            ax.scatter(variables[0], variables[1])
            ax.grid(True)

            plt.show()'''

            print("Za podejsciem: ", counter)
            break
    return variables


def main():

    cubeConstraints = [(-2, 2), (0, 4), (-1, 1)]
    funConstraints = [f1, f2, f3]

    var = startingPoints(cubeConstraints, funConstraints)

    print(var)


main()
