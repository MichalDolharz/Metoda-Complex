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

    def display(self):

        for it in range(0, len(self.x)):
            if self.x[it] < 0:
                eqStr = "="
            else:
                eqStr = "= "
            print(" x" + str(it), eqStr, '%.12f' %
                  (self.x[it]), end='')

    def setID(self, new_id):
        self.id = new_id

    def set(self, new_x):
        self.x = new_x

    def getID(self):
        return self.id

    # zwraca tablice wspolrzednych punktu
    def get(self):
        return self.x

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
