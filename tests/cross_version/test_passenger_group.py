import pytest

from core.simulation.passenger_group import PassengersGroup


@pytest.mark.parametrize(("dest", "count"),
                         [
                             ("A", 10),
                             ("B", 123),
                             ("G", 12),
                             ("B", 112),
                         ]
                         )
def test_create(dest, count):
    group = PassengersGroup(dest, count)
    assert group.count == count
    assert group.destination == dest


@pytest.mark.parametrize("count", [-1, -2, -3, -4, -5, -6, -99, -12321])
def test_bad_count_create(count):
    with pytest.raises(ValueError) as exceptionInfo:
        g = PassengersGroup("DEST", count)
    assert 'count' in str(exceptionInfo.value)


def test_bad_dest_create():
    with pytest.raises(ValueError) as exceptionInfo:
        g = PassengersGroup("", 123)
    assert 'destination' in str(exceptionInfo.value)


@pytest.mark.parametrize(("count1"), [1, 2, 3, 4, 5, 6])
@pytest.mark.parametrize(("count2"), [1, 2, 3, 4, 5, 6])
def test_good_sum(count1, count2):
    gr1 = PassengersGroup("dest", count1)
    gr2 = PassengersGroup("dest", count2)
    gr3 = gr1 + gr2
    assert gr1.destination == gr3.destination
    assert gr2.destination == gr3.destination
    assert gr3.count == count1 + count2


@pytest.mark.parametrize(("dest1"), ["a", "b", "c"])
@pytest.mark.parametrize(("dest2"), ["g", "e", "f"])
def test_bad_dest_sum(dest1, dest2):
    g1 = PassengersGroup(dest1, 0)
    g2 = PassengersGroup(dest2, 0)
    with pytest.raises(TypeError) as exceptionInfo:
        g3 = g1 + g2
    assert 'destination' in str(exceptionInfo.value)
    assert 'groups' in str(exceptionInfo.value)


@pytest.mark.parametrize(("obj"), [1, "a", 0.33, object()])
def test_bad_type_sum(obj):
    g1 = PassengersGroup("dest", 123)
    with pytest.raises(TypeError) as exceptionInfo:
        g3 = g1 + obj
    assert 'instance' in str(exceptionInfo.value)
