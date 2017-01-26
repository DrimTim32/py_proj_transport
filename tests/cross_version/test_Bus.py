import unittest
import sys
from core.simulation import bus


if sys.version_info[0] >= 3:
    import unittest.mock as mock
    from unittest.mock import PropertyMock
else:
    import mock
    from mock import PropertyMock

class GraphTests(unittest.TestCase):
    def test_bus_creation(self):
        with mock.patch('core.configuration.config.Config.graph_dict', new_callable=PropertyMock) as graph_dict:
            pass

