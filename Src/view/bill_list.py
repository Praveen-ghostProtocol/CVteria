import tkinter as tk

from tkinter import *
from tkinter.ttk import *
  
from model.bill import Bill
from view.helper.comp_helper import ComponentHelper
from view.bill_create import BillCreate
from database.db import Database

class BillList():
    def __init__(self, win):
        print('bill list constructor')
        self.createWidgets(win)

    def createWidgets(self, win):
        top=win.winfo_toplevel()

        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)

        win.rowconfigure(1, weight=1)
        win.columnconfigure(1, weight=1)
                
        win.submit = tk.Button(win, text='Add Bill', command=lambda:self.bill_create(win))
        win.submit.grid(row=0, column=1, sticky=tk.N+tk.S+tk.E+tk.W,padx=10,pady=10)

        tv = self.CreateUI(win)
        
        db = Database()
        reserv_list = db.bill_get_all()
        for data in reserv_list:
            self.AddItem(tv, data)

    def bill_create(self, win):
        helper = ComponentHelper()
        helper.remove_all_widgets(win)
        win.geometry("350x200")
        bill = Bill() #populate this object when opening in edit mode
        reserv_create = BillCreate(win, bill)
                
    def AddItem(self, tv, bill=Bill):
        tv.insert("", 'end', iid=None, text=bill.bill_id, values=(bill.customer, bill.table_number, bill.total_price, bill.mode_of_payment, bill.datetime))
        
    def CreateUI(self, win):
        tv = Treeview(win)
        tv['columns'] = ( 'Customer', 'Table Number', 'Total Price', 'Mode Of Payment', 'DateTime')
        
        tv.heading("#0", text='#', anchor='w')
        tv.column("#0", anchor="w", width=35)

        tv.heading('Customer', text='Customer')
        tv.column('Customer', anchor='center', width=100)

        tv.heading('Table Number', text='Table Number')
        tv.column('Table Number', anchor='center', width=100)

        tv.heading('Total Price', text='Total Price')
        tv.column('Total Price', anchor='center', width=100)
        
        tv.heading('Mode Of Payment', text='Mode Of Payment')
        tv.column('Mode Of Payment', anchor='center', width=100)

        tv.heading('DateTime', text='DateTime')
        tv.column('DateTime', anchor='center', width=150)
        
        tv.grid(row=1, column=1, sticky = (N,S,W,E))
        self.treeview = tv
        
        return tv