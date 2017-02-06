import sys
import tkinter as tk
from tkinter import ttk

class displayWidget():
    def __init__(self, note, parent, simulation):
        self.tab1 =[]
        self.tab2 = []
        self.tab3 = []
        self.note = note
        self.root = parent
        self.simulation = simulation

    def create_tabs(self, *args):
        self.tab1 = tk.Frame(self.note)
        self.tab2 = tk.Frame(self.note)
        self.tab3 = tk.Frame(self.note)
        self.buttonb = tk.Button(self.tab2, text = 'Pause', command = self.root.destroy).pack(side = tk.BOTTOM)
        self.buttonc = tk.Button(self.tab3, text = 'Pause', command = self.root.destroy).pack(side = tk.BOTTOM)

        self.note.add(self.tab1, text = "     Lines       ")
        self.note.add(self.tab2, text = "     Stops       ")
        self.note.add(self.tab3, text = "     Buses       ")
        self.note.pack(side = tk.TOP)

    def create_tables(self):
        rows = []
        for i in range(5):
            cols = []
            for j in range(5):
                e = tk.Entry(self.tab1)
                e.grid(row=i, column=j, sticky=tk.NSEW)
                e.insert(tk.END, '%d.%d' % (i, j))
                cols.append(e)
            rows.append(cols)

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
            self.add_item(line.routes[0], self.tab1, i, 2, cols)
            self.add_item(line.frequencies[0], self.tab1, i, 3, cols)
            self.add_item(line.bus_capacity, self.tab1, i, 4, cols)
            i += 1
            cols = []
            self.add_item(line.number, self.tab1, i, 0, cols)
            self.add_item(line.last_stop_name(1), self.tab1, i, 1, cols)
            self.add_item(line.routes[1], self.tab1, i, 2, cols)
            self.add_item(line.frequencies[1], self.tab1, i, 3, cols)
            self.add_item(line.bus_capacity, self.tab1, i, 4, cols)
            i += 1
            rows.append(cols)

    def add_item(self, item, grid, i, j, cols):
        e = tk.Entry(grid)
        e.grid(row=i, column=j, sticky=tk.NSEW)
        e.insert(tk.END, item)
        cols.append(e)
        # return cols


class GUI():
    def __init__(self, simulation):
        self.simulation = simulation
        self.root = tk.Tk()
        self.note = ttk.Notebook(self.root)
        self.D = displayWidget(self.note, self.root, self.simulation)
        self.D.create_tabs()
        self.D.create_lines_table()
        self.root.resizable(height=False, width=False)


    def run(self):
        self.root.mainloop()



