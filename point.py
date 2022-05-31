import matplotlib.pyplot as plt
import numpy as np


class Point():
    def __init__(self, x, id):

        # id punktu
        self.id = id
        self.x = x

        self.phi = 0
        self.r = 0

    def __eq__(p1, p2):
        if p1.getID() == p2.getID():
            return True
        else:
            return False

    def setPolar(self, arg_r, arg_phi):
        self.r = arg_r
        self.phi = arg_phi

    def getPhi(self):
        return self.phi

    def getR(self):
        return self.r

    def displayPolar(self):

        print(" r:", '%.15f' % self.r, " phi:", self.phi, end='')

    def display(self, mode='no_enter'):

        match mode:
            # wszystko w jednej linii, brak przejścia do nowej linii na końcu
            case 'no_enter':
                for it in range(0, len(self.x)):
                    if self.x[it] < 0:
                        eqStr = "="
                    else:
                        eqStr = "= "
                    print(" x" + str(it), eqStr, '%.12f' %
                          (self.x[it]), end='')
            # wszystko w jednej linii, przejście do nowej linii na końcu
            case 'enter':
                for it in range(0, len(self.x)):
                    if self.x[it] < 0:
                        eqStr = "="
                    else:
                        eqStr = "= "
                    print(" x" + str(it), eqStr, '%.12f' %
                          (self.x[it]))
                print()
            # kazda zmienna w nowej linii
            case 'multirow':
                for it in range(0, len(self.x)):
                    if self.x[it] < 0:
                        eqStr = "="
                    else:
                        eqStr = "= "
                    print(" x" + str(it), eqStr, '%.12f' %
                          (self.x[it]))

    def setID(self, new_id):
        self.id = new_id

    def set(self, new_x):
        self.x = new_x

    def getID(self):
        return self.id

    # zwraca tablice wspolrzednych punktu
    def get(self):
        return self.x[:]

    # zwraca wartości każdej wspolrzednej punktu osobno
    def get_xi(self):
        tmp = self.get()
        match len(self.get()):
            case 1:
                return tmp[0], None, None, None, None
            case 2:
                return tmp[0], tmp[1], None, None, None
            case 3:
                return tmp[0], tmp[1], tmp[2], None, None
            case 4:
                return tmp[0], tmp[1], tmp[2], tmp[3], None
            case 5:
                return tmp[0], tmp[1], tmp[2], tmp[3], tmp[4]
