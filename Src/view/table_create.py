import tkinter as tk

from model.table import Table
from view.helper.comp_helper import ComponentHelper

class TableCreate():
    def __init__(self, win, tbl=Table):
        print('create customer constructor')
        self.createWidgets(win, tbl)

    def createWidgets(self, win, tbl=Table):
        top=win.winfo_toplevel()

        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)

        win.rowconfigure(1, weight=1)
        win.columnconfigure(1, weight=1)

        helper = ComponentHelper()
        helper.create_label_entry(win, 0,'Table Number', tbl.table_number)
        helper.create_label_entry(win, 1,'Number of Seats', tbl.number_of_seats)
        helper.create_label_entry(win, 2,'Location', tbl.location)
        
        self.submit = tk.Button(win, text='Submit', command=win.quit)
        self.submit.grid(row=6, column=1, sticky=tk.N+tk.S+tk.E+tk.W)
