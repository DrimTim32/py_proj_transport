import numpy as np


class PoissonPassengerGenerator:
    def __init__(self, data):
        self.__data = data

    def generate(self, origin, destination):
        return np.random.poisson(self.__data[origin][destination] / 60)
