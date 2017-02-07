"""
This file contains tests for Stop class
"""
import sys

import pytest

from simulation.passenger_group import PassengersGroup
from simulation.stop import Stop
from utils.helpers import get_full_class_name

if sys.version_info[0] >= 3:
    import unittest.mock as mock
    from unittest.mock import PropertyMock

else:
    import mock
    from mock import PropertyMock


def test_create():
    """Tests if stop is created correctly"""
    stop = Stop("name")
    assert stop.name == 'name'
    for i in range(10):
        assert stop.count(str(i)) == 0


@pytest.mark.parametrize("dest", ["A", "B", "C"])
@pytest.mark.parametrize("count", [0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
def test_coun_one_group(dest, count):
    """Tests if count is being calculated correctly"""
    stop = Stop("")
    name = get_full_class_name(PassengersGroup)
    with mock.patch(name + ".destination", new_callable=PropertyMock) as mocked_destination:
        mocked_destination.return_value = dest
        group = PassengersGroup("a", 0)
        group.count = count
        stop.passengers.append(group)
        assert stop.count(dest) == count
