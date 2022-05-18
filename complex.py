from contextlib import AbstractAsyncContextManager
from re import A
import matplotlib.pyplot as plt
import numpy as np
from point import Point


class Complex():
    def __init__(self):
        self.points = []
        self.pointsCount = 0
        self.x_variables = 0
        self.epsilon = 0
        self.stop = False

    def fill(self, cubeConstraints, constraintsFuns, objFunction, epsilon):

        # wartosc do warunku stopu
        self.epsilon = epsilon

        # liczba wspolrzednych, zaklada sie, ze kazda wsp. ma ograniczenia
        self.x_variables = int(len(cubeConstraints))

        # liczba punktow
        points = self.x_variables + 2

        for point_it in range(0, points):

            # print("=====================================")
            # print("Punkt", point_it)
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

                        tmpPoint.set(new_x)

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

    # oblicza centroid, czyli "umowny" srodek obszaru simplexu

    # przesuwa podany punkt o polowe odleglosci od centrum
    def moveHalfwayToCentrum(self, x_point, objFunction):

        new_point = []

        x_p = x_point.get()
        x_p_id = x_point.getID()

        # liczy centrum (nie centroid), czyli srodek figury z dopuszczonych punktow
        c_p = self.centroid(objFunction, centrumFlag=True)
        c = c_p.get()
        # print("centrum", c_p)
        # print("punkt przed halfway", x_p)

        # dla kolejnych wspolrzednych
        for x_var_it in range(0, self.x_variables):

            new_x_var = abs(x_p[x_var_it] - c[x_var_it])
            new_x_var /= 2

            new_point.append(x_p[x_var_it]-new_x_var)
        # print("odleglosc: ", np.sqrt(new_point[0]**2 + new_point[1]**2))
        # print("punkt po halfway", new_point)
        # (self.points[x_p_id]).move(new_point)

        return Point(new_point, x_p_id)

    # laczy dwa punkty
    def connectPoints(self, ax, p1, p2):
        x_values = [p1[0], p2[0]]
        y_values = [p1[1], p2[1]]
        ax.plot(x_values, y_values, 'ko', linestyle='-')

    # laczy kolejne punkty tworzac wielokat
    def createPolygon(self, ax):
        for var_it in range(0, self.pointsCount):
            if var_it != self.pointsCount-1:
                self.connectPoints(
                    ax, self.points[var_it].get(), self.points[var_it+1].get())
            else:
                self.connectPoints(
                    ax, self.points[var_it].get(), self.points[0].get())

    # rysuje funkcje ograniczen funkcyjnych
    def plotObjFun(self, ax):
        n = np.linspace(-2, 1, 100)
        fun1 = []
        fun2 = []

        for i in n:
            fun1.append(i**2)
            fun2.append(2-i)

        ax.plot(n, fun1)
        ax.plot(n, fun2)

    # rysuje wielokat
    def plotPolygon(self, objFunction):
        fig, ax = plt.subplots()

        # rysuje funkcje ograniczen
        self.plotObjFun(ax)

        # rysuje centroid
        c_p = self.centroid(objFunction)
        c = c_p.get()
        ax.scatter(c[0], c[1])

        # wyznacza centrum, potrzebne do wyznaczenia wsp. biegunowych
        center = self.centroid(objFunction, centrumFlag=True)

        # aktualizuje wsp. biegunowe
        self.refreshPolar(center)

        # sortuje wzgledem phi
        self.sortByPolar()

        # posortowane punkty sa ze soba kolejno laczone
        self.createPolygon(ax)

        ax.grid(True)

        plt.show()

    # sortuje punkt wedlug phi
    def sortByPolar(self):

        n = self.pointsCount

        it = 0
        while it < n-1:
            phi1 = self.points[it].getPhi()
            phi2 = self.points[it+1].getPhi()
            if phi1 > phi2:
                # print("======================")
                # print(self.points[it].display())
                # print(self.points[it+1].display())
                self.swap(self.points[it], self.points[it+1])
                # print("poooooooooooooo")
                # print(self.points[it].display())
                # print(self.points[it+1].display())
                # print("\n======================")

            it += 1
        n -= 1

        while n > 1:
            it = 0
            while it < n-1:
                phi1 = self.points[it].getPhi()
                phi2 = self.points[it+1].getPhi()
                # print("phi1:", phi1)
                # print("phi2:", phi2)
                if phi1 > phi2:
                    # print("swap")
                    # print("======================")
                    # print("\nid:", self.points[it].getID(), end=' ')
                    # self.points[it].display()
                    # print("\nid:", self.points[it+1].getID(), end=' ')
                    # self.points[it+1].display()
                    self.swap(self.points[it], self.points[it+1])
                    # print("\nid:", self.points[it].getID(), end=' ')
                    # self.points[it].display()
                    # print("\nid:", self.points[it+1].getID(), end=' ')
                    # self.points[it+1].display()
                    # print("\n======================")
                it += 1
            n -= 1

    # zamienia dane dwoch punktow pozostawiajac jedynie ID
    def swap(self, p1, p2):
        id_1 = p1.getID()
        r1 = p1.getR()
        phi1 = p1.getPhi()

        id_2 = p2.getID()
        r2 = p2.getR()
        phi2 = p2.getPhi()

        tmp_point_1 = self.getPointFromID(id_1)
        tmp_point_2 = self.getPointFromID(id_2)
        tmp_point_1_x = tmp_point_1.get()
        tmp_point_2_x = tmp_point_2.get()

        self.points[id_1].set(tmp_point_2_x)
        self.points[id_2].set(tmp_point_1_x)

        self.points[id_1].setPolar(r2, phi2)
        self.points[id_2].setPolar(r1, phi1)

    # oblicza aktualne wartosci wspolrzednych biegunowych dla podanego punktu jako
    # poczatku ukladu wsp. biegunowych
    def refreshPolar(self, center):

        for point in self.points:

            c = center.get().copy()
            polar_x = point.get().copy()

            # wyznacza nowe wspolrzedne w ukladzie kartezjanskim, gdzie c jest srodkiem ukladu
            for x_it in range(0, self.x_variables):
                polar_x[x_it] = polar_x[x_it]-c[x_it]

            # wyznacza phi oraz r w ukladzie kartezjanskim
            phi = self.phiAngle(c, polar_x)
            r = self.rDist(polar_x)

            point.setPolar(r, phi)

    # zwraca parametr r (wspolrzedne biedunowe)
    def rDist(self, polar_x):

        sum = 0
        for x_var_it in range(0, self.x_variables):
            sum = np.power(polar_x[x_var_it], 2)

        return np.sqrt(sum)

    # zwraca parametr phi (wspolrzedne biedunowe)
    def phiAngle(self, c, p):

        return np.arctan2(p[0], p[1])

    def getPointFromID(self, id):

        if id > self.pointsCount:
            print("Nie ma punktu o takim ID")
            return "Nie ma punktu o takim ID"

        for point in self.points:
            if point.getID() == id:
                return point

    def dist(self, point1, point2):
        p1 = point1.get()
        p2 = point2.get()

        distance = 0
        for x in range(0, self.x_variables):
            distance += np.power(p1[x] - p2[x], 2)

        return np.sqrt(distance)

    def distX(self, point1, point2, x_num):
        p1 = point1.get()
        p2 = point2.get()

        return abs(p1[x_num]-p2[x_num])

    def checkEpsilon(self):

        if self.checkSidesLen() <= self.epsilon:
            self.stop = True

    # zwraca dlugosc najdluzszego boku wielokata
    def checkSidesLen(self):

        result = 10000
        biggest = 0
        # kazdy punkt jest laczony z kolejnym aby ustalic dlugosc tego boku
        for point_it in range(0, self.pointsCount):

            # dlugosc boku utworzonego z ostatniego i pierwszego punktu
            if point_it == self.pointsCount-1:
                result = self.dist(self.points[point_it], self.points[0])
            # dlugosc boku utworzonego z point_it oraz point_it+1 punktu
            else:
                result = self.dist(
                    self.points[point_it], self.points[point_it+1])

            # zapisuje aktualnie najwieksza dlugosc
            if result > biggest:
                biggest = result

        return biggest

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

        return Point(c, -1)

    # zwraca id punktu o najwiekszej wartosci funkcji celu
    def getWorstPointID(self, objFunction):

        f_max = 0
        id_rtn = None

        for point in self.points:  # tmp_point:
            value = self.objFunValue(objFunction, point.get())
            if value > f_max:
                f_max = value
                id_rtn = point.getID()

        return id_rtn

    # funkcja celu, zwraca wartosc dla danego punktu
    def objFunValue(self, objFun, point):
        return objFun(point)

    # wyswietla wszystkie wsp. wszystkich punktow complexu w ukladzie kartezjanskim
    def display(self):

        for point in self.points:
            print("\nPoint ID-" + str(point.getID()), end=':')
            point.display()
        print("\n")

    # wyswietla wszystkie wsp. wszystkich punktow complexu w ukladzie biegunowym
    def displayPolar(self):
        for point in self.points:
            print("\nPoint ID-" + str(point.getID()), end=':')
            point.displayPolar()
        print("\n")

    # zwraca tablice punktow complexu
    def get(self):

        tmp = []
        for it in range(0, len(self.points)):
            tmp.append((self.points[it]).get())

        return tmp
