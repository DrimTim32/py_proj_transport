from collections import namedtuple

LineStop = namedtuple('LineStop', ['name', 'time_to_next_stop'])


class Line:
    def __init__(self, line_data, route1, route2):
        self.number = line_data['id']
        self.bus_capacity = line_data['bus_capacity']
        self.frequencies = [line_data['frequency1'], line_data['frequency2']]
        self.routes = [route1, route2]
        self.last_bus = [line_data['frequency1'], line_data['frequency2']]

    def first_stop_name(self, route):
        return self.routes[route][0].name

    def last_stop_name(self, route):
        return self.routes[route][-1].name

    def last_stop(self, route):
        return len(self.routes[route]) - 1

    def tick(self):
        new_buses = [False, False]
        for i in range(len(self.last_bus)):
            self.last_bus[i] += 1

        for i in range(len(self.last_bus)):
            if self.last_bus[i] >= self.frequencies[i]:
                new_buses[i] = True
                self.last_bus[i] = 0

        return new_buses
