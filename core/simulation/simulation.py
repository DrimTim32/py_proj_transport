import time

from core.data_structures import Graph, Node, connect_both
from core.simulation.bus_collector import BusCollector
from core.simulation.generators import BusGenerator
from core.simulation.status_printer import StatusPrinter


class Simulation:
    def __init__(self, config):
        """Read configuration and do sth with it"""
        self.finished = False
        self.steps = 0
        self.buses = []
        self.lines = []
        self.graph = None
        self.bus_generator = BusGenerator(config)
        self.bus_collector = BusCollector()
        self.printer = StatusPrinter()

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

    def update(self):
        self.clean_buses()

    def update_buses(self):
        for bus in self.buses:
            pass

    def generate_buses(self):
        for line in self.lines:
            pass

    def clean_buses(self):
        for bus in self.buses:
            if bus.current_stop == bus.line.get_last_stop(bus.route) and bus.ticks_count == 0:
                self.buses.remove(bus)

    def mainloop(self):
        while not self.finished:
            print('________________________________________________________')
            print('STEP ', self.steps)
            for bus in self.buses:
                print('Bus{', 'line: ', bus.line, ' route: ', bus.route, ' last stop:', bus.current_stop,
                      'time to next stop:', bus.ticks_to_next_stop)

            self.steps += 1
            time.sleep(2)
            self.update()
