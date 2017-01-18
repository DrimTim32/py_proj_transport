from collections import namedtuple

LineStop = namedtuple('LineStop', ['name', 'time_to_next_stop'])


class Line:
    def __init__(self, number, bus_capacity, frequency1, frequency2, route1, route2):
        self.number = number
        self.bus_capacity = bus_capacity
        self.frequencies = [frequency1, frequency2]
        self.routes = [route1, route2]
        self.last_bus = [frequency1, frequency2]

    def get_first_stop(self, route):
        return self.routes[route][0].name

    def get_last_stop(self, route):
        return self.routes[route][-1].name

    def tick(self):
        new_buses = [False, False]
        for i in range(len(self.last_bus)):
            self.last_bus[i] += 1

        for i in range(len(self.last_bus)):
            if self.last_bus[i] >= self.frequencies[i]:
                new_buses[i] = True
                self.last_bus[i] = 0

        return new_buses
