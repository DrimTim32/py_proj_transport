import sys
import unittest

if sys.version_info[0] >= 3:
    pass
else:
    pass


class GraphTests(unittest.TestCase):
    def test_bus_creation(self):
        with mock.patch('core.configuration.config.Config.graph_dict', new_callable=PropertyMock) as graph_dict:
            pass

