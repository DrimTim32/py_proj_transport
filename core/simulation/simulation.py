"""
File containing main Simulation class
"""
from core.data_structures import Graph
from core.simulation import Bus
from core.simulation import PassengersGroup
from core.simulation.generators import PoissonPassengerGenerator
from core.simulation.line import LineStop, Line
from core.simulation.stop import Stop


class Simulation:
    def __init__(self, config, passenger_generator=PoissonPassengerGenerator):
        """
        Read configuration and do sth with it
        :param config
        :type config: Config
        """
        Bus.BUS_COUNTER = 0
        self.finished = False
        self.steps = -1
        self.__buses = []
        self.__lines = []
        self.__stops = {}
        self.__create_stops(config.stops)
        self.__graph = Graph.from_config(config.graph_dict)
        self.__create_lines(config.lines_dict)
        self.__passengers_generator = passenger_generator(config.traffic_data_dict)

    @property
    def buses(self):
        return self.__buses

    @property
    def stops(self):
        return self.__stops

    @property
    def lines(self):
        return self.__lines

    def refresh(self):
        """
        Main loop
        :return: None
        """
        if not self.finished:
            self.__update()
            self._print()

    def _print(self):
        """
        tego nie bydzie, nie komentuje
        :return:
        """
        if self.steps >= 1:
            print('________________________________________________________')
            print('STEP ', self.steps)
            for bus in self.__buses:
                print('Bus{ id:', bus.id, 'line:', bus.line.number, 'route:', bus.route, 'last stop:',
                      bus.current_stop_name,
                      ' next stop:', bus.next_stop_name, 'time to next:', bus.time_to_next_stop)
                if bus.passengers:
                    for group in bus.passengers:
                        print(group.destination, group.count)
            for stop in self.__stops.values():
                print(stop.name, "________________")
                if stop.passengers:
                    wait = 0
                    for group in stop.passengers:
                        print(group.destination, group.count)

                else:
                    print(0)

    def __update(self):
        """
        updates simulation state
        :return: None
        """
        self.steps += 1
        self.__update_stops()
        self.__update_buses()
        self.__update_passengers()
        self.__clean_buses()
        self.__generate_buses()

    def __update_stops(self):
        for src in self.__stops.keys():
            for dest in self.__stops.keys():
                if src is not dest:
                    new_passengers = self.__passengers_generator.generate(src, dest)
                    if new_passengers > 0:
                        source_stop = self.__stops[src]
                        i = 0
                        while i in range(len(source_stop.passengers)):
                            stop_group = source_stop.passengers[i]
                            if stop_group.destination == dest:
                                stop_group.count += new_passengers
                                break
                            i += 1
                        if i == len(source_stop.passengers):
                            source_stop.passengers.append(PassengersGroup(dest, new_passengers))

    def __update_buses(self):
        for bus in self.__buses:
            bus.move()

    def __update_passengers(self):
        for bus in self.__buses:
            if bus.time_to_next_stop == 0:
                Simulation.__transfer_out(self.__stops[bus.current_stop_name], bus)
                self.__transfer_between(self.__stops[bus.current_stop_name], bus)
                self.__transfer_in(self.__stops[bus.current_stop_name], bus)

    @staticmethod
    def __transfer_out(stop, bus):
        for bus_group in bus.passengers:  # wysiadanie
            if bus_group.destination == stop.name:
                bus.passengers.remove(bus_group)
                break

    def __transfer_in(self, stop, bus):
        in_groups = []
        for stop_group in stop.passengers:  # wsiadanie
            destination = stop_group.destination
            if self.__graph.get_path_between(stop.name, destination)[0] == bus.next_stop_name:
                in_groups.append(stop_group)
        stop.passengers = [group for group in stop.passengers if group not in in_groups]
        groups_after_fill = bus.fill(in_groups)
        for group in groups_after_fill:
            stop.passengers.append(group)

    def __transfer_between(self, stop, bus):
        for bus_group in bus.passengers:  # wysiadanie do przesiadki
            if self.__graph.get_path_between(stop.name, bus_group.destination)[0] != bus.next_stop_name:
                j = 0
                while j in range(len(stop.passengers)):
                    stop_group = stop.passengers[j]
                    if stop_group.destination == bus_group.destination:
                        stop_group += bus_group
                        break
                    j += 1
                if j == len(stop.passengers):
                    stop.passengers.append(bus_group)
                bus.passengers.remove(bus_group)

    def __generate_buses(self):
        for line in self.__lines:
            new_buses = line.tick()
            for i in range(len(new_buses)):
                if new_buses[i]:
                    self.__buses.append(Bus(line, i))

    def __clean_buses(self):
        buses_to_remove = [bus for bus in self.__buses if bus.current_stop == bus.line.last_stop(bus.route)]
        for bus in buses_to_remove:
            self.__buses.remove(bus)

    def __create_lines(self, lines):
        for line in lines.values():
            route1, route2 = [], []
            curr_route = line['route1']
            for i in range(len(curr_route)):
                route1.append(LineStop(curr_route[i],
                                       self.__graph[curr_route[i], curr_route[i + 1]] if i < len(
                                           curr_route) - 1 else 0))

            curr_route = line['route2']
            for i in range(len(curr_route)):
                route2.append(LineStop(curr_route[i],
                                       self.__graph[curr_route[i], curr_route[i + 1]] if i < len(
                                           curr_route) - 1 else 0))

            self.__lines.append(Line(line, route1, route2))

    def __create_stops(self, stops):
        self.__stops = {stop_name: Stop(stop_name) for stop_name in stops}
