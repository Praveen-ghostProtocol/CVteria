import tkinter as tk

from model.table_reservation import TableReservation
from view.helper.comp_helper import ComponentHelper
from database.db import Database

class TableReservationCreate():
    customer = tk.OptionMenu
    table = tk.OptionMenu
    datetime = ''
    pax = 2
    
    def __init__(self, win, tbl=TableReservation):
        print('create table reservation constructor')
        self.createWidgets(win, tbl)

    def createWidgets(self, win, tbl=TableReservation):
        top=win.winfo_toplevel()

        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)

        win.rowconfigure(1, weight=1)
        win.columnconfigure(1, weight=1)

        db = Database()
        self.table_list = db.table_get_all()
        table_arr = []
        table_arr.append('Please Select')
        for data in self.table_list:
            table_arr.append(data.table_number)

        self.cust_list = db.customer_get_all()
        cust_arr = []
        cust_arr.append('Please Select')
        for data in self.cust_list:
            cust_arr.append(data.customer_name)

        helper = ComponentHelper()
        self.customer = helper.create_label_options_menu(win, 0,'Customer', cust_arr, self.item_changed)
        self.table = helper.create_label_options_menu(win, 1,'Table', table_arr, self.item_changed)
        helper.create_label_label(win, 2,'Number of Seats', 2)
        helper.create_label_label(win, 3,'Location', tbl.location)
        self.datetime = helper.create_label_entry(win, 4,'DateTime', '')
        self.pax = helper.create_label_entry(win, 5,'Pax', '')
        
        self.submit = tk.Button(win, text='Submit', command=lambda:self.table_reservation_create())
        self.submit.grid(row=6, column=1, sticky=tk.N+tk.S+tk.E+tk.W)

    def table_reservation_create(self):
        db = Database()

        reserv = TableReservation()
        for data in self.table_list:
            if data.table_number == self.table.get():
                reserv.table_id = data.table_id
        
        for data in self.cust_list:
            if data.customer_name == self.customer.get():
                reserv.customer_id = data.customer_id

        reserv.pax = self.pax.get()
        reserv.datetime = self.datetime.get()

        db.table_reservation_create(reserv)
        
    def item_changed(self, *args):
        print(self)
