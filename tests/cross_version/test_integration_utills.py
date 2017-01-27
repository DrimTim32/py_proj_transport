import pytest
from utils.helpers import get_full_class_name
from core.simulation import Stop, Simulation, Bus, PassengersGroup
from core.data_structures import Graph, Node
from core.simulation.generators import BusGenerator
from core.simulation.line import LineStop, Line


@pytest.mark.parametrize(("obj", "type"), [
    (Stop, "core.simulation.stop.Stop"),
    (Simulation, "core.simulation.simulation.Simulation"),
    (PassengersGroup, "core.simulation.passenger_group.PassengersGroup"),
    (Bus, "core.simulation.bus.Bus"),
    (Graph, "core.data_structures.graph.Graph"),
    (Node, "core.data_structures.graph.Node"),
    (BusGenerator, "core.simulation.generators.bus_generator.BusGenerator"),
    (LineStop, "core.simulation.line.LineStop"),
    (Line, "core.simulation.line.Line"),
])
def test_on_buitlin(obj, type):
    assert get_full_class_name(obj) == type
