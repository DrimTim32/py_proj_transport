from typing import List, Dict, Tuple
from collections import namedtuple

Edge = namedtuple("Edge", ["node", "weight", "lines"])
NodeLengthPair = namedtuple("NodeLengthPair", ["node", "length"])


class Node:
    """Node structure"""

    def __init__(self, name):
        self.name = name
        self.__edges = []  # type: List[Edge]
        self.distance_vectors = {

        }

    def add_or_update_neighbour(self, node, weight, lines):
        nbs = self.neighbours
        if node not in nbs:
            self.__edges.append(Edge(node, weight, lines))
        else:
            index = next([i for i in range(len(self.__edges)) if self.__edges[i].node is node])
            self.__edges[index].weight = weight
            self.__edges[index].lines = lines
        self.distance_vectors[node.name] = weight

    @property
    def neighbours(self):
        return [x.node for x in self.__edges]

    def __str__(self):
        return self.name


def connect_both(node1: Node, node2: Node, weight, lines_right, lines_left):
    node1.add_or_update_neighbour(node2, weight, lines_right)
    node2.add_or_update_neighbour(node1, weight, lines_left)


import math


class Graph:
    """Graph structure"""

    def __init__(self, nodes: List[Node]):
        self.__graph = {}  # type: Dict[str,Node]
        self.__populate_graph(nodes)

    def get_path_between(self, source_name, destination_name):
        node1 = self.__graph[source_name]
        node2 = self.__graph[destination_name]
        return node1.distance_vectors[node2.name]

    def __populate_graph(self, nodes):
        for node in nodes:
            self.__graph[node.name] = node
        self.calculate_paths()

    def bfs(self, start):
        from queue import Queue
        output_list = []
        queue = Queue()
        queue.put(start)
        visited = set(start)
        while not queue.empty():
            current_node = queue.get()
            output_list.append(current_node)
            visited.add(current_node)
            for node in self.__graph[current_node].neighbours:
                if node.name not in visited:
                    queue.put(node.name)
        return output_list

    def calculate_paths(self):
        from copy import deepcopy
        tmpgraph = deepcopy(self.__graph)
        for key in self.__graph:
            (dist, tupl) = self.djikstra(deepcopy(tmpgraph), key)
            for k in self.__graph:
                curr = tupl[k]
                if curr is None:
                    self.__graph[key].distance_vectors[k] = ("", 0)
                    continue
                if tupl[curr] is None:
                    self.__graph[key].distance_vectors[k] = (k, dist[k])
                    continue
                while tupl[curr] != key:
                    curr = tupl[curr]
                self.__graph[key].distance_vectors[k] = (curr, dist[k])

    @staticmethod
    def djikstra(graph: Dict[str, Node], node_name: str) -> Dict[str, Tuple[str, int]]:
        pred = {key: None for key in graph.keys()}
        d = {key: math.inf for key in graph.keys()}
        d[node_name] = 0
        Q = set(graph.values())  # type : Set[Node]
        while len(Q) != 0:
            u = min(Q, key=lambda x: d[x.name])  # type: Node
            Q.remove(u)
            for v in u.neighbours:
                if d[v.name] > d[u.name] + u.distance_vectors[v.name]:
                    d[v.name] = d[u.name] + u.distance_vectors[v.name]
                    pred[v.name] = u.name
                    Q.add(v)
        return (d, pred)

    @property
    def vertices(self):
        return list(self.__graph.keys())

    @property
    def edges(self):
        # TODO : create algorithm generating connections
        raise NotImplementedError

    def __str__(self):
        pass
