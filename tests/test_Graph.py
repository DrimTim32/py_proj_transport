import unittest
from dataStructures.Graph import Node,Graph
class GraphTests(unittest.TestCase):

    def test_graph_creation(self):
        nodes =[]
        for letter in "ABCDEF":
            nodes.append(Node(letter))
        graph = Graph(nodes)