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
        return self.__route

    @property
    def current_stop_name(self):
        return self.__current_stop_name

    @property
    def next_stop_name(self):
        return self.__next_stop_name

    @property
    def id(self):
        return self.__id

    @property
    def current_stop(self):
        return self.__current_stop

    @property
    def line(self):
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

    @property
    def time_to_next_stop(self):
        """
        :rtype: int
        :return: time to next stop in ticks
        """
        return self.__time_to_next_stop_base - self.__ticks_count
