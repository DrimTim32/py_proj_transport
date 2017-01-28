from collections import namedtuple

from numpy import inf

Edge = namedtuple("Edge", ["node", "weight"])
NodeLengthPair = namedtuple("NodeLengthPair", ["node", "length"])

try:
    from queue import Queue
except ImportError:
    from Queue import Queue


class Node:
    """Node structure"""

    def __init__(self, name):
        self.name = name
        self.edges = []  # type: list[Edge]
        self.distance_vectors = {}

    def add_or_update_neighbour(self, node, weight):
        """
        Connects node to current node, if node already connected then updates it.
        :param node: node to connect
        :param weight: weight from current node to new node
        :param lines: lines going from current node to new node
        :type node: Node
        :type weight: int
        :type lines: List[int]
        :rtype: None
        """
        nbs = self.neighbours
        if node not in nbs:
            self.edges.append(Edge(node, weight))
        else:
            index = next([i for i in range(len(self.edges)) if self.edges[i].node is node])
            self.edges[index].weight = weight
        self.distance_vectors[node.name] = weight

    @property
    def neighbours(self):
        """Returns all neighbours of current node"""
        return [x.node for x in self.edges]

    def __str__(self):
        return self.name


def connect_both(node1, node2, weight):
    """
    Connects node1 with node2 and node2 with node1
    :param node1: first node
    :param node2: second node
    :param weight: weight on edge
    :param lines_right: lines from node1 to node2
    :param lines_left: lines from node2 to node 1
    :type node1 : Node
    :type node2 : Node
    :type weight : int
    :type lines_right : List[int]
    :type lines_left : List[int]
    :return: None
    .. seealso:: connect_one_way
    """
    connect_one_way(node1, node2, weight)
    connect_one_way(node2, node1, weight)


def connect_one_way(node1, node2, weight):
    """
    Connects node1 to node2
    :param node1: first node
    :param node2: second node
    :param weight: weight on edge
    :param lines: lines from node1 to node2
    :type node1 : Node
    :type node2 : Node
    :type weight : int
    :type lines : List[int]
    :return: None
    .. seealso:: connect_both
    """
    node1.add_or_update_neighbour(node2, weight)


class Graph:
    """Graph structure"""

    @staticmethod
    def from_config(dictionary):
        """
        Builds a graph from configuration object
        :param dictionary:
        :type dictionary: dict[str,List[tuple[str,int]]]
        :return:
        :rtype: Graph
        """
        nodes = {}

        for s in dictionary:
            nodes[s] = Node(s)
        for s in dictionary:
            for q in dictionary[s]:
                connect_one_way(nodes[s], nodes[q[0]], q[1])
        return Graph(nodes.values())

    def __init__(self, nodes):
        """
        :type nodes :  List[Node]
        """
        self.__graph = {}  # type: dict[str,Node]
        self.__populate_graph(nodes)

    def __getitem__(self, input):
        """

        :param input:
        :type input: tuple(str,str)
        :return:
        """
        node = self.__graph[input[0]]
        for edge in node.edges:
            if edge.node.name == input[1]:
                return edge.weight
        return -1

    def get_path_between(self, source_name, destination_name):
        """
        Returns distance between two nodes and first step to go from source to destination
        :param source_name: name of source node
        :param destination_name: name of destination node
        :type source_name: string
        :type destination_name: string
        :return: Tuple with first step and distance
        :rtype: Tuple[str,int]
        """
        node1 = self.__graph[source_name]
        return node1.distance_vectors[destination_name]

    def __populate_graph(self, nodes):
        for node in nodes:
            self.__graph[node.name] = node
        self.__calculate_paths()

    def bfs(self, start):
        """
        Iterates over graph using bfs algorithm
        :param start: first node
        :type start: str
        :return:
        :rtype: Iterator[Node]
        """
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

    def __calculate_paths(self):
        """
        Calculates whole graph
        :return: None
        """
        from copy import deepcopy
        tmp_graph = deepcopy(self.__graph)
        for key in self.__graph:
            (dist, tupl) = self.__djikstra(deepcopy(tmp_graph), key)
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
    def __djikstra(graph, node_name):
        """
        Uses djikstra algorithm to calculate distances bewteen first node and the others
        :param graph: graph to trvers
        :param node_name: first node name
        :type graph: Dict[str,Node]
        :type node_name: str
        :return: calculated distances and predecesors
        :rtype: Tuple[Dict[str,int],Dict[str,str]]
        """
        predecessors = {key: None for key in graph.keys()}
        distances = {key: inf for key in graph.keys()}
        distances[node_name] = 0
        nodes_set = set(graph.values())  # type : Set[Node]
        while len(nodes_set) != 0:
            min_node = min(nodes_set, key=lambda x: distances[x.name])  # type: Node
            nodes_set.remove(min_node)
            for neighbour in min_node.neighbours:
                if distances[neighbour.name] > distances[min_node.name] + min_node.distance_vectors[neighbour.name]:
                    distances[neighbour.name] = distances[min_node.name] + min_node.distance_vectors[neighbour.name]
                    predecessors[neighbour.name] = min_node.name
                    nodes_set.add(neighbour)
        return distances, predecessors

    @property
    def vertices(self):
        """
        Retuns all nodes in graph
        :return:
        :rtype: List[Node]
        """
        return list(self.__graph.values())

    def __str__(self):
        pass
