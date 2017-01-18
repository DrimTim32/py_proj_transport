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
        self.create_lines()

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
        q = [bus for bus in self.buses if bus.current_stop == len(bus.line.routes[bus.route]) - 1]
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

    def create_lines(self):
        route1, route2 = [], []
        route1.append(LineStop("E", 1))
        route1.append(LineStop("F", 5))
        route1.append(LineStop("B", 2))
        route1.append(LineStop("C", 1))
        route1.append(LineStop("D", 0))

        route2.append(LineStop("D", 1))
        route2.append(LineStop("C", 2))
        route2.append(LineStop("B", 5))
        route2.append(LineStop("F", 1))
        route2.append(LineStop("E", 0))

        self.lines.append(Line("0", 10, 20, 20, route1, route2))

        stops = ["Krowodrza Gorka", "Krowoderskich", "Batalionu", "Makowskiego", "Lobzow", "Mazowiecka", "Biprostal",
                 "Korek1", "Korek2",
                 "Korek3", "AGH", "Cracovia", "Jubilat", "Konopnickiej", "MOST GRUNWALDZKI", "Szwedzka", "Kapelanka",
                 "Slomiana",
                 "Kobierzynska", "Lipinskiego", "Grota", "Rostworowskiego", "Norymberska", "Ruczaj", "UJ",
                 "Chmieleniec", "Maki"]
        times = [2] * len(stops)
        route1 = []
        for i in range(len(stops)):
            route1.append(LineStop(stops[i], times[i]))
        route2 = route1[::-1]
        # self.lines.append(Line("194", 10, 10, 10, route1, route2))
