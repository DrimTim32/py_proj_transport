import pytest
from utils.helpers import fullname
import sys
import unittest
from core.simulation.bus import Bus
from core.simulation.line import Line, LineStop

if sys.version_info[0] >= 3:
    import unittest.mock as mock
    from unittest.mock import PropertyMock
else:
    import mock
    from mock import PropertyMock

class BusTests(unittest.TestCase):
    line_name = fullname(Line)

    @staticmethod
    def get_empty_line():
        return Line({'id': 0, 'bus_capacity': 0, "frequency1": 0, "frequency2": 0}, [], [])

    def test_create(self):
        with mock.patch(BusTests.line_name + ".routes", new_callable=PropertyMock) as mocked_routes:
            mocked_routes.return_value = [[LineStop('A', 0), LineStop('', 0)], [LineStop('B', 0), LineStop('', 0)]]
            line = BusTests.get_empty_line()
            bus = Bus(line, 0)
            bus2 = Bus(line, 1)
            assert bus.passengers == []
            assert bus.line == line
            assert bus.time_to_next_stop == 0
            assert bus.current_stop_name == 'A'
            assert bus.current_stop == 0
            assert bus2.passengers == []
            assert bus2.line == line
            assert bus2.time_to_next_stop == 0
            assert bus2.current_stop_name == 'B'
            assert bus2.current_stop == 0


counts = [[i] * (2 * i - 1) for i in range(2, 7)]
q = []
for c in counts:
    q.append(list(zip([i for i in range(1, len(c) - 1)], c)))
q = [item for sublist in q for item in sublist]


@pytest.mark.parametrize(("steps", "stops"),
                         q
                         )
def test_move(steps, stops):
    with mock.patch(BusTests.line_name + ".routes", new_callable=PropertyMock) as mocked_routes:

        lines_left = [LineStop('l' + str(i), 2) for i in range(stops)]
        lines_left = [LineStop('P', 1)] + lines_left

        lines_right = [LineStop('r' + str(i), 2) for i in range(stops)]
        lines_right = [LineStop('P', 1)] + lines_right
        mocked_routes.return_value = [
            lines_left,
            lines_right
        ]
        line = BusTests.get_empty_line()

        bus = Bus(line, 0)
        bus2 = Bus(line, 1)
        bus.move()
        bus2.move()

        stop = 0
        for i in range(steps):
            bus.move()
            bus2.move()
            if 2 - (i % 3) == 0:
                stop += 1
            assert bus.time_to_next_stop == 2 - (i % 3), "i = {}".format(i)
            assert bus.current_stop_name == 'l' + str(stop)
            assert bus.current_stop == (i // 3) + 1, "i = {}".format(i)

            assert bus2.time_to_next_stop == 2 - (i % 3), "i = {}".format(i)
            assert bus2.current_stop_name == 'r' + str(stop)
            assert bus2.current_stop == (i // 3) + 1, "i = {}".format(i)
        if stops * 2 <= steps:
            assert bus.next_stop_name is None
            assert bus2.next_stop_name is None
        else:
            assert bus.next_stop_name is not None
            assert bus2.next_stop_name is not None
