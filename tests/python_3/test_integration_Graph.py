import unittest

from core.data_structures.graph import Node, Graph


class GraphIntegrationTests(unittest.TestCase):
    def test_graph_creation(self):
        nodes = []
        for letter in "ABCDEF":
            nodes.append(Node(letter))
        graph = Graph(nodes)
