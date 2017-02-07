"""This file contains GUI class"""
import sys

if sys.version_info[0] >= 3:
    import tkinter as tk
    from tkinter import ttk
else:
    import Tkinter as tk
    import ttk


class GUI():
    """This class handles windows for the project"""
    def __init__(self, simulation):
        """
        Read simulation and generate GUI
        :param simulation
        :type simulation: Simulation
        """
        self.simulation = simulation
        self.root = tk.Tk()
        self.note = ttk.Notebook(self.root)
        self.tab1 = []
        self.tab2 = []
        self.tab3 = []
        self.button = tk.Button(self.root, text="Pause", command=self.__pause)
        self.button.pack(side=tk.BOTTOM)
        self.__create_tabs()
        self.__create_tables()
        self.root.resizable(height=False, width=False)
        self.is_executing = True

    def __create_tabs(self, *args):
        """
        creates three tabs in GUI
        :return: None
        """
        self.tab1 = tk.Frame(self.note)
        self.tab2 = tk.Frame(self.note)
        self.tab3 = tk.Frame(self.note)
        self.note.add(self.tab1, text="     Lines       ")
        self.note.add(self.tab2, text="     Stops       ")
        self.note.add(self.tab3, text="     Buses       ")
        self.note.pack(side=tk.TOP)

    def __create_tables(self):
        """
        adds tables to tabs
        :return: None
        """
        self.__create_lines_table()
        self.__create_stops_table()
        self.__create_buses_table()

    def __create_lines_table(self):
        """
        creates table that displays lines
        :return: None
        """
        i = 0
        rows = []
        cols = []
        self.__add_item('number', self.tab1, i, 0, cols)
        self.__add_item('last stop', self.tab1, i, 1, cols)
        self.__add_item('route', self.tab1, i, 2, cols)
        self.__add_item('frequency', self.tab1, i, 3, cols)
        self.__add_item('bus capacity', self.tab1, i, 4, cols)
        rows.append(cols)
        i += 1
        for line in self.simulation.lines:
            cols = []
            self.__add_item(line.number, self.tab1, i, 0, cols)
            self.__add_item(line.last_stop_name(0), self.tab1, i, 1, cols)
            _route = [stop.name.encode("utf-8") for stop in line.routes[0] if stop.name != "P"]
            self.__add_item(_route, self.tab1, i, 2, cols)
            self.__add_item(line.frequencies[0], self.tab1, i, 3, cols)
            self.__add_item(line.bus_capacity, self.tab1, i, 4, cols)
            i += 1
            cols = []
            self.__add_item(line.number, self.tab1, i, 0, cols)
            self.__add_item(line.last_stop_name(1), self.tab1, i, 1, cols)
            _route = [stop.name.encode("utf-8") for stop in line.routes[1] if stop.name != "P"]
            self.__add_item(_route, self.tab1, i, 2, cols)
            self.__add_item(line.frequencies[1], self.tab1, i, 3, cols)
            self.__add_item(line.bus_capacity, self.tab1, i, 4, cols)
            i += 1
            rows.append(cols)

    def __create_stops_table(self):
        """
        creates table that displays stops
        :return: None
        """
        all_stops_info = []
        for key, value in self.simulation.stops.items():

            if sys.version_info[0] >= 3:
                temp = [key, value]
            else:
                temp = [key.encode("utf-8"), value]
            all_stops_info.append(temp)
        all_stops_info.sort()
        nr_stops = len(all_stops_info)
        i = 0
        rows = []
        cols = []
        self.__add_item('name', self.tab2, i, 0, cols)
        j = 0
        for element in all_stops_info:
            self.__add_item(('to ' + element[0]), self.tab2, i, j + 1, cols)
            j += 1
        rows.append(cols)
        i += 1
        for current_stop in range(nr_stops):
            cols = []
            j = 0
            self.__add_item(all_stops_info[current_stop][0], self.tab2, current_stop + 1, 0, cols)
            for destination_stop in range(nr_stops):
                if sys.version_info[0] >= 3:
                    self.__add_item(all_stops_info[current_stop][1].count(all_stops_info[destination_stop][0]), self.tab2,
                                  i, j + 1, cols)
                else:
                    self.__add_item(all_stops_info[current_stop][1].count(all_stops_info[destination_stop][0]),
                                   self.tab2, i, j + 1, cols)
                j += 1
            rows.append(cols)
            i += 1

    def __create_buses_table(self):
        """
        creates table that displays buses
        :return: None
        """
        i = 0
        rows = []
        cols = []
        self.__add_item('id', self.tab3, i, 0, cols)
        self.__add_item('line', self.tab3, i, 1, cols)
        self.__add_item('route', self.tab3, i, 2, cols)
        self.__add_item('last stop', self.tab3, i, 3, cols)
        self.__add_item('next stop', self.tab3, i, 4, cols)
        self.__add_item('time to next stop', self.tab3, i, 5, cols)
        self.__add_item('passengers inside', self.tab3, i, 6, cols)
        self.__add_item('bus capacity', self.tab3, i, 7, cols)
        rows.append(cols)
        i += 1
        for bus in self.simulation.buses:
            cols = []
            self.__add_item(bus.id, self.tab3, i, 0, cols)
            self.__add_item(bus.line.number, self.tab3, i, 1, cols)
            _route = [stop.name.encode("utf-8") for stop in bus.line.routes[bus.route] if stop.name != "P"]
            self.__add_item(_route, self.tab3, i, 2, cols)
            self.__add_item(bus.current_stop_name, self.tab3, i, 3, cols)
            self.__add_item(bus.next_stop_name, self.tab3, i, 4, cols)
            self.__add_item(bus.time_to_next_stop, self.tab3, i, 5, cols)
            self.__add_item(len(bus.passengers), self.tab3, i, 6, cols)
            self.__add_item(bus.line.bus_capacity, self.tab3, i, 7, cols)
            i += 1
            rows.append(cols)

    def __add_item(self, item, grid, i, j, cols):
        """
        adds single item to grid
        :return: None
        """
        e = tk.Entry(grid)
        e.grid(row=i, column=j, sticky=tk.NSEW)
        e.insert(tk.END, item)
        cols.append(e)

    def run(self):
        """
        mainloop of GUI with timer
        :return: None
        """
        self.root.after(3000, self.__my_mainloop)
        self.root.mainloop()

    def __pause(self):
        """
        reacts to button click
        :return: None
        """
        if self.is_executing:
            self.is_executing = False
            self.button["text"] = "Run"
        else:
            self.is_executing = True
            self.button["text"] = "Pause"
            self.__my_mainloop()

    def __my_mainloop(self):
        """
        causes simulation to refresh and displays result in GUI
        :return: None
        """
        if self.is_executing:
            self.simulation.refresh()
            self.__create_tables()
            self.root.after(3000, self.__my_mainloop)
