"""
This file contains integration tests of utils module
"""
import pytest

from core.data_structures import Graph, Node
from core.simulation import Stop, Simulation, Bus, PassengersGroup
from core.simulation.line import LineStop, Line
from tests_utils.helpers import get_full_class_name


@pytest.mark.parametrize(("cls", "full_name"), [
    (Stop, "core.simulation.stop.Stop"),
    (Simulation, "core.simulation.simulation.Simulation"),
    (PassengersGroup, "core.simulation.passenger_group.PassengersGroup"),
    (Bus, "core.simulation.bus.Bus"),
    (Graph, "core.data_structures.graph.Graph"),
    (Node, "core.data_structures.graph.Node"),
    (LineStop, "core.simulation.line.LineStop"),
    (Line, "core.simulation.line.Line"),
])
def test_on_buitlin(cls, full_name):
    """
    Tests get_full_class_name method
    :param cls: class
    :param full_name: full class name
    """
    assert get_full_class_name(cls) == full_name
