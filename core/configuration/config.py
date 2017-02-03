"""
File containing Config class
"""
import json


class Config:
    """
    Configuration class
    """
    def __init__(self, stops, connections, lines, traffic_data):
        self.stops = stops
        self.connections = connections
        self.lines = lines
        self.traffic_data = traffic_data

    @staticmethod
    def from_config_file(file_name):
        """
        :param file_name: name of file with configuration
        :type file_name: str
        :return: Config object constructed from given file
        :rtype: Config
        """
        file = open(file_name)
        data = json.load(file)
        return Config(data['stops'], data['connections'], data['lines'], data['traffic_data'])

    @property
    def graph_dict(self):
        """
        :return: returns graph description
        :rtype: dict[str,List[tuple[str,int]]]
        """
        return {key: [tuple(pair) for pair in self.connections.get(key)] for key in self.connections.keys()}

    @property
    def lines_dict(self):
        """
        :return: returns dict of lines
        :rtype: dict[str,dict[str,str]]
        """
        return {line.get("id"): {k: line.get(k) for k in line} for line in self.lines}

    @property
    def traffic_data_dict(self):
        """
        :return: dict with passenger traffic data
        :rtype: dict[str,dict[str, int]]
        """
        return {source: {dest[0]: dest[1] for dest in self.traffic_data.get(source)}
                for source in self.traffic_data.keys()}
