import sys
import unittest

from core.simulation.line import Line
from utils.helpers import fullname

if sys.version_info[0] >= 3:
    import unittest.mock as mock
    from unittest.mock import PropertyMock
else:
    import mock
    from mock import PropertyMock


class BusTests(unittest.TestCase):
    @staticmethod
    def get_empty_line():
        return Line({'id': 0, 'bus_capacity': 0, "frequency1": 0, "frequency2": 0}, [], [])

    def BusTests(self):
        line_name = fullname(Line)
        with mock.patch(line_name + ".routes", new_callable=PropertyMock) as mocked_routes:
            mocked_routes.return_value = [["A"], ["B"]]
            line = BusTests.get_empty_line()
            assert line.routes != [["A"], ["B"]]
