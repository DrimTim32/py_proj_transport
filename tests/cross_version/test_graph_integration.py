import unittest

from core.configuration.config import Config
from core.data_structures.graph import Graph
from tests_utils.helpers import get_full_class_name

try:
    from mock import patch, mock_open, mock, PropertyMock
except ImportError:
    from unittest.mock import patch, mock_open


class GraphMockIntegrationTests(unittest.TestCase):
    def graph_mock_graph_dict(self, graph_dict_input):
        """
        Tests assertions
        :param graph_dict_input: value returned from config graph_dict
        :param assertions: methods asserting graph
        :type assertions: list[lambda]
        :rtype: Graph
        :return: Filled graph
        """
        name = get_full_class_name(Config)
        self.assertEqual('core.configuration.config.Config', name,
                         "Config directory has changed, please check! Should be {} but was ".format(
                             'core.configuration.config.Config', name))
        with mock.patch(name + ".graph_dict", new_callable=PropertyMock) as graph_dict:
            graph_dict.return_value = graph_dict_input
            graph = Graph.from_config(graph_dict_input)
            return graph

    def test_graph_from_simple_config(self):
        graph = self.graph_mock_graph_dict({
            "A": [("B", 10)],
            "B": [("A", 10)]
        })
        self.assertEqual(graph.get_path_between("A", "B"), ("B", 10))
        self.assertEqual(graph.get_path_between("B", "A"), ("A", 10))

    def test_line_graph(self):
        graph = self.graph_mock_graph_dict({
            "A": [("B", 10)],
            "B": [("A", 10), ("C", 10)],
            "C": [("B", 10), ("D", 10)],
            "D": [("C", 10)]
        })
        self.assertEqual(graph.get_path_between("A", "B"), ("B", 10))
        self.assertEqual(graph.get_path_between("B", "A"), ("A", 10))
        self.assertEqual(graph.get_path_between("B", "C"), ("C", 10))
        self.assertEqual(graph.get_path_between("C", "B"), ("B", 10))
        self.assertEqual(graph.get_path_between("C", "D"), ("D", 10))
        self.assertEqual(graph.get_path_between("D", "C"), ("C", 10))

    def test_one_way_graph(self):
        graph = self.graph_mock_graph_dict({
            "A": [("B", 10)],
            "B": [("C", 10)],
            "C": [("D", 10)],
            "D": []
        })
        self.assertEqual(graph.get_path_between("A", "B"), ("B", 10))
        self.assertEqual(graph.get_path_between("B", "C"), ("C", 10))
        self.assertEqual(graph.get_path_between("C", "D"), ("D", 10))
        self.assertEqual(graph.get_path_between("D", "C"), ("", 0))
        self.assertEqual(graph.get_path_between("B", "A"), ("", 0))
        self.assertEqual(graph.get_path_between("C", "B"), ("", 0))

    def test_different_numbers_graph(self):
        graph = self.graph_mock_graph_dict({
            "A": [("B", 1)],
            "B": [("C", 2)],
            "C": [("D", 3)],
            "D": [("C", 4)]
        })
        self.assertEqual(graph.get_path_between("A", "B"), ("B", 1))
        self.assertEqual(graph.get_path_between("B", "C"), ("C", 2))
        self.assertEqual(graph.get_path_between("C", "D"), ("D", 3))
        self.assertEqual(graph.get_path_between("D", "C"), ("C", 4))
