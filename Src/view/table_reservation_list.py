import tkinter as tk

from tkinter import *
from tkinter.ttk import *
  
from model.customer import Customer
from model.table_reservation import TableReservation
from view.helper.comp_helper import ComponentHelper
from view.table_reservation_create import TableReservationCreate
from database.db import Database

class TableReservationList():
    def __init__(self, win):
        print('table list constructor')
        self.createWidgets(win)

    def createWidgets(self, win):
        top=win.winfo_toplevel()

        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)

        win.rowconfigure(1, weight=1)
        win.columnconfigure(1, weight=1)
                
        win.submit = tk.Button(win, text='Add Table Reservation', command=lambda:self.table_reservation_create(win))
        win.submit.grid(row=7, column=1, sticky=tk.N+tk.S+tk.E+tk.W,padx=10,pady=10)

        tv = self.CreateUI(win)
        db = Database()
        reserv_list = db.table_reservation_get_all()
        for data in reserv_list:
            self.AddItem(tv, data)

    def table_reservation_create(self, win):
        helper = ComponentHelper()
        helper.remove_all_widgets(win)
        win.geometry("550x200")
        reserv = TableReservation() #populate this object when opening in edit mode
        reserv_create = TableReservationCreate(win, reserv)
                
    def AddItem(self, tv, reserv=TableReservation):
        tv.insert("", 'end', iid=None, text=reserv.reservation_id, values=(reserv.table_number, reserv.pax, reserv.datetime, reserv.customer))
        
    def CreateUI(self, win):
        tv = Treeview(win)
        tv['columns'] = ('Table Number', 'Pax', 'DateTime', 'Customer')
        
        tv.heading("#0", text='#', anchor='w')
        tv.column("#0", anchor="w", width=25)

        tv.heading('Table Number', text='Table Number')
        tv.column('Table Number', anchor='center', width=100)

        tv.heading('Pax', text='Pax')
        tv.column('Pax', anchor='center', width=100)
        
        tv.heading('DateTime', text='DateTime')
        tv.column('DateTime', anchor='center', width=150)
        
        tv.heading('Customer', text='Customer')
        tv.column('Customer', anchor='center', width=100)

        tv.grid(row=8, column=1, sticky = (N,S,W,E))
        self.treeview = tv
        
        return tv