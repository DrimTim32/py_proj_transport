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


class Stop:
    def __init__(self, name):
        self.name = name
        self.passengers = []


class Bus:
    """
        Bus class
    """
    BUS_COUNTER = 1

    def __init__(self, line, route):
        self.line = line
        self.route = route
        self.current_stop = 0
        self.ticks_to_next_stop = self.line.routes[self.route][self.current_stop].time_to_next_stop
        self.current_stop_name = self.line.routes[self.route][self.current_stop].name
        self.next_stop_name = self.line.routes[self.route][self.current_stop + 1].name
        self.ticks_count = 0
        self.route_len = len(self.line.routes[self.route])
        self.passengers = []
        self.id = Bus.BUS_COUNTER
        Bus.BUS_COUNTER += 1

    def move(self):
        if self.time_to_next_stop == 1:
            self.current_stop_name = self.next_stop_name
            self.next_stop_name = self.line.routes[self.route][
                self.current_stop + 2].name if self.current_stop < self.route_len - 2 else "None"
        if self.time_to_next_stop == 0:
            self.current_stop += 1
            if self.current_stop == self.route_len:
                return
            self.ticks_to_next_stop = self.line.routes[self.route][self.current_stop].time_to_next_stop
            self.ticks_count = 0
        else:
            self.ticks_count += 1

    @property
    def time_to_next_stop(self):
        return self.ticks_to_next_stop - self.ticks_count
