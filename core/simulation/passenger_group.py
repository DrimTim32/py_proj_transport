"""
File containing PassengersGroup class
"""


class PassengersGroup:
    """
        Group of passengers going to the same bus stop
    """

    def __init__(self, destination, count):
        """
        :param destination: destination stop name
        :param count: number of passengers heading to destination stop
        :type count: int
        """
        if count < 0:
            raise ValueError("count must be non negative")
        if destination == "":
            raise ValueError("destination must be not empty")

        self.__destination = destination
        self.count = count

    @property
    def destination(self):
        """
        :return: destination(name of stop) of passengers from group
        :rtype: str
        """
        return self.__destination

    def __add__(self, other):
        """
        :param other: PassengersGroup to be added
        :type other: PassengersGroup
        :return: sum of PassengersGroups
        """
        if not isinstance(other, PassengersGroup):
            raise TypeError("Cannot sum two different instances")
        if self.destination != other.destination:
            raise TypeError("Cannot sum groups with two different destinations")

        return PassengersGroup(self.destination, self.count + other.count)

    def __iadd__(self, other):
        """
               :param other: PassengersGroup to be added
               :type other: PassengersGroup
               :return: sum of PassengersGroups
               """
        if not isinstance(other, PassengersGroup):
            raise TypeError("Cannot sum two different instances")
        if self.destination != other.destination:
            raise TypeError("Cannot sum groups with two different destinations")
        self.count += other.count
        return self
