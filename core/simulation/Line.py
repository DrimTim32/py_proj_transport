class Line:
    def __init__(self, number, bus_capacity, graph1, frequency1, graph2, frequency2):
        self.number = number
        self.bus_capacity = bus_capacity
        self.graph1 = graph1
        self.frequency1 = frequency1
        self.graph2 = graph2
        self.frequency2 = frequency2

    def get_path(self, node1, node2):
        """
        Calculates path from node1 to node2
        :param node1:
        :param node2:
        :return: list of all nodes between
        """
