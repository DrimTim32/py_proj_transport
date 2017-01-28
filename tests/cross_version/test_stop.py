import pytest
from core.simulation.passenger_group import PassengersGroup
from utils.helpers import get_full_class_name
import sys

if sys.version_info[0] >= 3:
    import unittest.mock as mock
else:
    import mock

from mock import PropertyMock

from core.simulation.stop import Stop
def test_create():
    s = Stop("name")
    assert s.name == 0
    for i in range(10):
        assert s.count(str(i)) == 0

def test_count(dests, counts):
    s = Stop("")
    name = get_full_class_name(PassengersGroup)
    for i in range(counts):
        with mock.patch(name+"destination",  new_callable=PropertyMock) as mocked_destination:
            mocked_destination.return_value = dests[i]
            with mock.patch(name + "count") as mocked_count:
                mocked_count.return_value = counts[i]
                group = PassengersGroup("a",0)
