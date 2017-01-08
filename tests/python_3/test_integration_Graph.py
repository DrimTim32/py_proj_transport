import unittest
from unittest.mock import MagicMock
from dataStructures.Graph import Node, Graph, connect_both

class GraphIntegrationTests(unittest.TestCase):
    def test_graph_creation(self):
        nodes = []
        for letter in "ABCDEF":
            nodes.append(Node(letter))
        graph = Graph(nodes)