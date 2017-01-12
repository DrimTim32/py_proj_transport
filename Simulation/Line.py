class Line:
    def __init__(self,graph,number,timetable):
        self.graph = graph
        self.number = number
        self.timetable = timetable

    @staticmethod
    def from_config(configuration):
        """
        Creates a line from config data
        @:param configuration
        """
        pass

    def get_path(self,node1,node2):
        """
        Calculates path from node1 to node2
        :param node1:
        :param node2:
        :return: list of all nodes between
        """
