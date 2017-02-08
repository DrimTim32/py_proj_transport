"""
This file contains functional tests for simulation class
"""
import sys

from core.configuration import Config
from core.simulation import PassengersGroup
from core.simulation import Simulation
from utils.TestsBase import TestBase
from utils.helpers import add_property, add_variable, get_full_class_name
if sys.version_info[0] >= 3:
    from unittest.mock import PropertyMock, patch
else:
    from mock import PropertyMock, patch


def passenger_group_equality(first_group, second_group):
    """
    Checks if two passenger groups are equal
    :param first_group: first group
    :param second_group: second group
    :return: True if are equal False if not
    :rtype: bool
    """
    return first_group.count == second_group.count and first_group.destination == second_group.destination


class SimulationTest(TestBase):
    """Class for testing simulation class"""

    def test_graph_and_lines(self):
        """Tests simulation with graph and lines"""
        config_name = get_full_class_name(Config)
        with patch(config_name+'.graph_dict', new_callable=PropertyMock) as mock_graph_dict:
            with patch(config_name+'.lines_dict', new_callable=PropertyMock) as mock_lines_dict:
                with patch(config_name+'.traffic_data_dict',
                           new_callable=PropertyMock) as mock_traffic_dict:
                    mock_graph_dict.return_value = {'A': [('B', 7), ('D', 2)],
                                                    'B': [('A', 7), ('C', 1), ('E', 2)],
                                                    'C': [('B', 1), ('D', 3)],
                                                    'D': [('A', 2), ('C', 3)],
                                                    'E': [('B', 2), ('F', 2)],
                                                    'F': [('E', 2)]}
                    mock_lines_dict.return_value = {
                        0: {'id': 0, 'bus_capacity': 20, 'frequency1': 17, 'frequency2': 17,
                            'route1': ['A', 'D', 'C', 'B', 'E', 'F'],
                            'route2': ['F', 'E', 'B', 'A']}}
                    config = Config(["A", "B", "C", "D", "E", "F"], {}, {}, {}, 1.0)
                    mock_traffic_dict.return_value = {'E': {'E': 0, 'F': 0, 'D': 0, 'A': 0, 'C': 0, 'B': 0},
                                                      'F': {'E': 0, 'F': 0, 'D': 0, 'A': 0, 'C': 0, 'B': 0},
                                                      'D': {'E': 0, 'F': 0, 'D': 0, 'A': 0, 'C': 0, 'B': 0},
                                                      'A': {'E': 0, 'F': 0, 'D': 0, 'A': 0, 'C': 0, 'B': 0},
                                                      'C': {'E': 0, 'F': 0, 'D': 0, 'A': 0, 'C': 0, 'B': 0},
                                                      'B': {'E': 0, 'F': 0, 'D': 0, 'A': 0, 'C': 0, 'B': 0}}

                    simulation = Simulation(config)

                def mocked_update(mocked_self):
                    """Mocked update """
                    for bus in mocked_self.buses:
                        if bus.route == 0:
                            if bus.id not in mocked_self.mocked_dict.keys():
                                mocked_self.mocked_dict[bus.id] = []
                            if bus.time_to_next_stop == 0:
                                mocked_self.mocked_dict[bus.id].append(bus.current_stop_name)
                            else:
                                mocked_self.mocked_dict[bus.id].append(bus.current_stop_name + bus.next_stop_name)

                def finished(mocked_self):
                    mocked_self.mocked_update()
                    return False

                add_property(simulation, "finished", finished)
                from types import MethodType
                simulation.mocked_update = MethodType(mocked_update, simulation)
                add_variable(simulation, "count_finished", 0)
                add_variable(simulation, "mocked_dict", {})
                count = 0
                while count < 35:
                    count += 1
                    simulation.refresh()
                paths = ['PA', 'A', 'AD', 'AD', 'D', 'DC', 'DC', 'DC', 'C', 'CB', 'B', 'BE', 'BE', 'E', 'EF', 'EF', 'F']
                self.assertEqual(len(simulation.mocked_dict), 2)
                for path in simulation.mocked_dict.values():
                    self.assertEqual(path, paths)

    def test_graph_and_lines_transfer(self):
        """Tests simulation with graph and lines - choosing better way"""
        config_name = get_full_class_name(Config)
        with patch(config_name+'.graph_dict', new_callable=PropertyMock) as mock_graph_dict:
            with patch(config_name+'.lines_dict', new_callable=PropertyMock) as mock_lines_dict:
                with patch(config_name+'.traffic_data_dict',
                           new_callable=PropertyMock) as mock_traffic_dict:
                    class MockedGenerator:
                        def __init__(self, empty_argument):
                            self.done = False

                        def generate(self, src, dest):
                            if not self.done and src == 'C' and dest == 'F':
                                self.done = True
                                return 1
                            return 0

                    mock_graph_dict.return_value = {'A': [('B', 2), ('D', 2)],
                                                    'B': [('A', 2), ('C', 100), ('E', 2)],
                                                    'C': [('B', 100), ('D', 2)],
                                                    'D': [('A', 2), ('C', 2)],
                                                    'E': [('B', 2), ('F', 2)],
                                                    'F': [('E', 2)]}
                    mock_lines_dict.return_value = {
                        0: {'id': 0, 'bus_capacity': 20, 'frequency1': 1000, 'frequency2': 1000,
                            'route1': ['B', 'A', 'D', 'C'],
                            'route2': ['C', 'D', 'A', 'B']},
                        1: {'id': 1, 'bus_capacity': 20, 'frequency1': 1000, 'frequency2': 1000,
                            'route1': ['C', 'B', 'E', 'F'],
                            'route2': ['F', 'E', 'B', 'C']}}
                    config = Config(["A", "B", "C", "D", "E", "F"], {}, {}, {}, 1.0)
                    mock_traffic_dict.return_value = {'E': {'E': 0, 'F': 0, 'D': 0, 'A': 0, 'C': 0, 'B': 0},
                                                      'F': {'E': 0, 'F': 0, 'D': 0, 'A': 0, 'C': 0, 'B': 0},
                                                      'D': {'E': 0, 'F': 0, 'D': 0, 'A': 0, 'C': 0, 'B': 0},
                                                      'A': {'E': 0, 'F': 0, 'D': 0, 'A': 0, 'C': 0, 'B': 0},
                                                      'C': {'E': 0, 'F': 1, 'D': 0, 'A': 0, 'C': 0, 'B': 0},
                                                      'B': {'E': 0, 'F': 0, 'D': 0, 'A': 0, 'C': 0, 'B': 0}}

                    simulation = Simulation(config, MockedGenerator)
                    simulation.refresh()

                    self.are_lists_equal(simulation.stops['C'].passengers, [PassengersGroup('F', 1)],
                                         passenger_group_equality)
                    simulation.refresh()
                    self.are_lists_equal(simulation.stops['C'].passengers, [],
                                         passenger_group_equality)
                    k = 0
                    buuu = None
                    for bus in simulation.buses:
                        if bus.line.number == 0 and bus.route == 1:
                            buuu = bus
                            k += 1
                            self.are_lists_equal(bus.passengers, [PassengersGroup('F', 1)],
                                                 passenger_group_equality)
                    self.are_equal(k, 1)

                    for _ in range(9):
                        simulation.refresh()

                    self.are_lists_equal(simulation.stops['B'].passengers, [PassengersGroup('F', 1)],
                                         passenger_group_equality)

                    self.are_lists_equal(buuu.passengers, [], passenger_group_equality)

                    for _ in range(91):
                        simulation.refresh()
                    self.are_lists_equal(simulation.stops['B'].passengers, [PassengersGroup('F', 1)],
                                         passenger_group_equality)

                    simulation.refresh()
                    self.are_lists_equal(simulation.stops['B'].passengers, [], passenger_group_equality)

                    k = 0
                    buuu = None
                    for bus in simulation.buses:
                        if bus.line.number == 1 and bus.route == 0:
                            buuu = bus
                            k += 1
                            self.are_lists_equal(bus.passengers, [PassengersGroup('F', 1)],
                                                 passenger_group_equality)
                    self.are_equal(k, 1)

                    for _ in range(6):
                        simulation.refresh()
                    self.are_lists_equal(buuu.passengers, [], passenger_group_equality)

    def test_graph_and_lines_transfer_2(self):
        """Tests simulation with graph and lines - duplication"""
        config_name = get_full_class_name(Config)
        with patch(config_name+'.graph_dict', new_callable=PropertyMock) as mock_graph_dict:
            with patch(config_name+'.lines_dict', new_callable=PropertyMock) as mock_lines_dict:
                with patch(config_name+'.traffic_data_dict',
                           new_callable=PropertyMock) as mock_traffic_dict:
                    class MockedGenerator:
                        def __init__(self, empty_argument):
                            self.done = False

                        def generate(self, src, dest):
                            if not self.done and src == 'C' and dest == 'F':
                                self.done = True
                                return 1
                            return 0

                    mock_graph_dict.return_value = {'A': [('B', 2), ('D', 2)],
                                                    'B': [('A', 2), ('C', 2), ('E', 2)],
                                                    'C': [('B', 2), ('D', 2)],
                                                    'D': [('A', 2), ('C', 2)],
                                                    'E': [('B', 2), ('F', 2)],
                                                    'F': [('E', 2)]}
                    mock_lines_dict.return_value = {
                        0: {'id': 0, 'bus_capacity': 20, 'frequency1': 1000, 'frequency2': 1000,
                            'route1': ['B', 'A', 'D', 'C'],
                            'route2': ['C', 'D', 'A', 'B']},
                        1: {'id': 1, 'bus_capacity': 20, 'frequency1': 1000, 'frequency2': 1000,
                            'route1': ['C', 'B', 'E', 'F'],
                            'route2': ['F', 'E', 'B', 'C']}}
                    config = Config(["A", "B", "C", "D", "E", "F"], {}, {}, {}, 1.0)
                    mock_traffic_dict.return_value = {'E': {'E': 0, 'F': 0, 'D': 0, 'A': 0, 'C': 0, 'B': 0},
                                                      'F': {'E': 0, 'F': 0, 'D': 0, 'A': 0, 'C': 0, 'B': 0},
                                                      'D': {'E': 0, 'F': 0, 'D': 0, 'A': 0, 'C': 0, 'B': 0},
                                                      'A': {'E': 0, 'F': 0, 'D': 0, 'A': 0, 'C': 0, 'B': 0},
                                                      'C': {'E': 0, 'F': 1, 'D': 0, 'A': 0, 'C': 0, 'B': 0},
                                                      'B': {'E': 0, 'F': 0, 'D': 0, 'A': 0, 'C': 0, 'B': 0}}

                    simulation = Simulation(config, MockedGenerator)
                    simulation.refresh()

                    self.are_lists_equal(simulation.stops['C'].passengers, [PassengersGroup('F', 1)],
                                         passenger_group_equality)
                    simulation.refresh()
                    self.are_lists_equal(simulation.stops['C'].passengers, [],
                                         passenger_group_equality)
                    k = 0
                    for bus in simulation.buses:
                        k += bus.count
                    self.are_equal(k, 1)

    def test_graph_and_lines_transfer_3(self):
        """Tests simulation with graph and lines - looong bus stops"""
        config_name = get_full_class_name(Config)
        with patch(config_name+'.graph_dict', new_callable=PropertyMock) as mock_graph_dict:
            with patch(config_name+'.lines_dict', new_callable=PropertyMock) as mock_lines_dict:
                with patch(config_name+'.traffic_data_dict',
                           new_callable=PropertyMock) as mock_traffic_dict:
                    class MockedGenerator:
                        def __init__(self, empty_argument):
                            self.done = False

                        def generate(self, src, dest):
                            if not self.done and src == 'C' and dest == 'F':
                                self.done = True
                                return 1
                            return 0

                    mock_graph_dict.return_value = {'A': [('B', 2), ('D', 2)],
                                                    'B': [('A', 2), ('C', 2), ('E', 2)],
                                                    'C': [('B', 8), ('D', 2)],
                                                    'D': [('A', 2), ('C', 2)],
                                                    'E': [('B', 2), ('F', 2)],
                                                    'F': [('E', 2)]}
                    mock_lines_dict.return_value = {
                        0: {'id': 0, 'bus_capacity': 20, 'frequency1': 1000, 'frequency2': 1000,
                            'route1': ['B', 'A', 'D', 'C'],
                            'route2': ['C', 'D', 'A', 'B']},
                        1: {'id': 1, 'bus_capacity': 20, 'frequency1': 1000, 'frequency2': 1000,
                            'route1': ['C', 'B', 'E', 'F'],
                            'route2': ['F', 'E', 'B', 'C']}}
                    config = Config(["A", "B", "C", "D", "E", "F"], {}, {}, {}, 1.0)
                    mock_traffic_dict.return_value = {'E': {'E': 0, 'F': 0, 'D': 0, 'A': 0, 'C': 0, 'B': 0},
                                                      'F': {'E': 0, 'F': 0, 'D': 0, 'A': 0, 'C': 0, 'B': 0},
                                                      'D': {'E': 0, 'F': 0, 'D': 0, 'A': 0, 'C': 0, 'B': 0},
                                                      'A': {'E': 0, 'F': 0, 'D': 0, 'A': 0, 'C': 0, 'B': 0},
                                                      'C': {'E': 0, 'F': 1, 'D': 0, 'A': 0, 'C': 0, 'B': 0},
                                                      'B': {'E': 0, 'F': 0, 'D': 0, 'A': 0, 'C': 0, 'B': 0}}

                    simulation = Simulation(config, MockedGenerator)
                    for _ in range(11):
                        simulation.refresh()
                    k = 0
                    for bus in simulation.buses:
                        if bus.line.number == 1 and bus.route == 0:
                            k += 1
                            self.are_lists_equal(bus.passengers, [PassengersGroup('F', 1)],
                                                 passenger_group_equality)
                    self.are_equal(k, 1)
