import matplotlib.pyplot as plt
import numpy as np


class Point():
    def __init__(self, cubeConstraints, constraintsFuns):

        # liczba wspolrzednych
        varCount = int(len(cubeConstraints))

        # liczba funkcji ograniczen
        functions = int(len(constraintsFuns))

        # przygotowanie list
        variables = [None] * varCount
        result = [None] * functions

        # zmienna do zliczania liczby prob generowania wspolrzednych
        counter = 0

        # losowanie wspolrzednych punktu do skutku
        while True:

            # flaga wyjscia z petli
            foundFlag = True

            # zwiekszenie licznika prob
            counter += 1

            # losowanie wspolrzednych
            for it in range(0, varCount):

                # poczatek zakresu losowania
                startValue = cubeConstraints[it][0]

                # koniec zakresu losowania
                endValue = cubeConstraints[it][1]

                # losowanie
                variables[it] = np.random.uniform(startValue, endValue)

            # print("Wylosowano: x=", variables[0], " y=", variables[1])

            # sprawdzenie, czy wylosowane wspolrzedne znajduja sie w obszarze ograniczonym funkcjami
            for it in range(0, functions):
                result[it] = constraintsFuns[it](variables)

                # pierwsza funkcja, ktora zwroci wartosc spoza obszaru powoduje powtorzenie losowania wspolrzednych
                if result[it] > 0:
                    # print("losowanie nieudane: f", it+1, " result: ", result[it], " aaa: ", result[0])
                    foundFlag = False
                    break

            # zabezpieczenie przed nieplanowanym zapetleniem programu
            if counter >= 100:
                print("za dużo iteracji")
                break

            # jezeli wylosowane wspolrzedne sa poprawne, to sa zwracane
            if foundFlag:
                print("Za podejsciem: ", counter)
                break

        self.var = variables

    def display(self):

        for it in range(0, len(self.var)):
            if self.var[it] < 0:
                eqStr = "="
            else:
                eqStr = "= "
            print(" x" + str(it), eqStr, '%.12f' %
                  (self.var[it]), end='')

    def get(self):
        return self.var

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
