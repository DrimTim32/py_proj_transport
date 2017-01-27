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

    @property
    def name(self):
        return self.__name
