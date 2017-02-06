import sys
import tkinter as GUI
from tkinter import ttk

class displayWidget():
    def __init__(self, note):
        self.tab1 =[]
        self.tab2 = []
        self.tab3 = []
        self.pada = []
        self.padb = []
        self.padc = []
        self.note = note

    def create_tabs(self, *args):
        self.tab1 = GUI.Frame(self.note)
        self.tab2 = GUI.Frame(self.note)
        self.tab3 = GUI.Frame(self.note)
        self.pada = GUI.Text(self.tab1, height = 40, width = 150).pack(side = GUI.TOP)
        self.padb = GUI.Text(self.tab2, height = 40, width = 150).pack(side = GUI.TOP)
        self.padc = GUI.Text(self.tab3, height = 40, width = 150).pack(side = GUI.TOP)
        self.buttonb = GUI.Button(self.tab2, text = 'Pause', command = root.destroy).pack(side = GUI.BOTTOM)
        self.buttonc = GUI.Button(self.tab3, text = 'Pause', command = root.destroy).pack(side = GUI.BOTTOM)

        self.note.add(self.tab1, text = "     Lines       ")
        self.note.add(self.tab2, text = "     Stops       ")
        self.note.add(self.tab3, text = "     Buses       ")
        self.note.pack(side = GUI.TOP)



root = GUI.Tk()
note = ttk.Notebook(root)
D = displayWidget(note)

D.create_tabs()

root.resizable(height = False,width = False)
root.mainloop()
exit()








