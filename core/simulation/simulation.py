import time

from core.data_structures import Graph, Node, connect_both
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
        self.graph = None
        self.bus_generator = BusGenerator()
        self.bus_collector = BusCollector()
        self.printer = StatusPrinter()

        self.create_graph()
        self.create_lines(config.lines_list)

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

    def create_graph(self):
        """
          A - 1 - B - 2 - C - 1 - D
          |       |
          1       5
          |       |
          E - 1 - F
        """
        nodes = {}
        for letter in "ABCDEF":
            nodes[letter] = Node(letter)

        def conn_nod(a, b, length):
            connect_both(nodes[a], nodes[b], length)

        conn_nod("A", "B", 1)
        conn_nod("A", "E", 1)
        conn_nod("E", "F", 1)
        conn_nod("F", "B", 5)
        conn_nod("B", "C", 2)
        conn_nod("D", "C", 1)
        self.graph = Graph([nodes[key] for key in nodes])

    def create_lines(self, lines):
        for line in lines.values():
            route1 = [LineStop(stop, 1) for stop in line["route1"]]
            route2 = [LineStop(stop, 1) for stop in line["route2"]]
            self.lines.append(Line(line, route1, route2))
