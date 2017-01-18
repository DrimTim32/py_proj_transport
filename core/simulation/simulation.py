import time

from core.data_structures import Graph, Node
from core.simulation.bus_collector import BusCollector
from core.simulation.generators import BusGenerator


class Simulation:
    def __init__(self, config):
        """Read configuration and do sth with it"""
        self.finished = False
        self.buses = []
        self.graph = None
        self.bus_generator = BusGenerator(config)
        self.bus_collector = BusCollector()

    def create_graph(self):
        """
          A - 1 - B - 2 - C - 1 - D
          |       |
          1       5
          |       |
          E - 1 - F
        """
        nodes = {}  # slownik 'nazwa noda' : Node()
        for letter in "ABCDEF":
            nodes[letter] = Node(letter)  # tworzymy nody o nazwie letter

        self.graph = Graph([nodes[key] for key in nodes])  # wyrzucam tylko same klasy node

    #
    # conn_nod("A", "B", 1)  # tworzy polaczenie A<->B (ta metoda wyzej
    # conn_nod("A", "E", 1)
    # conn_nod("E", "F", 1)
    # conn_nod("F", "B", 5)
    # conn_nod("B", "C", 2)
    # conn_nod("D", "C", 1)

    def update(self):
        pass

    def mainloop(self):
        while not self.finished:
            print("IM WORKING")
            time.sleep(2)
            self.update()
