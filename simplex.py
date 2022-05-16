import matplotlib.pyplot as plt
import numpy as np
from point import Point


class Simplex():
    def __init__(self):
        self.points = []
        self.pointsCount = 0
        self.x_variables = 0

    def fill(self, cubeConstraints, constraintsFuns, objFunction):
        # liczba punktow
        self.x_variables = int(len(cubeConstraints))
        points = self.x_variables + 2

        for point_it in range(0, points):

            x = [None] * self.x_variables

            # liczba funkcji ograniczen
            functions = int(len(constraintsFuns))

            # przygotowanie list
            result = [None] * functions

            # losowanie wspolrzednych
            for it in range(0, self.x_variables):

                # poczatek zakresu losowania
                l = cubeConstraints[it][0]

                # koniec zakresu losowania
                u = cubeConstraints[it][1]

                # pierwszy punkt jest losowany w pelnym zakresie
                if point_it == 0:
                    x[it] = np.random.uniform(l, u)

                # kazdy kolejny punkt zgodnie ze wzorem (311)
                else:
                    r = np.random.uniform(0, 1)
                    x[it] = u + r * abs(u - l)

            # sprawdzenie, czy wylosowane wspolrzedne znajduja sie w obszarze ograniczonym funkcjami
            x_var_it = 0
            nextPointFlag = True
            while x_var_it <= self.x_variables:

                # za kazdym razem sprawdza, czy wspolrzedna x spelnia wszystkie funkcje
                for it in range(0, functions):
                    result[it] = constraintsFuns[it](x)

                    # w przypadku pierwszego punktu pierwsza funkcja,
                    # ktora zwroci wartosc spoza obszaru powoduje powtorzenie losowania wspolrzednych
                    if point_it == 0 and result[it] > 0:
                        # print("losowanie nieudane: f", it+1, " result: ", result[it], " aaa: ", result[0])
                        for x0_it in range(0, self.x_variables):
                            x[x0_it] = np.random.uniform(l, u)
                            nextPointFlag = False

                    elif point_it != 0 and result[it] > 0:
                        print(x)
                        # wyliczenie centroidu i przesuniecie punktu o polowe, sprawdzenie czy ok, jak ok to kolejny punkt, jak nie to przesuniecie
                        # centroid mozna liczyc wczesniej, bo dopoki nie bedzie liczony nowy punkt to centroid sie nie zmieni

                    else:
                        self.points.append(Point(x, x_var_it))
                        self.pointsCount += 1

                        # zabezpieczenie przed nieplanowanym zapetleniem programu
                if nextPointFlag == True:
                    x_var_it += 1

        # self.pointsCount = 4
        # self.x_variables = 2
        # self.points.append(Point([1, 1], 0))
        # self.points.append(Point([1, 2], 1))
        # self.points.append(Point([2, 2], 2))
        # self.points.append(Point([2, 1], 3))

    # oblicza centroid, czyli "umowny" srodek obszaru simplexu
    def centroid(self, objFunction, centrumFlag=False):

        # lista zsumowanych poszczegolnych wspolrzednych
        sum_x_var = [0] * self.x_variables

        # lista wspolrzednych centroidu
        c = []

        # ID punktu dajacego najwieksza (najgorsza) wartosc funkcji celu
        x_var_worst_id = self.getWorstPointID(objFunction)

        # k jest rowne ilosci punktow w przypadku liczenia centrum
        # jezeli jest liczony centroid, to zostanie to zmienione pozniej
        k = self.pointsCount

        # sumowanie wspolrzednych kazdego punktu poza tym najgorszym
        for point in self.points:

            # jezeli nie jest liczone centrum, to liczony jest centroid,
            # wtedy nie bierzemy pod uwage najgorszego punktu
            if not(centrumFlag) and point.id == x_var_worst_id:
                k = self.pointsCount - 1

                # pominiecie aktualnej iteracji petli for
                continue

            # wlasciwe sumowanie wspolrzednych punktow
            for x_var_it in range(0, self.x_variables):
                sum_x_var[x_var_it] += (point.get())[x_var_it]

        # przypisanie punktowi c (centroid/centrum) jego wspolrzednych
        # wspolrzedne to srednia algebraiczna wspolrzednych punktow wierzcholkow
        for it in range(0, self.x_variables):
            c.append(sum_x_var[it]/k)

        return c

    # zwraca id punktu o najwiekszej wartosci funkcji celu
    def getWorstPointID(self, objFunction):
        values = []

        f_max = 0
        id_rtn = None

        for point in self.points:  # tmp_point:
            values.append(self.objFunValue(objFunction, point.x))
            if values[-1] > f_max:
                f_max = values[-1]
                id_rtn = point.id

        return id_rtn

    def objFunValue(self, objFun, args):
        return objFun(args)

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
