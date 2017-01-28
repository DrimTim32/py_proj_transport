from random import shuffle

from core.simulation.passenger_group import PassengersGroup

"""
File containing Bus class
"""


class Bus:
    """
        Bus class
    """
    BUS_COUNTER = 0

    def __init__(self, line, route):
        """
        :param line: line on which bus will operate
        :param route: bus route on line
        :type line: Line
        :type route: int
        """
        Bus.BUS_COUNTER += 1
        self.passengers = []
        self.__line = line
        self.__current_stop = 0
        self.__route = route
        self.__current_stop_name = self.line.routes[self.route][self.current_stop].name
        self.__next_stop_name = self.line.routes[self.route][self.current_stop + 1].name
        self.__id = Bus.BUS_COUNTER
        self.__time_to_next_stop_base = self.line.routes[self.route][self.current_stop].time_to_next_stop
        self.__ticks_count = 0
        self.__route_len = len(self.line.routes[self.route])

    @property
    def route(self):
        """
        :return: bus route index
        :rtype: int
        """
        return self.__route

    @property
    def current_stop_name(self):
        """
        :return: name of the current stop
        :rtype: str
        """
        return self.__current_stop_name

    @property
    def next_stop_name(self):
        """
        :return: name of the next stop
        :rtype: str
        """
        return self.__next_stop_name

    @property
    def id(self):
        """
        :return: bus id
        :rtype: int
        """
        return self.__id

    @property
    def current_stop(self):
        """
        :return: current stop index
        :rtype: int
        """
        return self.__current_stop

    @property
    def line(self):
        """
        :return: bus line
        :rtype: Line
        """
        return self.__line

    def move(self):
        """
        Performs move to next position on bus
        :rtype: None
        :return: mone
        """
        if self.time_to_next_stop == 1:
            self.__current_stop_name = self.next_stop_name
            self.__next_stop_name = self.line.routes[self.route][
                self.__current_stop + 2].name if self.current_stop < self.__route_len - 2 else "None"
        if self.time_to_next_stop == 0:
            self.__current_stop += 1
            if self.__current_stop == self.__route_len:
                return
            self.__time_to_next_stop_base = self.line.routes[self.route][self.current_stop].time_to_next_stop
            self.__ticks_count = 0
        else:
            self.__ticks_count += 1

    def fill(self, passenger_groups):
        """
        Fills bus with passengers from passenger groups
        :param passenger_groups: array of passenger groups
        :type passenger_groups list[PassengersGroup]
        :rtype: list{PassengersGroup]
        :return: list of passengers groups of passengers who didn't fit into the bus
        """
        count = self.count
        in_count = 0
        space = self.line.bus_capacity - count
        for group in passenger_groups:
            in_count += group.count
        if space >= in_count:
            for stop_group in passenger_groups:
                i = 0
                while i in range(len(self.passengers)):
                    bus_group = self.passengers[i]
                    if bus_group.destination == stop_group.destination:
                        bus_group += stop_group
                        break
                    i += 1
                if i == len(self.passengers):
                    self.passengers.append(stop_group)
            return []
        else:
            passengers = []
            for group in passenger_groups:
                passengers += [group.destination] * group.count
            shuffle(passengers)

            lucky_passengers = passengers[0:space]
            Bus.__fill_with_groups(lucky_passengers, self.passengers)
            passengers = passengers[space:]
            not_lucky_passenger_groups = []
            Bus.__fill_with_groups(passengers, not_lucky_passenger_groups)
            return not_lucky_passenger_groups

    @staticmethod
    def __fill_with_groups(passengers, group_list):
        """
        fills group_list with PassengersGrpups made from passenegers
        :param passengers: list of destination stop names, one for every passenger
        :param group_list:
        :type passengers: list[str]
        :type group_list: list[PassengersGroup]
        :return:
        """
        for passenger in passengers:
            i = 0
            while i in range(len(group_list)):
                group = group_list[i]
                if passenger == group.destination:
                    group.count += 1
                    break
                i += 1
            if i == len(group_list):
                group_list.append(PassengersGroup(passenger, 1))
    @property
    def count(self):
        """
        :return: number of passengers in bus
        :rtype: int
        """
        c = 0
        for group in self.passengers:
            c += group.count
        return c

    @property
    def time_to_next_stop(self):
        """
        :rtype: int
        :return: time to next stop in ticks
        """
        return self.__time_to_next_stop_base - self.__ticks_count
