from typing import List, Dict
from collections import namedtuple

Edge = namedtuple("Edge", ["node1", "node2", "weight"])


class Node:
    """Node structure"""

    def __init__(self, name):
        self.value = ""
        self.name = name
        self.__edges = []  # type: List[Edge]

    @property
    def neighbours(self):
        return [x.node2 for x in self.__edges]


class Graph:
    """Graph structure"""

    def __init__(self, nodes: List[Node] = None):
        if nodes is None:
            nodes = {}
        nodes = nodes
        self.graph = {}  # type: Dict[Node,Node]
        self.__populate_graph()

    def get_path_between(self, source_name, destination_name):
        raise NotImplementedError

    def __populate_graph(self):
        pass

    @property
    def vertices(self):
        return list(self.graph.keys())

    @property
    def edges(self):
        # TODO : create algorithm generating connections
        raise NotImplementedError
