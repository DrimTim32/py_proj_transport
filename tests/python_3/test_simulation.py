import sys
import types
import unittest
from copy import copy

from core.configuration import Config
from core.simulation import Simulation

if sys.version_info[0] >= 3:
    from unittest.mock import PropertyMock, patch
else:
    from mock import PropertyMock, patch


class SimulationTest(unittest.TestCase):
    @staticmethod
    def copy_func(f, name=None):
        return types.FunctionType(f.func_code, f.func_globals, name or f.func_name,
                                  f.func_defaults, f.func_closure)

    def test_graph_and_lines(self):
        with patch('core.configuration.Config.graph_dict', new_callable=PropertyMock) as mock_graph_dict:
            with patch('core.configuration.Config.lines_dict', new_callable=PropertyMock) as mock_lines_dict:
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
                config = Config({}, {}, {})
                config.stops = ["A", "B", "C", "D", "E", "F"]
                simulation = Simulation(config)
                bardzo_ladna_kopia_updejt = copy(simulation._update)

                fajny_slownik = {}

                def foo():
                    bardzo_ladna_kopia_updejt()
                    for bus in simulation.buses:
                        if bus.route == 0:
                            if bus.id not in fajny_slownik.keys():
                                fajny_slownik[bus.id] = []
                            if bus.time_to_next_stop == 0:
                                fajny_slownik[bus.id].append(bus.current_stop_name)
                            else:
                                fajny_slownik[bus.id].append(bus.current_stop_name + bus.next_stop_name)

                def fajny_mejnloop():
                    while not simulation.finished:
                        foo()
                        if simulation.steps == 33:
                            simulation.finished = True

                simulation.mainloop = fajny_mejnloop
                simulation.mainloop()

                pathsy = ['PA', 'A', 'AD', 'AD', 'D', 'DC', 'DC', 'DC', 'C', 'CB', 'B', 'BE', 'BE', 'E', 'EF', 'EF',
                          'F']
                for path in fajny_slownik.values():
                    self.assertEqual(path, pathsy)
                self.assertEqual(len(fajny_slownik), 2)
