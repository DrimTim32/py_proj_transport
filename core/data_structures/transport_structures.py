class PassengersGroup:
    """
        Group of passengers going to the same bus stop
    """

    def __init__(self, stop_name, group_count):
        """
        Inits passenger group
        :param stop_name: destination stop name
        :param group_count: how much passengers are going to destination
        """
        self.stop_name = stop_name
        self.count = group_count

    def __add__(self, other):
        return PassengersGroup(self.stop_name, self.count + other.count)


class Bus:
    """
        Bus class
    """

    def __init__(self, line, route):
        self.line = line
        self.route = route
        self.current_stop = 0
        self.ticks_to_next_stop = self.line.routes[self.route][self.current_stop].time_to_next_stop
        self.current_stop_name = self.line.routes[self.route][self.current_stop].name
        self.ticks_count = -1

    def move(self):
        if self.ticks_count == self.ticks_to_next_stop:
            self.current_stop += 1
            self.ticks_to_next_stop = self.line.routes[self.route][self.current_stop].time_to_next_stop
            self.current_stop_name = self.line.routes[self.route][self.current_stop].name
            self.ticks_count = -1
        self.ticks_count += 1
