"""
This file contains functional tests passenger generation
"""
import sys

import scipy.stats as st

from core.configuration import Config
from core.simulation import Simulation

if sys.version_info[0] >= 3:
    from unittest.mock import PropertyMock, patch
else:
    from mock import PropertyMock, patch


def test_passenger_generation():
    """Tests passenger generation"""
    with patch('core.configuration.Config.graph_dict', new_callable=PropertyMock) as mock_graph_dict:
        with patch('core.configuration.Config.lines_dict', new_callable=PropertyMock) as mock_lines_dict:
            with patch('core.configuration.Config.traffic_data_dict',
                       new_callable=PropertyMock) as mock_traffic_dict:
                mock_graph_dict.return_value = {'A': [('B', 1)],
                                                'B': [('A', 1)]}
                mock_lines_dict.return_value = {
                    0: {'id': 0, 'bus_capacity': 1, 'frequency1': 10000000, 'frequency2': 1000000000,
                        'route1': ['B', 'A'],
                        'route2': ['A', 'B']}}
                config = Config({}, {}, {}, {})
                config.stops = ["A", "B"]
                mock_traffic_dict.return_value = {'A': {'A': 0, 'B': 120},
                                                  'B': {'A': 0, 'B': 0}}

                generated = []
                simulation = Simulation(config)
                simulation.refresh()
                simulation.refresh()
                for i in range(100000):
                    simulation.refresh()
                    generated.append(simulation.stops['A'].passengers[0].count)

                for i in range(len(generated) - 1, 0, -1):
                    generated[i] -= generated[i - 1]

                prob = st.poisson.cdf(generated, 2)
                print(prob)
                assert 3 == 6
