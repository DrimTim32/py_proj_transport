"""
This file contains functional tests for simulation class
"""
import sys

import time
import unittest

from core.configuration import Config
from core.simulation import Simulation
from tests_utils.helpers import add_property, add_variable

if sys.version_info[0] >= 3:
    from unittest.mock import PropertyMock, patch
else:
    from mock import PropertyMock, patch


class SimulationTest(unittest.TestCase):
    """Class for testing simulation class"""

    def test_graph_and_lines(self):
        """Tests simulation with graph and lines"""
        with patch('core.configuration.Config.graph_dict', new_callable=PropertyMock) as mock_graph_dict:
            with patch('core.configuration.Config.lines_dict', new_callable=PropertyMock) as mock_lines_dict:
                with patch('core.configuration.Config.traffic_data_dict',
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
                    config = Config({}, {}, {}, {})
                    config.stops = ["A", "B", "C", "D", "E", "F"]
                    mock_traffic_dict.return_value = {'E': {'E': 0, 'F': 0, 'D': 0, 'A': 0, 'C': 0, 'B': 0},
                                                      'F': {'E': 0, 'F': 0, 'D': 0, 'A': 0, 'C': 0, 'B': 0},
                                                      'D': {'E': 0, 'F': 0, 'D': 0, 'A': 0, 'C': 0, 'B': 0},
                                                      'A': {'E': 0, 'F': 0, 'D': 0, 'A': 0, 'C': 0, 'B': 0},
                                                      'C': {'E': 0, 'F': 0, 'D': 0, 'A': 0, 'C': 0, 'B': 0},
                                                      'B': {'E': 0, 'F': 0, 'D': 0, 'A': 0, 'C': 0, 'B': 0}}

                    simulation = Simulation(config)

                def mocked_update(mocked_self):
                    """Mocked update """
                    for bus in mocked_self._buses:
                        if bus.route == 0:
                            if bus.id not in mocked_self.mocked_dict.keys():
                                mocked_self.mocked_dict[bus.id] = []
                            if bus.time_to_next_stop == 0:
                                mocked_self.mocked_dict[bus.id].append(bus.current_stop_name)
                            else:
                                mocked_self.mocked_dict[bus.id].append(bus.current_stop_name + bus.next_stop_name)

                def finished(mocked_self):
                    time.sleep = lambda x: None
                    if mocked_self.count_finished == 35:
                        return True
                    mocked_self.count_finished += 1
                    mocked_self.mocked_update()
                    return False

                add_property(simulation, "finished", finished)
                from types import MethodType
                simulation.mocked_update = MethodType(mocked_update, simulation)
                add_variable(simulation, "count_finished", 0)
                add_variable(simulation, "mocked_dict", {})
                simulation.mainloop()
                paths = ['PA', 'A', 'AD', 'AD', 'D', 'DC', 'DC', 'DC', 'C', 'CB', 'B', 'BE', 'BE', 'E', 'EF', 'EF', 'F']
                self.assertEqual(len(simulation.mocked_dict), 2)
                for path in simulation.mocked_dict.values():
                    self.assertEqual(path, paths)
