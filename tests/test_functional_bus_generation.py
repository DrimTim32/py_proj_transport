"""
This file contains functional tests bus generation
"""
import sys

from simulation import Bus
from configuration import Config
from simulation import Simulation
from utils.helpers import get_full_class_name
if sys.version_info[0] >= 3:
    from unittest.mock import PropertyMock, patch
else:
    from mock import PropertyMock, patch


def test_bus_generation():
    """Tests bus generation"""
    config_name = get_full_class_name(Config)
    with patch(config_name + '.graph_dict', new_callable=PropertyMock) as mock_graph_dict:
        with patch(config_name + '.lines_dict', new_callable=PropertyMock) as mock_lines_dict:
            with patch(config_name + '.traffic_data_dict',
                       new_callable=PropertyMock) as mock_traffic_dict:
                mock_graph_dict.return_value = {'A': [('B', 1)],
                                                'B': [('A', 1)]}
                mock_lines_dict.return_value = {
                    0: {'id': 0, 'bus_capacity': 20, 'frequency1': 10, 'frequency2': 1000,
                        'route1': ['B', 'A'],
                        'route2': ['A', 'B']}}
                config = Config({}, {}, {}, {})
                config.stops = ["A", "B"]
                mock_traffic_dict.return_value = {'A': {'A': 0, 'B': 0},
                                                  'B': {'A': 0, 'B': 0}}

                simulation = Simulation(config)
                assert Bus.BUS_COUNTER == 0
                simulation.refresh()
                simulation.refresh()
                assert Bus.BUS_COUNTER == 2

                for i in range(1, 10):
                    for _ in range(10):
                        simulation.refresh()
                    assert Bus.BUS_COUNTER == 2 + i
