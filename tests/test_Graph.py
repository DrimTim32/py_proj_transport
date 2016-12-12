import unittest
from dataStructures.Graph import Node, Graph, connect_both


class GraphTests(unittest.TestCase):
    def test_graph_creation(self):
        nodes = []
        for letter in "ABCDEF":
            nodes.append(Node(letter))
        graph = Graph(nodes)

    def test_graph_easy_path(self):
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

        connect_both(nodes["A"], nodes["B"], 1, [], [])
        connect_both(nodes["A"], nodes["E"], 1, [], [])
        connect_both(nodes["E"], nodes["F"], 1, [], [])
        connect_both(nodes["F"], nodes["B"], 5, [], [])
        connect_both(nodes["B"], nodes["C"], 2, [], [])
        connect_both(nodes["D"], nodes["C"], 1, [], [])
        graph = Graph([nodes[key] for key in nodes])

        self.assert_path_len(graph, "A", "B", 1)
        self.assert_path_len(graph, "B", "A", 1)
        self.assert_path_len(graph, "A", "E", 1)
        self.assert_path_len(graph, "E", "F", 1)
        self.assert_path_len(graph, "F", "B", 3)
        self.assert_path_len(graph, "B", "F", 3)
        self.assert_path_len(graph, "B", "C", 2)
        self.assert_path_len(graph, "D", "C", 1)
        self.assert_path_len(graph, "A", "F", 2)

    def test_graph_cracov_easy_path_next(self):
        stops_common = ["Czerwone Maki", "Chmieleniec", "Kampus UJ", "Ruczaj", "Norymberska", "Grota", "Lipinskiego"]
        nodes = {}
        for name in stops_common:
            nodes[name] = Node(name)
        nodesList = [node for node in nodes.values()]
        connect_both(nodes[stops_common[0]], nodes[stops_common[1]], 5, [], [])
        connect_both(nodes[stops_common[1]], nodes[stops_common[2]], 5, [], [])
        connect_both(nodes[stops_common[2]], nodes[stops_common[3]], 5, [], [])
        connect_both(nodes[stops_common[3]], nodes[stops_common[4]], 5, [], [])
        connect_both(nodes[stops_common[4]], nodes[stops_common[5]], 5, [], [])
        connect_both(nodes[stops_common[5]], nodes[stops_common[6]], 5, [], [])
        graph = Graph(nodesList)
        for stop in stops_common[1:]:
            self.assert_path_next_move(graph, "Czerwone Maki", stop, "Chmieleniec")
        for stop in stops_common[2:]:
            self.assert_path_next_move(graph, "Chmieleniec", stop, "Kampus UJ")
        for stop in stops_common[3:]:
            self.assert_path_next_move(graph, "Kampus UJ", stop, "Ruczaj")
        for stop in stops_common[:2]:
            self.assert_path_next_move(graph, "Kampus UJ", stop, "Chmieleniec")
        for stop in stops_common[4:]:
            self.assert_path_next_move(graph, "Ruczaj", stop, "Norymberska")

    def test_graph_cracov_easy_path_len(self):
        stops_common = ["Czerwone Maki", "Chmieleniec", "Kampus UJ", "Ruczaj", "Norymberska", "Grota", "Lipinskiego"]
        nodes = {}
        for name in stops_common:
            nodes[name] = Node(name)
        nodesList = [node for node in nodes.values()]
        connect_both(nodes[stops_common[0]], nodes[stops_common[1]], 5, [], [])
        connect_both(nodes[stops_common[1]], nodes[stops_common[2]], 5, [], [])
        connect_both(nodes[stops_common[2]], nodes[stops_common[3]], 5, [], [])
        connect_both(nodes[stops_common[3]], nodes[stops_common[4]], 5, [], [])
        connect_both(nodes[stops_common[4]], nodes[stops_common[5]], 5, [], [])
        connect_both(nodes[stops_common[5]], nodes[stops_common[6]], 5, [], [])
        graph = Graph(nodesList)
        q = 0
        for i in range(0,len(stops_common)):
            for q in range(0,len(stops_common)):
                self.assert_path_len(graph,stops_common[i],stops_common[q],abs(i-q)*5)

    def assert_path_len(self, graph: Graph, node1: str, node2: str, len: int):
        self.assertEqual(graph.get_path_between(node1, node2)[1], len)

    def assert_path_next_move(self, graph: Graph, node1: str, node2: str, next: str):
        self.assertEqual(graph.get_path_between(node1, node2)[0], next)
