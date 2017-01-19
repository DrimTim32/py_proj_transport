import json


class Config:
    def __init__(self, stops, connections, lines):
        self.stops = stops
        self.connections = connections
        self.lines = lines

    @staticmethod
    def from_config_file(file):
        f = open(file)
        data = json.load(f)
        return Config(data['stops'], data['connections'], data['lines'])

    @property
    def graph_dict(self):
        """
        :return: returns graph description
        :rtype: dict[str,List[tuple[str,int]]]
        """
        return {key: [tuple(pair) for pair in self.connections.get(key)] for key in self.connections.keys()}

    @property
    def lines_list(self):
        """
        :return: returns dict of lines
        :rtype: dict[str,dict[str,str]]
        """
        return {line.get("id"): {k: line.get(k) for k in line} for line in self.lines}
