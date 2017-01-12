import unittest

from core.data_structures.graph import Node, Graph, connect_both


class GraphTests(unittest.TestCase):
    def test_graph_creation(self):
        nodes = []
        for letter in "ABCDEF":
            nodes.append(Node(letter))
        graph = Graph(nodes)

    def connect_nodes_without_lines(self, node, node2, dist):
        connect_both(node, node2, dist)

    def test_graph_harder_path_len(self):
        """
          A - - 2 - - E
          |  \      / |
          4   1    3  10
          |    \  /   |
          B -2- D -7- F
          |    / \    |
          5   8    4   6
          | /       \ |
          C - - 1 - - G
        """
        nodes = {}
        for letter in "ABCDEFG":
            nodes[letter] = Node(letter)

        def ass_path_len(a, b, i):
            self.assert_path_len(graph, a, b, i, "between {0} and {1} should be {2}".format(a, b, i))

        def conn_nod(a, b, len):
            self.connect_nodes_without_lines(nodes[a], nodes[b], len)

        connection_list = [
            ("A", "E", 2), ("A", "B", 4), ("A", "D", 1), ("B", "D", 2),
            ("B", "C", 5), ("C", "D", 8), ("C", "G", 1), ("E", "D", 3),
            ("E", "F", 10), ("F", "D", 7), ("F", "G", 6), ("G", "D", 4)]
        for conn in connection_list:
            conn_nod(conn[0], conn[1], conn[2])
        graph = Graph([nodes[key] for key in nodes])

        paths_to_check = [
            ("A", "B", 3), ("A", "C", 6),
            ("A", "D", 1), ("A", "E", 2),
            ("A", "F", 8), ("A", "G", 5),

            ("B", "A", 3), ("B", "C", 5),
            ("B", "D", 2), ("B", "E", 5),
            ("B", "F", 9), ("B", "G", 6),

            ("C", "A", 6), ("C", "B", 5),
            ("C", "D", 5), ("C", "E", 8),
            ("C", "F", 7), ("C", "G", 1),

            ("D", "A", 1), ("D", "B", 2),
            ("D", "C", 5), ("D", "E", 3),
            ("D", "F", 7), ("D", "G", 4),

            ("E", "A", 2), ("E", "B", 5),
            ("E", "C", 8), ("E", "D", 3),
            ("E", "F", 10), ("E", "G", 7),
        ]
        for path in paths_to_check:
            ass_path_len(path[0], path[1], path[2])

    def test_graph_easy_path_len(self):
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

        def conn_nod(a, b, len):
            self.connect_nodes_without_lines(nodes[a], nodes[b], len)

        def ass_path_len(a, b, i):
            self.assert_path_len(graph, a, b, i, "between {0} and {1} should be {2}".format(a, b, i))

        conn_nod("A", "B", 1)
        conn_nod("A", "E", 1)
        conn_nod("E", "F", 1)
        conn_nod("F", "B", 5)
        conn_nod("B", "C", 2)
        conn_nod("D", "C", 1)
        graph = Graph([nodes[key] for key in nodes])

        ass_path_len("A", "B", 1)
        ass_path_len("B", "A", 1)
        ass_path_len("A", "E", 1)
        ass_path_len("E", "F", 1)
        ass_path_len("F", "B", 3)
        ass_path_len("B", "F", 3)
        ass_path_len("B", "C", 2)
        ass_path_len("D", "C", 1)
        ass_path_len("A", "F", 2)

    def test_graph_cracov_easy_path_next(self):
        stops_common = ["Czerwone Maki", "Chmieleniec", "Kampus UJ", "Ruczaj", "Norymberska", "Grota", "Lipinskiego"]
        nodes = {}
        for name in stops_common:
            nodes[name] = Node(name)

        def conn_nod(a, b, len):
            self.connect_nodes_without_lines(nodes[a], nodes[b], len)

        nodes_list = [node for node in nodes.values()]
        for i in range(0, len(stops_common) - 1):
            conn_nod(stops_common[i], stops_common[i + 1], 5)

        graph = Graph(nodes_list)
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

        def conn_nod(a, b, len):
            self.connect_nodes_without_lines(nodes[a], nodes[b], len)

        def ass_path_len(a, b, i):
            self.assert_path_len(graph, a, b, i, "between {0} and {1} should be {2}".format(a, b, i))

        nodes_list = [node for node in nodes.values()]
        conn_nod(stops_common[0], stops_common[1], 5)
        conn_nod(stops_common[1], stops_common[2], 5)
        conn_nod(stops_common[2], stops_common[3], 5)
        conn_nod(stops_common[3], stops_common[4], 5)
        conn_nod(stops_common[4], stops_common[5], 5)
        conn_nod(stops_common[5], stops_common[6], 5)
        graph = Graph(nodes_list)
        q = 0
        for i in range(0, len(stops_common)):
            for q in range(0, len(stops_common)):
                self.assert_path_len(graph, stops_common[i], stops_common[q], abs(i - q) * 5)

    def assert_path_len(self, graph, node1, node2, len, msg=None):
        tmp = graph.get_path_between(node1, node2)[1]
        self.assertEqual(tmp, len, (msg + " but was {0}".format(tmp)) if msg is not None else None)

    def assert_path_next_move(self, graph, node1, node2, next):
        self.assertEqual(graph.get_path_between(node1, node2)[0], next)
