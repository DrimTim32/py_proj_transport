import os

from configuration import config

stops = ['A', 'B', 'C', 'D', 'E', 'F']
graph_dict = {'A': [('B', 1), ('E', 1)], 'C': [('B', 2), ('D', 1)], 'F': [('B', 5), ('E', 1)], 'B': [('A', 1), ('C', 2), ('F', 5)], 'E': [('A', 1), ('F', 1)], 'D': [('C', 1)]}
lines_dict = {0: {'id': 0, 'route1': ['E', 'F', 'B', 'C', 'D'], 'bus_capacity': 20, 'frequency2': 20, 'frequency1': 20, 'route2': ['D', 'C', 'B', 'F', 'E']}, 1: {'id': 1, 'route1': ['E', 'A', 'B'], 'bus_capacity': 20, 'frequency2': 20, 'frequency1': 20, 'route2': ['B', 'A', 'E']}}
traffic_data_dict = {'A': {'A': 0, 'C': 0, 'F': 0, 'B': 0, 'E': 0, 'D': 0}, 'C': {'A': 0, 'C': 0, 'F': 0, 'B': 0, 'E': 0, 'D': 0}, 'F': {'A': 25, 'C': 0, 'F': 0, 'B': 0, 'E': 0, 'D': 0}, 'B': {'A': 0, 'C': 0, 'F': 0, 'B': 0, 'E': 0, 'D': 0}, 'E': {'A': 0, 'C': 0, 'F': 0, 'B': 0, 'E': 0, 'D': 0}, 'D': {'A': 12, 'C': 0, 'F': 0, 'B': 0, 'E': 25, 'D': 0}}
tick = 2.5

file_json = """{
  "stops": ["A", "B", "C", "D", "E", "F"],
  "connections": {
    "A": [["B", 1], ["E", 1]],
    "B": [["A", 1], ["C", 2], ["F", 5]],
    "C": [["B", 2], ["D", 1]],
    "D": [["C", 1]],
    "E": [["A", 1], ["F", 1]],
    "F": [["B", 5], ["E", 1]]
  },
  "lines": [
    {
      "id": 0,
      "bus_capacity": 20,
      "route1": ["E", "F", "B", "C", "D"],
      "frequency1": 20,
      "route2": ["D", "C", "B", "F", "E"],
      "frequency2": 20
    },
    {
      "id": 1,
      "bus_capacity": 20,
      "route1": ["E", "A", "B"],
      "frequency1": 20,
      "route2": ["B", "A", "E"],
      "frequency2": 20
    }
  ],
  "traffic_data": {
    "A": [["A", 0], ["B", 0], ["C", 0], ["D", 0], ["E", 0], ["F", 0]],
    "B": [["A", 0], ["B", 0], ["C", 0], ["D", 0], ["E", 0], ["F", 0]],
    "C": [["A", 0], ["B", 0], ["C", 0], ["D", 0], ["E", 0], ["F", 0]],
    "D": [["A", 12], ["B", 0], ["C", 0], ["D", 0], ["E", 25], ["F", 0]],
    "E": [["A", 0], ["B", 0], ["C", 0], ["D", 0], ["E", 0], ["F", 0]],
    "F": [["A", 25], ["B", 0], ["C", 0], ["D", 0], ["E", 0], ["F", 0]]
  },
  "tick": 2.5
}"""

def test_reading_from_file():
    text_file = open("test.json", "w")
    text_file.write(file_json)
    text_file.close()
    configuration = config.Config.from_config_file("test.json")
    assert configuration.stops == stops
    assert configuration.graph_dict == graph_dict
    assert configuration.lines_dict == lines_dict
    assert configuration.traffic_data_dict == traffic_data_dict
    assert configuration.tick == tick
    os.remove("test.json")
