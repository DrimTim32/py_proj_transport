"""
This file contains test for Bus class
"""
import sys

import pytest

from core.simulation import Bus
from core.simulation.line import Line, LineStop
from core.simulation.passenger_group import PassengersGroup
from tests_utils.TestsBase import TestBase
from tests_utils.helpers import get_full_class_name

if sys.version_info[0] >= 3:
    import unittest.mock as mock
    from unittest.mock import PropertyMock
else:
    import mock
    from mock import PropertyMock


# region
def get_empty_line():
    """Creates empty line"""
    return Line({'id': 0, 'bus_capacity': 0, "frequency1": 0, "frequency2": 0}, [LineStop('', 0)], [LineStop('', 0)])


def passenger_group_equality(first_group, second_group):
    """
    Checks if two passenger groups are equal
    :param first_group: first group
    :param second_group: second group
    :return: True if are equal False if not
    :rtype: bool
    """
    return first_group.count == second_group.count and first_group.destination == second_group.destination


def get_group(count, name="!"):
    """
    Creates PassengersGroup with parameters
    :param count: group count
    :param name: group name
    :return: Passengers Group
    :rtype: PassengersGroup
    """
    group = PassengersGroup(name, count)
    group.name = name
    group.count = count
    return group


LINE_NAME = get_full_class_name(Line)


def test_create():
    """
    Checks if bus is created properly
    """
    with mock.patch(LINE_NAME + ".routes", new_callable=PropertyMock) as mocked_routes:
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


N_RANGE = 7
COUNTS = [[i] * ((2 * i) + N_RANGE + 1) for i in range(2, N_RANGE)]
TEST_ARRAY = []
for _count in COUNTS:
    TEST_ARRAY.append(list(zip([i for i in range(1, len(_count) - 1)], _count)))
TEST_ARRAY = [item for sublist in TEST_ARRAY for item in sublist]


@pytest.mark.parametrize(("steps", "stops"), TEST_ARRAY)
def test_move(steps, stops):
    """
    Tests if bus is moving properly
    :param steps: steps to move
    :param stops: stops count on the line
    """
    with mock.patch(LINE_NAME + ".routes", new_callable=PropertyMock) as mocked_routes:

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


class TestFill(TestBase):
    """
    Group for filling tests
    """
    def test_basic(self):
        """
        Fills bus with one group without overflow
        """
        with mock.patch(LINE_NAME + ".bus_capacity", new_callable=PropertyMock) as mocked_bus_capacity:
            mocked_bus_capacity.return_value = 10
            group = get_group(10)
            bus = Bus(get_empty_line(), 0)
            assert bus.passengers == []
            assert [] == bus.fill([group])
            assert len(bus.passengers) == 1
            assert isinstance(bus.passengers[0], PassengersGroup)
            assert bus.passengers[0].count == 10

    def test_overflow_basic(self):
        """
        Fills bus with one group with overflow
        """
        with mock.patch(LINE_NAME + ".bus_capacity", new_callable=PropertyMock) as mocked_bus_capacity:
            mocked_bus_capacity.return_value = 10
            group = get_group(30, "A")
            bus = Bus(get_empty_line(), 0)
            self.are_lists_equal(bus.passengers, [])
            after_fill = bus.fill([group])
            self.are_lists_equal([PassengersGroup("A", 20)], after_fill, passenger_group_equality)
            assert len(bus.passengers) == 1
            assert bus.count == 10
            assert isinstance(bus.passengers[0], PassengersGroup)
            self.are_equal(bus.passengers[0], PassengersGroup("A", 10), passenger_group_equality)

    def test_two_different_in_one(self):
        """
        Fills bus with two groups (as one list) without overflow
        """
        with mock.patch(LINE_NAME + ".bus_capacity", new_callable=PropertyMock) as mocked_bus_capacity:
            mocked_bus_capacity.return_value = 20
            group1 = get_group(10, "A")
            group2 = get_group(10, "B")
            bus = Bus(get_empty_line(), 0)
            self.are_lists_equal(bus.passengers, [])
            after_fill = bus.fill([group1, group2])
            assert after_fill == []
            assert bus.count == 20
            assert len(bus.passengers) == 2
            assert group1 in bus.passengers
            assert group2 in bus.passengers
            assert bus.passengers[0] != bus.passengers[1]

    def test_two_different_in_one_overflow(self):
        """
        Fills bus with two groupss (as one list) with overflow
        """
        with mock.patch(LINE_NAME + ".bus_capacity", new_callable=PropertyMock) as mocked_bus_capacity:
            mocked_bus_capacity.return_value = 20
            group1 = get_group(10, "A")
            group2 = get_group(30, "B")
            bus = Bus(get_empty_line(), 0)
            self.are_lists_equal(bus.passengers, [])
            after_fill = bus.fill([group1, group2])
            assert sum([i.count for i in after_fill]) == 20
            assert after_fill != []
            assert bus.count == 20
            assert len(bus.passengers) == 2
            assert bus.passengers[0] != bus.passengers[1]

    def test_two_different_in_two_overflow(self):
        """
        Fills bus with two groups one by one with overflow
        """
        with mock.patch(LINE_NAME + ".bus_capacity", new_callable=PropertyMock) as mocked_bus_capacity:
            mocked_bus_capacity.return_value = 20
            group1 = get_group(10, "A")
            group2 = get_group(30, "B")
            bus = Bus(get_empty_line(), 0)
            self.are_lists_equal(bus.passengers, [])
            after_fill = bus.fill([group1])
            assert after_fill == []
            assert bus.count == 10
            assert len(bus.passengers) == 1
            after_fill = bus.fill([group2])
            self.are_lists_equal(after_fill, [get_group(20, "B")], passenger_group_equality)
            assert bus.count == 20
            assert len(bus.passengers) == 2

    def test_add_the_same_overflow(self):
        """
        Fills bus with two identical groupss with overflow
        """
        with mock.patch(LINE_NAME + ".bus_capacity", new_callable=PropertyMock) as mocked_bus_capacity:
            mocked_bus_capacity.return_value = 20
            group1 = get_group(10, "A")
            group2 = get_group(30, "A")
            bus = Bus(get_empty_line(), 0)
            self.are_lists_equal(bus.passengers, [])
            after_fill = bus.fill([group1])
            assert bus.count == 10
            assert len(bus.passengers) == 1
            after_fill = bus.fill([group2])
            self.are_lists_equal(after_fill, [get_group(20, "A")], passenger_group_equality)
            assert bus.count == 20
            assert len(bus.passengers) == 1
            self.are_equal(bus.passengers[0], get_group(20, "A"), passenger_group_equality)

    def test_add_the_same(self):
        """
        Fills bus with two identical groupss without overflow
        """
        with mock.patch(LINE_NAME + ".bus_capacity", new_callable=PropertyMock) as mocked_bus_capacity:
            mocked_bus_capacity.return_value = 20
            group1 = get_group(10, "A")
            group2 = get_group(9, "A")
            bus = Bus(get_empty_line(), 0)
            assert bus.passengers == []
            after_fill = bus.fill([group1])
            assert after_fill == []
            assert bus.count == 10
            assert len(bus.passengers) == 1
            after_fill = bus.fill([group2])
            assert after_fill == []
            assert bus.count == 19
            assert len(bus.passengers) == 1
            self.are_equal(bus.passengers[0], get_group(19, "A"), passenger_group_equality)
