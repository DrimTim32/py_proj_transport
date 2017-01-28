import sys
import unittest

import pytest

from core.simulation.bus import Bus
from core.simulation.line import Line, LineStop
from utils.helpers import get_full_class_name
from core.simulation.passenger_group import PassengersGroup

if sys.version_info[0] >= 3:
    import unittest.mock as mock
    from unittest.mock import PropertyMock
else:
    import mock
    from mock import PropertyMock


def get_empty_line():
    return Line({'id': 0, 'bus_capacity': 0, "frequency1": 0, "frequency2": 0}, [LineStop('', 0)], [LineStop('', 0)])


def get_group(count):
    gr = PassengersGroup("!", count)
    gr.count = count
    return gr

N = 7
counts = [[i] * ((2 * i) + N + 1) for i in range(2, N)]
q = []
for c in counts:
    q.append(list(zip([i for i in range(1, len(c) - 1)], c)))
q = [item for sublist in q for item in sublist]


class BusTests(unittest.TestCase):
    line_name = get_full_class_name(Line)

    def test_create(self):
        with mock.patch(BusTests.line_name + ".routes", new_callable=PropertyMock) as mocked_routes:
            mocked_routes.return_value = [[LineStop('A', 0), LineStop('', 0)], [LineStop('B', 0), LineStop('', 0)]]
            line = get_empty_line()
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


@pytest.mark.parametrize(("steps", "stops"), q)
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
        line = get_empty_line()

        bus = Bus(line, 0)
        bus2 = Bus(line, 1)
        bus.move()
        bus2.move()

        stop = 0
        for i in range(min(3 * stops - 4, steps)):  # 4 because of 4 = 2 ticks from end + 2 ticks from start
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

        if steps >= 3 * stops:
            for i in range(steps - 3 * stops + 1):
                bus2.move()
                bus.move()
            assert bus.next_stop_name == "None"
            assert bus2.next_stop_name == "None"
        else:
            assert bus.next_stop_name != "None"
            assert bus2.next_stop_name != "None"

class TestFill():
    def test_basic(self):
        with mock.patch(BusTests.line_name + ".bus_capacity", new_callable=PropertyMock) as mocked_bus_capacity:
            mocked_bus_capacity.return_value = 10
            group = get_group(10)
            bus = Bus(get_empty_line(), 0)
            assert bus.passengers == []
            assert [] == bus.fill([group])
            assert len(bus.passengers) == 1
            assert isinstance(bus.passengers[0], PassengersGroup)
            assert bus.passengers[0].count == 10

    def test_too_much_basic(self):
        with mock.patch(BusTests.line_name + ".bus_capacity", new_callable=PropertyMock) as mocked_bus_capacity:
            mocked_bus_capacity.return_value = 30
            group = get_group(10)
            bus = Bus(get_empty_line(), 0)
            assert bus.passengers == []
            #assert [PassengersGroup()] == bus.fill([group])
            #assert len(bus.passengers) == 1
            #assert isinstance(bus.passengers[0], PassengersGroup)
            #assert bus.passengers[0].count == 10

