from contextlib import AbstractAsyncContextManager
from re import A
import matplotlib.pyplot as plt
import numpy as np
from point import Point


class Complex():
    def __init__(self):
        self.points = []
        self.pointsCount = 0
        self.xCount = 0
        self.epsilon = 0
        self.stop = False

    def fill(self, cubeConstraints, constraintsFuns, objFunction, epsilon):

        # wartosc do warunku stopu
        self.epsilon = epsilon

        # liczba wspolrzednych, zaklada sie, ze kazda wsp. ma ograniczenia
        self.xCount = int(len(cubeConstraints))

        # liczba punktow
        points = self.xCount + 2

        for point_it in range(0, points):

            # print("=====================================")
            # print("Punkt", point_it)
            # tablica na wspolrzedne o dlugosci liczby wspolrzednych (x0, x1, x2...)
            x = [None] * self.xCount

            # liczba funkcji ograniczen
            functions = int(len(constraintsFuns))

            # przygotowanie list
            result = [None] * functions

            # losowanie wspolrzednych pierwszego punktu
            for it in range(0, self.xCount):

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

            tmp_point = Point(x, point_it)

            self.addPoint(tmp_point, constraintsFuns, cubeConstraints)

    # Dodaje podany punkt do complexu. Sprawdza, czy znajduje sie w obszarze dopuszczalnym, jezeli nie, to go poprawia
    def addPoint(self, point, constraintsFuns, cubeConstraints):

        point = self.correctPoint(point, constraintsFuns, cubeConstraints)
        self.points.append(
            Point(point.get(), point.getID()))

        self.pointsCount += 1

    # Sprawdza, czy podany punkt znajduje sie w obszarze dopuszczalnym,
    #   – jezeli nie, to go poprawia i zwraca
    #   – jezeli tak, to po prostu go zwraca bez zmian
    def correctPoint(self, point, constraintsFuns, cubeConstraints=None):
        # sprawdzenie, czy wylosowane wspolrzedne znajduja sie w obszarze ograniczonym funkcjami
        again = True
        while again:  # x_var_it <= self.x_variables:

            # Funkcja zwraca wartosci:
            #   – False, jezeli punkt spelnia warunki ograniczen
            #   – True, jezeli punkt nie spelnia chociaz jednej funkcji ograniczen
            again = self.checkConstraints(
                point, constraintsFuns)

            # jezeli punkt nie spelnia ograniczen, to
            # w przypadku pierwszego punktu losowanie tego punktu jest powtarzane
            if point.getID() == 0 and again:
                for it in range(0, self.xCount):
                    l = cubeConstraints[it][0]
                    u = cubeConstraints[it][1]
                new_x = []
                for x0_it in range(0, self.xCount):
                    new_x.append(np.random.uniform(l, u))

                point.set(new_x)

            # jezeli punkt nie spelnia ograniczen, to
            # w przypadku kazdego innego punktu jest on przesuwany w strone centrum zaakceptowanych juz punktow o polowe odleglosci
            elif point.getID() != 0 and again:
                point = self.moveHalfwayToCentrum(point)

        # jezeli punkt spelnia ograniczenia, to program wychodzi z petli while i zwraca ten punkt
        return point

    def addPointToComplex(self, objFunction, constraintsFuns, cubeConstraints):
        x = []

        for x_it in range(0, self.xCount):
            l = cubeConstraints[x_it][0]
            u = cubeConstraints[x_it][1]
            r = np.random.uniform(0, 1)
            x.append(u + r * abs(u - l))
        # jako ID wystarczy podac aktualna liczbe punktow, poniewaz ID jest liczone od zera
        tmp_point = Point(x, self.pointsCount)

        self.addPoint(tmp_point, constraintsFuns, cubeConstraints)

    # uruchamia algorytm

    def run(self, objFunction, constraintsFuns, cubeConstraints):

        # dopoki warunek stopu nie jest spelniony
        while (self.convergence() == False):

            # znajdz najgorszy punkt
            x_w = self.getWorstPoint()

            # znajdz centroid
            centroid = self.centroid(x_w)

            # sprawdz, czy centroid znajduje sie w obszarze dopuszczalnym

        # zwraca id optymalnego punktu, ktory daje najlepsza (najmniejsza) wartosc funkcji celu
        best_point_id = self.getBestPoint()

    # sprawdza, czy dany punkt znajduje sie w obszarze dopuszczalnym
    def checkConstraints(self, point, constraintsFuns):

        # sprawdza, czy punkt spelnia wszystkie funkcje ograniczen
        for function in constraintsFuns:
            result = function(point.get())

            # pierwsza funkcja ograniczen, ktora zwroci wartosc spoza obszaru powoduje zwrocenie wartosci True
            if result > 0:
                return True

        # jezeli punkt spelnia wszystkie funkcje ograniczen, to zwracana jest wartosc False
        return False

    def reflect2(self, centroid):

        p = self.points[0]
        c = centroid.get()
        pp = p.get()

        alpha = 1.3

        # x = c[:]
        x = []

        print("\nc", c)
        for x_it in range(0, self.xCount):
            # x[x_it] += (1+alpha)*c[x_it] - pp[x_it]*alpha
            x.append((1+alpha)*c[x_it] - pp[x_it]*alpha)

        print("\nx:", x)

        self.points[0].set(x)
        self.points[0].display()

    def reflect(self, centroid, point):

        p = point.get()
        c = centroid.get()

        alpha = 1.3

        x = []

        for x_it in self.xCount:
            x.append((1-alpha)*c[x_it] - p[x_it])

        point.set(x)

    # przesuwa punkt do centrum o polowe odleglosci
    def moveHalfwayToCentrum(self, point):
        centrum = self.centrum()
        return self.moveHalfwayTo(point, centrum)

    # przesuwa punkt do centroidu o polowe odleglosci
    def moveHalfwayToCentroid(self, point, objFun):
        worst_point = self.getWorstPoint(objFun)
        centroid = self.centroid(worst_point)
        return self.moveHalfwayTo(point, centroid)

    # przesuwa punkt do drugiego punktu (niekoniecznie centroidu lub centrum) o polowe odleglosci
    def moveHalfwayTo(self, point_p, c_p):

        new_point = []

        point = point_p.get()
        point_id = point_p.getID()

        c = c_p.get()

        # dla kolejnych wspolrzednych
        for x_it in range(0, self.xCount):

            # obliczenie polowy odleglosci wspolrzednej
            x_trans = 0.5*abs(point[x_it] - c[x_it])

            # ustalenie nowej wartosci wspolrzednej, juz po przesunieciu
            new_point.append(point[x_it]-x_trans)

        return Point(new_point, point_id)

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

        worst_point = self.getWorstPoint(objFunction)

        # rysuje centroid
        centroid_p = self.centroid(worst_point)
        centroid = centroid_p.get()
        ax.scatter(centroid[0], centroid[1])

        # wyznacza centrum, potrzebne do wyznaczenia wsp. biegunowych
        centrum = self.centrum()

        # aktualizuje wsp. biegunowe
        self.refreshPolar(centrum)

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
            for x_it in range(0, self.xCount):
                polar_x[x_it] = polar_x[x_it]-c[x_it]

            # wyznacza phi oraz r w ukladzie kartezjanskim
            phi = self.phiAngle(c, polar_x)
            r = self.rDist(polar_x)

            point.setPolar(r, phi)

    # zwraca parametr r (wspolrzedne biedunowe)
    def rDist(self, polar_x):

        sum = 0
        for x_var_it in range(0, self.xCount):
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
        for x in range(0, self.xCount):
            distance += np.power(p1[x] - p2[x], 2)

        return np.sqrt(distance)

    def distX(self, point1, point2, x_num):
        p1 = point1.get()
        p2 = point2.get()

        return abs(p1[x_num]-p2[x_num])

    # sprawdza, czy kryterium stopu jest spelnione
    def convergence(self):

        if self.checkSidesLen() <= self.epsilon:
            return True

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

    # liczy centroid, czyli srodek wielokatu nie zawierajacego punktu dajacego najwieksza wartosc funkcji celu
    def centroid(self, worst_point):

        # lista zsumowanych poszczegolnych wspolrzednych
        sum_x_var = [0] * self.xCount

        # lista wspolrzednych centroidu
        c = []

        # sumowanie wspolrzednych kazdego punktu poza tym najgorszym
        for point in self.points:

            # jezeli nie jest liczone centrum, to liczony jest centroid,
            # wtedy nie bierzemy pod uwage najgorszego punktu
            if point.getID() == worst_point.getID():
                # pominiecie aktualnej iteracji petli for
                continue

            # wlasciwe sumowanie wspolrzednych punktow
            for x_var_it in range(0, self.xCount):
                sum_x_var[x_var_it] += (point.get())[x_var_it]

        # przypisanie punktowi c (centroid) jego wspolrzednych
        # wspolrzedne to srednia algebraiczna wspolrzednych punktow wierzcholkow
        for it in range(0, self.xCount):
            c.append(sum_x_var[it]/(self.pointsCount - 1))

        return Point(c, -1)

    # liczy centroid, czyli srodek wielokatu skladajacego sie ze wszystkich punktow
    def centrum(self):

        # lista zsumowanych poszczegolnych wspolrzednych
        sum_x_var = [0] * self.xCount

        # lista wspolrzednych centroidu
        c = []

        # sumowanie wspolrzednych kazdego punktu
        for point in self.points:

            # wlasciwe sumowanie wspolrzednych punktow
            for x_var_it in range(0, self.xCount):
                sum_x_var[x_var_it] += (point.get())[x_var_it]

        # przypisanie punktowi c (centrum) jego wspolrzednych
        # wspolrzedne to srednia algebraiczna wspolrzednych punktow wierzcholkow
        for it in range(0, self.xCount):
            c.append(sum_x_var[it]/self.pointsCount)

        return Point(c, -1)

    # zwraca punkt o najwiekszej wartosci funkcji celu
    def getWorstPoint(self, objFunction):

        f_max = 0
        rtn_point = None

        for point in self.points:
            value = self.objFunValue(objFunction, point.get())
            if value > f_max:
                f_max = value
                rtn_point = point

        return rtn_point

    # zwraca punkt o najmniejszej wartosci funkcji celu
    def getBestPoint(self, objFunction):

        f_min = 10000000000
        rtn_point = None

        for point in self.points:  # tmp_point:
            value = self.objFunValue(objFunction, point.get())
            if value < f_min:
                f_min = value
                rtn_point = point

        return rtn_point

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
