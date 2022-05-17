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

            # print("=====================================")
            #print("Punkt", point_it)
            # tablica na wspolrzedne o dlugosci liczby wspolrzednych (x0, x1, x2...)
            x = [None] * self.x_variables

            # liczba funkcji ograniczen
            functions = int(len(constraintsFuns))

            # przygotowanie list
            result = [None] * functions

            # losowanie wspolrzednych pierwszego punktu
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

            tmpPoint = Point(x, point_it)

            # sprawdzenie, czy wylosowane wspolrzedne znajduja sie w obszarze ograniczonym funkcjami
            nextPointFlag = False
            while nextPointFlag == False:  # x_var_it <= self.x_variables:
                # if point_it > 0:
                #   self.plot(tmpPoint)
                # za kazdym razem sprawdza, czy wspolrzedne x spelnia wszystkie funkcje
                for it in range(0, functions):
                    result[it] = constraintsFuns[it](tmpPoint.get())

                    # w przypadku pierwszego punktu pierwsza funkcja,
                    # ktora zwroci wartosc spoza obszaru powoduje powtorzenie losowania wspolrzednych
                    if point_it == 0 and result[it] > 0:
                        # print("losowanie nieudane: f", it+1, " result: ", result[it], " aaa: ", result[0])
                        new_x = []
                        for x0_it in range(0, self.x_variables):
                            new_x.append(np.random.uniform(l, u))

                        tmpPoint.move(new_x)

                        nextPointFlag = False
                        break

                    # sprawdzenie, czy wspolrzedna punktu spelnia funkcje ograniczen
                    # (czyli czy w danej "osi" punkt "lezy w obszarze dopuszczalnym")
                    # jezeli nie, to przesuniecie w strone centrum zaakceptowanych punktow o polowe odleglosci
                    elif point_it != 0 and result[it] > 0:
                        # wyliczenie centroidu i przesuniecie punktu o polowe, sprawdzenie czy ok, jak ok to sprawdza kolejna, jak nie to przesuniecie
                        # centroid mozna liczyc wczesniej, bo dopoki nie bedzie liczony nowy punkt to centroid sie nie zmieni

                        tmpPoint = self.moveHalfwayToCentrum(
                            tmpPoint, objFunction)

                        nextPointFlag = False
                        break

                    # jezeli wspolrzedna punktu spelnia funkcje ograniczen, to jest akceptowana
                    # i program przechodzi do kolejnej wspolrzednej

                    if it == functions-1:
                        self.points.append(
                            Point(tmpPoint.get(), tmpPoint.getID()))

                        self.pointsCount += 1
                        nextPointFlag = True
            del tmpPoint
        # self.pointsCount = 4
        # self.x_variables = 2
        # self.points.append(Point([1, 1], 0))
        # self.points.append(Point([1, 2], 1))
        # self.points.append(Point([2, 2], 2))
        # self.points.append(Point([2, 1], 3))

    # oblicza centroid, czyli "umowny" srodek obszaru simplexu

    def moveHalfwayToCentrum(self, x_point, objFunction):

        new_point = []

        x_p = x_point.get()
        x_p_id = x_point.getID()

        # liczy centrum (nie centroid), czyli srodek figury z dopuszczonych punktow
        c_p = self.centroid(objFunction, centrumFlag=True)
        #print("centrum", c_p)
        #print("punkt przed halfway", x_p)

        # dla kolejnych wspolrzednych
        for x_var_it in range(0, self.x_variables):

            new_x_var = abs(x_p[x_var_it] - c_p[x_var_it])
            new_x_var /= 2

            new_point.append(x_p[x_var_it]-new_x_var)
        #print("odleglosc: ", np.sqrt(new_point[0]**2 + new_point[1]**2))
        #print("punkt po halfway", new_point)
        # (self.points[x_p_id]).move(new_point)

        return Point(new_point, x_p_id)

    # def move()

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

    def plot(self, tmpPoint):
        fig, ax = plt.subplots()

        n = np.linspace(-5, 5, 100)
        fun1 = []
        fun2 = []

        for i in n:
            fun1.append(i**2)
            fun2.append(2-i)

        ax.plot(n, fun1)
        ax.plot(n, fun2)
        #ax.scatter(variables[0], variables[1])

        for var in self.points:
            v = var.get()
            ax.scatter(v[0], v[1])

        tmpP = tmpPoint.get()
        ax.scatter(tmpP[0], tmpP[1])
        ax.grid(True)

        plt.show()

    def plot2(self):
        fig, ax = plt.subplots()

        n = np.linspace(-5, 5, 100)
        fun1 = []
        fun2 = []

        for i in n:
            fun1.append(i**2)
            fun2.append(2-i)

        ax.plot(n, fun1)
        ax.plot(n, fun2)
        #ax.scatter(variables[0], variables[1])

        for var in self.points:
            v = var.get()
            ax.scatter(v[0], v[1])

        ax.grid(True)

        plt.show()
