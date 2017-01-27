class PassengersGroup:
    """
        Group of passengers going to the same bus stop
    """

    def __init__(self, destination, count):
        """
        :param destination: destination stop name
        :param count: how much passengers are going to destination
        :type count: int
        """
        self.__destination = destination
        self.count = count

    @property
    def destination(self):
        return self.__destination

    def __add__(self, other):
        """
        :param other: PassengerGroup to be added
        :type other: PassengersGroup
        :return: sum of PassengerGroups
        """
        if not isinstance(other, PassengersGroup) or self.destination != other.destination:
            raise Exception

        return PassengersGroup(self.destination, self.count + other.count)
