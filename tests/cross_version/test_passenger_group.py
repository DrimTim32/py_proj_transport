import pytest

from core.simulation.passenger_group import PassengersGroup

@pytest.mark.parametrize(("dest", "count"),
                         [
                             ("A", 10),
                             ("B", 123),
                             ("G", 12),
                             ("B", 112),
                         ])
def test_create(dest, count):
    """Tests if Passenger group is created correctly"""
    group = PassengersGroup(dest, count)
    assert group.count == count
    assert group.destination == dest


@pytest.mark.parametrize("count", [-1, -2, -3, -4, -5, -6, -99, -12321])
def test_bad_count_create(count):
    """Checks if negative count raises an error"""
    with pytest.raises(ValueError) as exception_info:
        PassengersGroup("DEST", count)
    assert 'count' in str(exception_info.value)


def test_bad_dest_create():
    """Checks if empty destination raises an error"""
    with pytest.raises(ValueError) as exception_info:
        PassengersGroup("", 123)
    assert 'destination' in str(exception_info.value)


@pytest.mark.parametrize(("count1"), [1, 2, 3, 4, 5, 6])
@pytest.mark.parametrize(("count2"), [1, 2, 3, 4, 5, 6])
def test_good_sum(count1, count2):
    """Tests if sum is being calculated properly"""
    group1 = PassengersGroup("dest", count1)
    group2 = PassengersGroup("dest", count2)
    group3 = group1 + group2
    assert group1.destination == group3.destination
    assert group2.destination == group3.destination
    assert group3.count == count1 + count2


@pytest.mark.parametrize(("dest1"), ["a", "b", "c"])
@pytest.mark.parametrize(("dest2"), ["g", "e", "f"])
def test_bad_dest_sum(dest1, dest2):
    """Tests if sum of two groups throw an exception if groups have different destinations"""
    group1 = PassengersGroup(dest1, 0)
    group2 = PassengersGroup(dest2, 0)
    with pytest.raises(TypeError) as exception_info:
        group1 + group2
    assert 'destination' in str(exception_info.value)
    assert 'groups' in str(exception_info.value)


@pytest.mark.parametrize(("obj"), [1, "a", 0.33, object()])
def test_bad_type_sum(obj):
    """Tests if second object is not a group"""
    group = PassengersGroup("dest", 123)
    with pytest.raises(TypeError) as exception_info:
        group + obj
    assert 'instance' in str(exception_info.value)
