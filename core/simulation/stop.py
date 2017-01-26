class Stop:
    """
    Bus Stop class
    """
    def __init__(self, name):
        """
        :param name: name of stop
        :type name: str
        """
        self.name = name
        self.passengers = []
