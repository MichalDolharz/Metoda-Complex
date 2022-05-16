import matplotlib.pyplot as plt
import numpy as np


class Point():
    def __init__(self, x, id):

        # id punktu
        self.id = id
        self.x = x

    def display(self):

        for it in range(0, len(self.x)):
            if self.x[it] < 0:
                eqStr = "="
            else:
                eqStr = "= "
            print(" x" + str(it), eqStr, '%.12f' %
                  (self.x[it]), end='')

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
