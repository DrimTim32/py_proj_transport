class PassengersGroup:
    """
        Group of passengers going to the same bus stop
    """

    def __init__(self, destination, count):
        """
        Inits passenger group
        :param destination: destination stop name
        :param count: how much passengers are going to destination
        """
        self.destination = destination
        self.count = count

    def __add__(self, other):
        """
        :param other:
         :type other: PassengersGroup
        :return:
        """
        if self.destination != other.destination and not isinstance(other, PassengersGroup):
            raise Exception

        return PassengersGroup(self.destination, self.count + other.count)
