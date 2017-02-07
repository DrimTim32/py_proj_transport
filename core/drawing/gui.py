import sys
import tkinter as tk
from tkinter import ttk
import collections

class displayWidget():
    def __init__(self, note, parent, simulation):
        self.tab1 = []
        self.tab2 = []
        self.tab3 = []
        self.note = note
        self.root = parent
        self.simulation = simulation

    def create_tabs(self, *args):

        self.tab1 = tk.Frame(self.note)
        self.tab2 = tk.Frame(self.note)
        self.tab3 = tk.Frame(self.note)
        self.buttonb = tk.Button(self.root, text = 'Pause', command = self.root.destroy).pack(side = tk.BOTTOM)

        self.note.add(self.tab1, text = "     Lines       ")
        self.note.add(self.tab2, text = "     Stops       ")
        self.note.add(self.tab3, text = "     Buses       ")
        self.note.pack(side = tk.TOP)
        # self.button = tk.Button(self.note, text='Pause', command=self.root.destroy).pack(side=tk.BOTTOM)


    def create_tables(self):
        self.create_lines_table()
        self.create_stops_table()
        self.create_buses_table()

    def create_lines_table(self):
        i = 0
        rows = []
        cols = []
        self.add_item('number', self.tab1, i, 0, cols)
        self.add_item('last stop', self.tab1, i, 1, cols)
        self.add_item('route', self.tab1, i, 2, cols)
        self.add_item('frequency', self.tab1, i, 3, cols)
        self.add_item('bus capacity', self.tab1, i, 4, cols)
        rows.append(cols)
        i += 1
        for line in self.simulation.lines:
            cols = []
            self.add_item(line.number, self.tab1, i, 0, cols)
            self.add_item(line.last_stop_name(0), self.tab1, i, 1, cols)
            r = [stop.name for stop in line.routes[0] if stop.name != "P"]
            self.add_item(r, self.tab1, i, 2, cols)
            self.add_item(line.frequencies[0], self.tab1, i, 3, cols)
            self.add_item(line.bus_capacity, self.tab1, i, 4, cols)
            i += 1
            cols = []
            self.add_item(line.number, self.tab1, i, 0, cols)
            self.add_item(line.last_stop_name(1), self.tab1, i, 1, cols)
            r = [stop.name for stop in line.routes[1] if stop.name != "P"]
            self.add_item(r, self.tab1, i, 2, cols)
            self.add_item(line.frequencies[1], self.tab1, i, 3, cols)
            self.add_item(line.bus_capacity, self.tab1, i, 4, cols)
            i += 1
            rows.append(cols)

    def create_stops_table(self):
        all_stops_info = collections.OrderedDict(sorted(self.simulation.stops.items()))
        i = 0
        rows = []
        cols = []
        self.add_item('name', self.tab2, i, 0, cols)
        j = 0
        for key in all_stops_info.keys():
            self.add_item(('to ' + key), self.tab2, i, j+1, cols)
            j += 1
        rows.append(cols)
        i += 1

        for current_stop in all_stops_info:
            cols = []
            j = 0
            self.add_item(current_stop, self.tab2, i, 0, cols)
            for destination_stop in all_stops_info.keys():
                self.add_item(all_stops_info[current_stop].count(destination_stop), self.tab2, i, j + 1, cols)
                j += 1
            rows.append(cols)
            i += 1

    def create_buses_table(self):
        i = 0
        rows = []
        cols = []
        self.add_item('id', self.tab3, i, 0, cols)
        self.add_item('line', self.tab3, i, 1, cols)
        self.add_item('route', self.tab3, i, 2, cols)
        self.add_item('last stop', self.tab3, i, 3, cols)
        self.add_item('next stop', self.tab3, i, 4, cols)
        self.add_item('time to next stop', self.tab3, i, 5, cols)
        self.add_item('passengers inside', self.tab3, i, 6, cols)
        self.add_item('bus capacity', self.tab3, i, 7, cols)
        rows.append(cols)
        i += 1
        for bus in self.simulation.buses:
            cols = []
            self.add_item(bus.id, self.tab3, i, 0, cols)
            self.add_item(bus.line.number, self.tab3, i, 1, cols)
            r = [stop.name for stop in bus.line.routes[bus.route] if stop.name != "P"]
            self.add_item(r, self.tab3, i, 2, cols)
            self.add_item(bus.current_stop_name, self.tab3, i, 3, cols)
            self.add_item(bus.next_stop_name, self.tab3, i, 4, cols)
            self.add_item(bus.time_to_next_stop, self.tab3, i, 5, cols)
            self.add_item(len(bus.passengers), self.tab3, i, 6, cols)
            self.add_item(bus.line.bus_capacity, self.tab3, i, 7, cols)
            i += 1
            rows.append(cols)

    def add_item(self, item, grid, i, j, cols):
        e = tk.Entry(grid)
        e.grid(row=i, column=j, sticky=tk.NSEW)
        e.insert(tk.END, item)
        cols.append(e)


class GUI():
    def __init__(self, simulation):
        self.simulation = simulation
        self.root = tk.Tk()
        self.note = ttk.Notebook(self.root)
        self.D = displayWidget(self.note, self.root, self.simulation)
        self.D.create_tabs()
        self.D.create_tables()
        self.root.resizable(height=False, width=False)
        self.go = True


    def run(self):
        self.root.after(1000, self.my_mainloop)
        self.root.mainloop()



    def my_mainloop(self):
        self.simulation.refresh()
        self.D.create_tables()
        self.root.after(3000, self.my_mainloop)

