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
        c = 0
        for group in self.passengers:
            if group.destination == destination:
                c = group.count
                break
        return c

    @property
    def name(self):
        return self.__name
