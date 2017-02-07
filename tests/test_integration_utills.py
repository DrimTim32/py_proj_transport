"""
This file contains integration tests of utils module
"""
import pytest

from data_structures import Graph, Node
from simulation import Stop, Simulation, Bus, PassengersGroup
from simulation.line import LineStop, Line
from utils.helpers import get_full_class_name


@pytest.mark.parametrize(("cls", "full_name"), [
    (Stop, "simulation.stop.Stop"),
    (Simulation, "simulation.simulation.Simulation"),
    (PassengersGroup, "simulation.passenger_group.PassengersGroup"),
    (Bus, "simulation.bus.Bus"),
    (Graph, "data_structures.graph.Graph"),
    (Node, "data_structures.graph.Node"),
    (LineStop, "simulation.line.LineStop"),
    (Line, "simulation.line.Line"),
])
def test_on_buitlin(cls, full_name):
    """
    Tests get_full_class_name method
    :param cls: class
    :param full_name: full class name
    """
    assert get_full_class_name(cls) == full_name
