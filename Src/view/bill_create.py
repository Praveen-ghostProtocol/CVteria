import tkinter as tk

from datetime import datetime
from model.bill import Bill
from view.helper.comp_helper import ComponentHelper
from database.db import Database

class BillCreate():
    def __init__(self, win, bill=Bill):
        print('create bill constructor')
        self.createWidgets(win, bill)

    def createWidgets(self, win, bill=Bill):
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

        self.payment_mode_list = db.payment_mode_get_all()
        payment_mode_arr = []
        payment_mode_arr.append('Please Select')
        for data in self.payment_mode_list:
            payment_mode_arr.append(data.payment_mode_name)

        helper = ComponentHelper()
        self.cust = helper.create_label_options_menu(win, 0,'Customer', cust_arr, self.item_changed)
        self.table = helper.create_label_options_menu(win, 1,'Table', table_arr, self.item_changed)
        self.datetime = helper.create_label_entry(win, 2,'DateTime', datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        self.total_price = helper.create_label_entry(win, 3,'Amount', bill.total_price)        
        self.mode_of_payment = helper.create_label_options_menu(win, 4,'Mode Of Payment', payment_mode_arr, self.item_changed)
                
        self.submit = tk.Button(win, text='Submit', command=lambda:self.bill_create())
        self.submit.grid(row=5, column=1, sticky=tk.N+tk.S+tk.E+tk.W)

    def bill_create(self):
        db = Database()

        bill = Bill()
        for data in self.table_list:
            if data.table_number == self.table.get():
                bill.table_id = data.table_id
        
        for data in self.cust_list:
            if data.customer_name == self.cust.get():
                bill.customer_id = data.customer_id

        for data in self.payment_mode_list:
            if data.payment_mode_name == self.mode_of_payment.get():
                bill.payment_mode_id = data.payment_mode_id

        bill.total_price = self.total_price.get()
        bill.datetime = self.datetime.get()

        db.bill_create(bill)

    def item_changed(self, *args):
        print(self)
