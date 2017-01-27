import unittest
import sys
from core.simulation.bus import Bus
from core.simulation.line import Line


if sys.version_info[0] >= 3:
    import unittest.mock as mock
    from unittest.mock import PropertyMock
else:
    import mock
    from mock import PropertyMock

class GraphTests(unittest.TestCase):
    def test_bus_creation(self):
        pass

