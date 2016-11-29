class Graph:
    """Graph structure"""
    def __init__(self,nodes=None):
        if nodes is None:
            nodes = {}
        self.nodes = nodes

    @property
    def vertices(self):
        return list(self.nodes)

    @property
    def edges(self):
        # TODO : create algorithm generating connections
        pass

    def append(self,node):
        if node not in self.nodes:
            self.nodes[node] = []

    def __str__(self):
        return "vertices " + ''.join([k+' ' for k in self.nodes])
