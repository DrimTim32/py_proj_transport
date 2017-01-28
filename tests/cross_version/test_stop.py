import pytest
from core.simulation.passenger_group import PassengersGroup
from tests_utils.helpers import get_full_class_name
import sys

if sys.version_info[0] >= 3:
    import unittest.mock as mock
else:
    import mock

from mock import PropertyMock, MagicMock

from core.simulation.stop import Stop


def test_create():
    s = Stop("name")
    assert s.name == 'name'
    for i in range(10):
        assert s.count(str(i)) == 0


@pytest.mark.parametrize("dest", ["A", "B", "C"])
@pytest.mark.parametrize("count", [0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
def test_coun_one_group(dest, count):
    s = Stop("")
    name = get_full_class_name(PassengersGroup)
    with mock.patch(name + ".destination", new_callable=PropertyMock) as mocked_destination:
        mocked_destination.return_value = dest
        group = PassengersGroup("a", 0)
        group.count = count
        s.passengers.append(group)
        assert s.count(dest) == count
