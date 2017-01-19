import time

from core.data_structures import Graph
from core.data_structures.transport_structures import Bus
from core.simulation.bus_collector import BusCollector
from core.simulation.generators import BusGenerator
from core.simulation.line import LineStop, Line
from core.simulation.status_printer import StatusPrinter


class Simulation:
    def __init__(self, config):
        """Read configuration and do sth with it"""
        self.finished = False
        self.steps = 0
        self.buses = []
        self.lines = []
        self.bus_generator = BusGenerator()
        self.bus_collector = BusCollector()
        self.printer = StatusPrinter()

        self.graph = Graph.from_config(config.graph_dict)
        """
             A - 1 - B - 2 - C - 1 - D
             |       |
             1       5
             |       |
             E - 1 - F
           """
        self.create_lines(config.lines_dict)

    def mainloop(self):
        while not self.finished:
            print('________________________________________________________')
            print('STEP ', self.steps)
            for bus in self.buses:
                print('Bus{', 'line:', bus.line.number, 'route:', bus.route, 'last stop:', bus.current_stop_name,
                      ' next stop:', bus.next_stop_name, 'time to next:', bus.time_to_next_stop())
            self.update()
            time.sleep(0.1)

    def update(self):
        self.steps += 1
        self.clean_buses()
        self.update_buses()
        self.generate_buses()

    def update_buses(self):
        for bus in self.buses:
            bus.move()

    def generate_buses(self):
        for line in self.lines:
            new_buses = line.tick()
            for i in range(len(new_buses)):
                if new_buses[i]:
                    self.buses.append(Bus(line, i))

    def clean_buses(self):
        q = [bus for bus in self.buses if bus.current_stop == bus.line.last_stop(bus.route)]
        for b in q:
            self.buses.remove(b)

    def create_lines(self, lines):
        for line in lines.values():
            route1, route2 = [], []
            curr_route = line['route1']
            for i in range(len(curr_route)):
                route1.append(LineStop(curr_route[i],
                                       self.graph[curr_route[i], curr_route[i + 1]] if i < len(curr_route) - 1 else 0))

            curr_route = line['route2']
            for i in range(len(curr_route)):
                route2.append(LineStop(curr_route[i],
                                       self.graph[curr_route[i], curr_route[i + 1]] if i < len(curr_route) - 1 else 0))

            self.lines.append(Line(line, route1, route2))
