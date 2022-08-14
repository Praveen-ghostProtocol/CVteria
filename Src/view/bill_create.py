import tkinter as tk
from tkinter import messagebox

from datetime import datetime
from model.bill import Bill
from view.helper.comp_helper import ComponentHelper
from database.db import Database
from view.event import Event

class BillCreate():
    cafe_order_header_id=0
    def __init__(self):
        print('create bill constructor')
        self.OnViewUpdated = Event()

    def ViewUpdated(self):
        self.OnViewUpdated()
         
    def AddSubscribersForViewUpdatedEvent(self,objMethod):
        self.OnViewUpdated += objMethod
         
    def RemoveSubscribersForViewUpdatedEvent(self,objMethod):
        self.OnViewUpdated -= objMethod

    def createWidgets(self, win, id=0):
        top=win.winfo_toplevel()

        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)

        win.rowconfigure(1, weight=1)
        win.columnconfigure(1, weight=1)

        db = Database()
        self.order_header_list = db.order_header_get_upaid()
        order_header_arr = []
        order_header_arr.append('Please Select')
        for data in self.order_header_list:
            order_header_arr.append(str(data.order_header_id) + "|" + str(data.table_number) + "|" + str(data.total_amount) + "|" + str(data.create_time))

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

        self.payment_mode_list = db.payment_mode_get_all()
        payment_mode_arr = []
        payment_mode_arr.append('Please Select')
        for data in self.payment_mode_list:
            payment_mode_arr.append(data.payment_mode_name)

        helper = ComponentHelper()
        self.order = helper.create_label_options_menu(win, 0,'Order', order_header_arr, self.order_changed)
        
        self.table = helper.create_label_label(win, 1,'Table', 0)
        self.total_amount = helper.create_label_label(win, 2,'Total Amount', 0)
        self.datetime = helper.create_label_label(win, 3, 'DateTime', 0)
        
        self.cust = helper.create_label_options_menu(win, 4,'Customer', cust_arr, self.item_changed)
        self.mode_of_payment = helper.create_label_options_menu(win, 5,'Mode Of Payment', payment_mode_arr, self.item_changed)
                
        self.submit = tk.Button(win, text='Submit', command=lambda:self.bill_create())
        self.submit.grid(row=6, column=0, sticky=tk.N+tk.S+tk.E+tk.W)

        cancel = tk.Button(win, text='Cancel', command=lambda:self.bill_cancel())
        cancel.grid(row=6, column=1, sticky=tk.N+tk.S+tk.E+tk.W)

    def bill_cancel(self, *args):
        self.ViewUpdated()
        
    def order_changed(self, *args):
        args_arr = args[0].split('|')
        self.cafe_order_header_id = args_arr[0]
        self.table.config(text=args_arr[1])
        self.total_amount.config(text=args_arr[2])
        self.datetime.config(text=args_arr[3])
        print('data', self)

    def item_changed(self, *args):
        print(self)

    def bill_create(self):
        if self.cust[0].get() == "Please Select":
            messagebox.showerror('Failure!', 'Please Select Customer!')
            return
        if self.mode_of_payment[0].get() == "Please Select":
            messagebox.showerror('Failure!', 'Please Select Mode of Payment!')
            return
        
        db = Database()      
        
        bill = Bill()        
        bill.cafe_order_header_id = self.cafe_order_header_id
        for data in self.cust_list:
            if data.customer_name == self.cust[0].get():
                bill.customer_id = data.customer_id

        for data in self.payment_mode_list:
            if data.payment_mode_name == self.mode_of_payment[0].get():
                bill.payment_mode_id = data.payment_mode_id

        bill.datetime = self.datetime.cget("text")

        db.bill_create(bill)        
        self.ViewUpdated()
        messagebox.showinfo('Success!', 'Bill Created Successfully')

