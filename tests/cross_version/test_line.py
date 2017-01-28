from core.simulation.line import Line, LineStop
import unittest


class LineTests(unittest.TestCase):
    def test_create(self):
        stops_left = [LineStop("Al", 1), LineStop("B", 1), LineStop("C", 1), LineStop("Dl", 1)]
        stops_right = [LineStop("Ar", 1), LineStop("B", 1), LineStop("C", 1), LineStop("Dr", 1)]
        line = Line({
            'id': 123,
            'bus_capacity': 10,
            'frequency1': 10,
            'frequency2': 5
        }, stops_left, stops_right
        )
        self.assertEqual(line.number,123)
        self.assertEqual(line.bus_capacity, 10)
        self.assertEqual(line.first_stop_name(0), "Al")
        self.assertEqual(line.last_stop_name(0), "Dl")
        self.assertEqual(line.first_stop_name(1), "Ar")
        self.assertEqual(line.last_stop_name(1), "Dr")
        self.assertEqual(line.frequencies, [10, 5])
        self.assertEqual(line.routes, [
            [LineStop('P', 1)] + stops_left, [LineStop('P', 1)] + stops_right
        ])
