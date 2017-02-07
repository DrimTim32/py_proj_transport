from __future__ import division
"""
File containing PoissonPassengerGenerator class
"""
import numpy as np

class PoissonPassengerGenerator:
    """
    Basic passenger generator class based on poisson distribution
    """

    def __init__(self, data):
        """
        Initializes generator with statistical data about passenger traffic
        :param data: data with means
        :type: data: dict[str, dict[str, int]]
        """
        self.__data = data

    def generate(self, origin, destination):
        """
        Generates passengers
        :param origin: origin stop name
        :param destination: destination stop name
        :type origin: str
        :type destination: str
        :return: how many passengers heading to deastination stop will be added to origin stop
        :rtype: int
        """
        return np.random.poisson(self.__data[origin][destination] / 60)
