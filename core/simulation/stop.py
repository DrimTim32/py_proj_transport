"""
File containing Bus class
"""


class Stop:
    """
    Bus Stop class
    """

    def __init__(self, name):
        """
        :param name: name of stop
        :type name: str
        """
        self.__name = name
        self.passengers = []

    def count(self, destination):
        """
        :return: number of passengers waiting for bus to specific destination
        :rtype: int
        """
        count = 0
        for group in self.passengers:
            if group.destination == destination:
                count = group.count
                break
        return count

    @property
    def name(self):
        """
        :return: name of stop
        :rtype str
        """
        return self.__name
