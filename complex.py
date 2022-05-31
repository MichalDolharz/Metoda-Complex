from contextlib import AbstractAsyncContextManager
from re import A
import matplotlib.pyplot as plt
import numpy as np
from point import Point
from typing import Callable, List
import sympy as sp
from sympy.solvers.solveset import solvify
from copy import *


class Complex():
    def __init__(self):
        self.points = []
        self.pointsCount = 0
        self.xCount = 0
        self.epsilon = 0
        self.stop = False

    # Ustawia wartości do zmiennych Complexu
    def set(self, new_points):
        self.points = new_points
        self.pointsCount = len(new_points)
        # self.xCount = len(new_points[0])

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
    def correctPoint(self, point, constraintsFuns, cubeConstraints):
        # sprawdzenie, czy wylosowane wspolrzedne znajduja sie w obszarze ograniczonym funkcjami
        again = True
        while again:  # x_var_it <= self.x_variables:

            # Funkcja zwraca wartosci:
            #   – True, jezeli punkt spelnia warunki ograniczen
            #   – False, jezeli punkt nie spelnia chociaz jednej funkcji ograniczen
            again = not(self.checkConstraints(
                point, constraintsFuns, cubeConstraints))

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
                self.moveHalfwayToCentrum(point)

        # jezeli punkt spelnia ograniczenia, to program wychodzi z petli while i zwraca ten punkt
        return point

    def addPointToComplex(self, constraintsFuns, cubeConstraints):
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

    def run(self, objFunction, constraintsFuns, cubeConstraints, max_it):

        counter = 0
        step_program = []

        # KROK 2,3
        # dopoki warunek stopu nie jest spelniony
        while (self.convergence() == False):
            # self.plotPolygon(objFunction)
            # self.display()

            # KROK 4
            # znajdz najgorszy punkt
            ten_konkretny_point = self.getWorstPoint(objFunction)

            # print("przed funkcją: ", end='')
            # ten_konkretny_point.display()

            # KROK 5
            # znajdz centroid
            centroid = self.centroid(ten_konkretny_point)

            # sprawdz, czy centroid znajduje sie w obszarze dopuszczalnym
            # jezeli nie, to dodaje punkt i wraca do poczatku petli
            if not(self.checkFunConstraints(centroid, constraintsFuns)):
                self.addPointToComplex(constraintsFuns, cubeConstraints)
                continue

            # KROK 6
            # print("krok 6")
            # self.plotPolygon(objFunction)
            # odbij najgorszy punkt wzgledem centroidu
            self.reflect(centroid, ten_konkretny_point)

            # dopoki odbity punkt nie znajduje sie w obszarze dopuszczalnym
            # to bedzie poprawiany wewnatrz petli
            while not(self.checkConstraints(ten_konkretny_point, constraintsFuns, cubeConstraints)):
                # self.plotPolygon(objFunction)
                # KROK 7
                # print("krok 7")
                # sprawdz, ktory typ ograniczen nie jest spelniany
                con = self.checkWhichConstraints(
                    ten_konkretny_point, constraintsFuns, cubeConstraints)

                # print("Krok 7, ", con)
                match con:
                    case 'functions':
                        # przesuniecie do centroidu o polowe odleglosci

                        self.contract(ten_konkretny_point, centroid)

                    case 'cube':
                        # przyjecie skrajnych wartosci ograniczen
                        self.correctCubeConstraints(
                            ten_konkretny_point, cubeConstraints)

            # KROK 8
            # znajdz, jaki teraz jest najgorszy punkt
            new_worst_point = self.getWorstPoint(objFunction)

            # dopoki odbity punkt nadal jest tym najgorszym
            # to jest przesuwany w kierunku centroidu

            while ten_konkretny_point == new_worst_point:

                self.contract(ten_konkretny_point, centroid)

                # znajdz, jaki teraz jest najgorszy punkt
                new_worst_point = self.getWorstPoint(objFunction)

            # jezeli program wyszedl z petli while, to znaczy, ze jest zaakceptowany
            # i procedura zaczyna sie od nowa

            counter += 1
            if counter == max_it:
                print("Osiągnięto limit iteracji")
                break
            if counter % 500 == 0:
                # print("Counter ", counter)
                self.plotPolygon(objFunction)
                self.addPointToComplex(constraintsFuns, cubeConstraints)
                # self.plotPolygon(objFunction)

            step_program.append(deepcopy(self))
            # step_program[-1].display()

        # zwraca id optymalnego punktu, ktory daje najlepsza (najmniejsza) wartosc funkcji celu
        best_point = self.getBestPoint(objFunction)
        print("\nLiczba iteracji algorytmu:", counter)
        print("Liczba punktów na koniec:", self.pointsCount)
        return best_point, step_program

    def weights(self, objFunction):
        x1, x2, x3, x4, x5 = point.get_xi()
        for point in self.points:
            print(point.getID(), " - ", objFunction(x1, x2, x3, x4, x5))

    def correctCubeConstraints(self, point, cubeConstraints):

        p = point.get()

        # ograniczenia wpolrzednych
        for it in range(0, self.xCount):
            if p[it] < cubeConstraints[it][0]:
                p[it] = cubeConstraints[it][0]
            elif p[it] > cubeConstraints[it][1]:
                p[it] = cubeConstraints[it][1]

        point.set(p)

    def shrink(self, objFunction):

        best_point = self.getBestPoint(objFunction)

        for point in self.points:
            self.moveHalfwayTo(point, best_point)

    # sprawdza, jakiego typu ograniczen nie spelnia podany punkt

    def checkWhichConstraints(self, point, constraintsFuns, cubeConstraints):

        cubeFlag = False
        funFlag = False

        # ograniczenia funkcyjne
        funFlag = self.checkFunConstraints(point, constraintsFuns)
        if funFlag == False:
            return 'functions'

        # ograniczenia wpolrzednych
        cubeFlag = self.checkCubeConstraints(point, cubeConstraints)
        if cubeFlag == False:
            return 'cube'

        return 'none'

    def contract(self, point, centroid):
        self.moveHalfwayToCentroid(point, centroid)

    # sprawdza, czy punkt spelnia ograniczenia
    # Funkcja zwraca wartosci:
    #   – True, jezeli punkt spelnia warunki ograniczen
    #   – False, jezeli nie spelnia ograniczen

    def checkConstraints(self, point, constraintsFuns, cubeConstraints):
        if self.checkFunConstraints(point, constraintsFuns) and self.checkCubeConstraints(point, cubeConstraints):
            return True
        else:
            return False

    # sprawdza, czy dany punkt spelnia warunki ograniczen wspolrzednych
    # Funkcja zwraca wartosci:
    #   – True, jezeli punkt spelnia warunki ograniczen
    #   – False, jezeli chociaz jedna wspolrzedna nie spelnia ograniczen
    def checkCubeConstraints(self, point, cubeConstraints):

        p = point.get()

        # ograniczenia wpolrzednych
        for it in range(0, self.xCount):
            if p[it] < cubeConstraints[it][0] or p[it] > cubeConstraints[it][1]:
                return False

        # jezeli spelnia wszystkie ograniczenia wspolrzednych
        return True

    # sprawdza, czy dany punkt spelnia warunki ograniczen funkcyjnych
    # Funkcja zwraca wartosci:
    #   – True, jezeli punkt spelnia warunki ograniczen
    #   – False, jezeli punkt nie spelnia chociaz jednej funkcji ograniczen
    def checkFunConstraints(self, point, constraintsFuns):

        # sprawdza, czy punkt spelnia wszystkie funkcje ograniczen
        for function in constraintsFuns:
            x1, x2, x3, x4, x5 = point.get_xi()
            result = function(x1, x2, x3, x4, x5)

            # pierwsza funkcja ograniczen, ktora zwroci wartosc spoza obszaru powoduje zwrocenie wartosci True
            if result > 0:
                return False

        # jezeli punkt spelnia wszystkie funkcje ograniczen, to zwracana jest wartosc False
        return True

    # odbija punkt wzgledem centroidu
    def reflect(self, centroid, point):

        # pobranie wspolrzednych
        p = point.get()
        c = centroid.get()

        # wspolczynnik odbicia
        alpha = 1.3

        # nowe wspolrzedne
        x = []

        # odbicie
        for x_it in range(0, self.xCount):
            x.append((1+alpha)*c[x_it] - p[x_it]*alpha)

        # zapisanie nowych wspolrzednych
        point.set(x)
        # return Point(x, point.getID())  # -100)

    # przesuwa punkt do centrum o polowe odleglosci

    def moveHalfwayToCentrum(self, point):
        centrum = self.centrum()
        self.moveHalfwayTo(point, centrum)

    # przesuwa punkt do centroidu o polowe odleglosci
    def moveHalfwayToCentroid(self, point, centroid):
        self.moveHalfwayTo(point, centroid)

    # przesuwa punkt do drugiego punktu (niekoniecznie centroidu lub centrum) o polowe odleglosci
    def moveHalfwayTo(self, point_p, c_p):

        new_x = []

        point = point_p.get()
        point_id = point_p.getID()

        c = c_p.get()

        # dla kolejnych wspolrzednych
        for x_it in range(0, self.xCount):

            # obliczenie polowy odleglosci wspolrzednej
            x_trans = 0.5*(c[x_it] - point[x_it])
            # x_trans = 0.5*(point[x_it] - c[x_it])

            # ustalenie nowej wartosci wspolrzednej, juz po przesunieciu
            new_x.append(c[x_it]-x_trans)
            # new_point.append(point[x_it]-x_trans)

        point_p.set(new_x)

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

    def plotObjFun(self, constraintsFunsString, cubeConstraints, ax):

        n = []
        N = 100

        n_x2 = np.linspace(cubeConstraints[1][0], cubeConstraints[1][1], N)

        # dla x1
        n.append(np.linspace(cubeConstraints[0][0], cubeConstraints[0][1], N))
        # od x3 do x5 (bez x2, bo on jest obliczany i wyświetlany)
        for it in range(2, len(cubeConstraints)):
            n.append(np.linspace(
                cubeConstraints[it][0], cubeConstraints[it][1], N))

        # wszystkie możliwe zmienne
        x1, x2, x3, x4, x5 = sp.symbols("x1, x2, x3, x4, x5")
        xs = [x1, x3, x4, x5]
        funs = []
        for it in range(0, len(constraintsFunsString)):
            fun = []
            expr = sp.parse_expr(constraintsFunsString[it])

            if x1 in expr.free_symbols and len(expr.free_symbols) == 1:
                tmp = []
                equation = sp.Eq(expr, 0)
                for ni in n_x2:
                    solution = solvify(equation, x1, sp.Reals)
                    tmp.append(solution[0])
                ax.plot(tmp, n_x2, 'k')

            elif x1 in expr.free_symbols and x2 in expr.free_symbols:
                for jt in range(0, N):
                    expr2 = expr.subs(
                        [(x1, n[0][jt]), (x3, n[1][jt]), (x4, n[2][jt]), (x5, n[3][jt])])

                    equation = sp.Eq(expr2, 0)
                    solution = solvify(equation, x2, sp.Complexes)
                    if sp.im(solution[0]):
                        tmp = []
                        tmp.append(sp.re(solution[0]))
                        solution = tmp[:]
                    fun.append(solution[0])

                funs.append(fun)

                ax.plot(n[0], fun, 'k')

    # rysuje wielokat
    def plotPolygon(self, objFunction, constraintsFunsString, tmp_cubeConstraints, print=False):

        fig, ax = plt.subplots()
        ax.set_title('')
        ax.set_xlabel('x1')
        ax.set_ylabel('x2')
        ax.grid(True)

        # rysuje funkcje ograniczen
        self.plotObjFun(constraintsFunsString, tmp_cubeConstraints, ax)

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

        if print:
            plt.show()

    # rysuje wielokat ponownie
    # przydatne do wyświetlania wykresu dla danego kroku

    def plotStepPolygon(self, points, objFunction):
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
        if print:
            plt.show()

    # sortuje punkt wedlug phi

    def sortByPolar(self):

        n = self.pointsCount

        it = 0
        while it < n-1:
            phi1 = self.points[it].getPhi()
            phi2 = self.points[it+1].getPhi()
            if phi1 > phi2:
                self.swap(self.points[it], self.points[it+1])

            it += 1
        n -= 1

        while n > 1:
            it = 0
            while it < n-1:
                phi1 = self.points[it].getPhi()
                phi2 = self.points[it+1].getPhi()
                if phi1 > phi2:
                    self.swap(self.points[it], self.points[it+1])
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

    # zwraca parametr r (wspolrzedne biegunowe)
    def rDist(self, polar_x):

        sum = 0
        for x_var_it in range(0, self.xCount):
            sum = np.power(polar_x[x_var_it], 2)

        return np.sqrt(sum)

    # zwraca parametr phi (wspolrzedne biegunowe)
    def phiAngle(self, c, p):

        return np.arctan2(p[0], p[1])

    def getPointFromID(self, id):

        if id > self.pointsCount:
            print("BLAD! Nie ma punktu o takim ID")
            return "BLAD! Nie ma punktu o takim ID"

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
        else:
            return False

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
        # self.display()

        # print("Worst_point: ", end='')
        # worst_point.display()
        # lista wspolrzednych centroidu
        c = []

        # sumowanie wspolrzednych kazdego punktu poza tym najgorszym
        for point in self.points:

            # print("Teraz punkt: ", end='')
            # point.display()

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
        # print("SZUKAM NAJGORSZEGO PUNKTU")
        f_max = np.NINF
        rtn_point = None

        for point in self.points:
            value = self.objFunValue(objFunction, point)
            # print("    - wartosc dla punktu ", point.getID(), " : ", value)
            if value > f_max:
                f_max = value
                rtn_point = point

        return rtn_point

    # zwraca punkt o najmniejszej wartosci funkcji celu
    def getBestPoint(self, objFunction):

        f_min = 10000000000
        rtn_point = None

        for point in self.points:  # tmp_point:
            value = self.objFunValue(objFunction, point)
            if value < f_min:
                f_min = value
                rtn_point = point

        return rtn_point

    # zwraca punkt o najmniejszej wartosci funkcji celu
    def getFmin(self, objFunction):

        f_min = 10000000000
        rtn_point = None

        for point in self.points:  # tmp_point:
            value = self.objFunValue(objFunction, point)
            if value < f_min:
                f_min = value
                rtn_point = point

        return f_min

    # funkcja celu, zwraca wartosc dla danego punktu
    def objFunValue(self, objFun, point):
        x1, x2, x3, x4, x5 = point.get_xi()
        return objFun(x1, x2, x3, x4, x5)

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

    # zwraca tablice punktow complexu (listy)
    def get(self):
        tmp = []
        for it in range(0, len(self.points)):
            tmp.append((self.points[it]).get())

        return tmp
