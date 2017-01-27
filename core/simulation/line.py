from collections import namedtuple

LineStop = namedtuple('LineStop', ['name', 'time_to_next_stop'])


class Line:
    """
    Line class
    """

    def __init__(self, line_data, route1, route2):
        """
        :param line_data: specification of line ('id', 'bus_capacity', 'frequency1', 'frequency2')
        :param route1: specification of stops on route1
        :param route2: specification of stops on route2
        :type line_data: dict
        :type route1: list[LineStop]
        :type route2: list[LineStop]
        """
        self.__number = line_data['id']
        self.__bus_capacity = line_data['bus_capacity']
        self.__frequencies = [line_data['frequency1'], line_data['frequency2']]
        self.__routes = [[LineStop('P', 1)] + route1, [LineStop('P', 1)] + route2]
        self.__last_bus = [line_data['frequency1'], line_data['frequency2']]

    @property
    def number(self):
        """
        returns line number
        :rtype: int
        """
        return self.__number

    @property
    def bus_capacity(self):
        """
        returns how many passengers can fit to buses on this line
        :rtype: int
        """
        return self.__bus_capacity

    @property
    def frequencies(self):
        """
        returns how frequent buses are being sent from depot
        :rtype: int
        """
        return self.__frequencies

    @property
    def routes(self):
        """
        returns line routes
        :rtype: list[list[LineStop]]
        """
        return self.__routes

    @property
    def last_bus(self): 
        return self.__last_bus

    def first_stop_name(self, route):
        """
        :param route: route
        :type route: int
        :return: Name of the first stop on given route
        :rtype: str
        """
        return self.routes[route][0].name

    def last_stop_name(self, route):
        """
        :param route: route
        :type route: int
        :return: Name of the last stop on given route
        :rtype: str
        """
        return self.routes[route][-1].name

    def last_stop(self, route):
        """
        :param route: route
        :type route: int
        :return: index of the last stop on given route
        :rtype: int
        """
        return len(self.routes[route]) - 1

    def tick(self):
        """
        Adds 1 to time from last bus on routes 1 and 2
        :return: if buses should be putted on routes 1 and 2
        :rtype: list[bool]
        """
        new_buses = [False, False]
        for i in range(len(self.last_bus)):
            self.last_bus[i] += 1

        for i in range(len(self.last_bus)):
            if self.last_bus[i] >= self.frequencies[i]:
                new_buses[i] = True
                self.last_bus[i] = 0

        return new_buses
