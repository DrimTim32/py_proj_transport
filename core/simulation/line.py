from collections import namedtuple

LineStop = namedtuple('LineStop', ['name', 'time_to_next'])


class Line:
    def __init__(self, number, bus_capacity, frequency1, frequency2, route1, route2):
        self.number = number
        self.bus_capacity = bus_capacity
        self.frequencies = [frequency1, frequency2]
        self.routes = [route1, route2]

    def get_first_stop(self, route):
        return self.routes[route][0].name

    def get_last_stop(self, route):
        return self.routes[route][-1].name
