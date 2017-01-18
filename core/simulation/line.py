class Line:
    def __init__(self, number, bus_capacity, frequency1, frequency2):
        self.number = number
        self.bus_capacity = bus_capacity
        self.frequencies = [1, 1]
        self.routes = [[], []]

    def get_first_stop(self, route):
        return self.routes[route][0]

    def get_last_stop(self, route):
        return self.routes[route][-1]
