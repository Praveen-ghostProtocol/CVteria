import tkinter as tk
from tkinter import messagebox

from datetime import datetime
from model.bill import Bill
from view.helper.comp_helper import ComponentHelper
from database.db import Database
from view.event import Event

class BillCreate():
    
    cafe_order_header_id=0
    id=0
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
        self.id = id
        top=win.winfo_toplevel()

        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)

        win.rowconfigure(1, weight=1)
        win.columnconfigure(1, weight=1)

        helper = ComponentHelper()
        win.frame = helper.add_background(win, "./images/bill_add_del2.gif")

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

        bill = Bill()
        db = Database()
        if(id > 0):            
            list = db.bill_get_by_id(id)
            for data in list:
                bill.bill_id = data.bill_id
                bill.cafe_order_header_id=data.cafe_order_header_id
                bill.payment_mode_id = data.payment_mode_id
                bill.mode_of_payment = data.mode_of_payment
                bill.datetime = data.datetime
                bill.customer_id = data.customer_id
                bill.customer = data.customer
                bill.table_id = data.table_id
                bill.table_number = data.table_number
                bill.total_amount=data.total_amount
                bill.discount = data.discount
                bill.final_amount = data.final_amount
            order_txt = ''
            for data in self.order_header_list:
                if(data.cafe_order_header_id == bill.cafe_order_header_id):
                    order_txt = str(data.order_header_id) + "|" + str(data.table_number) + "|" + str(data.total_amount) + "|" + str(data.create_time)

                
        helper = ComponentHelper()
        if(self.id > 0):
            self.order = helper.create_label_options_menu(win.frame, 0,'Order', order_header_arr, self.order_changed, order_txt)
            self.cust = helper.create_label_options_menu(win.frame, 4,'Customer', cust_arr, self.customer_changed, bill.customer)
            self.mode_of_payment = helper.create_label_options_menu(win.frame, 5,'Mode Of Payment', payment_mode_arr, self.item_changed, bill.mode_of_payment)
        else:
            self.order = helper.create_label_options_menu(win.frame, 0,'Order', order_header_arr, self.order_changed)
            self.cust = helper.create_label_options_menu(win.frame, 4,'Customer', cust_arr, self.customer_changed)
            self.mode_of_payment = helper.create_label_options_menu(win.frame, 7,'Mode Of Payment', payment_mode_arr, self.item_changed)
        
        self.table = helper.create_label_label(win.frame, 1,'Table', bill.table_number)
        self.total_amount = helper.create_label_label(win.frame, 2,'Total Amount', bill.total_amount)        
        self.datetime = helper.create_label_label(win.frame, 3, 'DateTime', bill.datetime)
        self.total_amount = helper.create_label_entry(win.frame, 5,'Discount', bill.discount)
        self.total_amount = helper.create_label_label(win.frame, 6,'Final Amount', bill.final_amount)
                
        cancel = tk.Button(win.frame, text='Cancel', command=lambda:self.bill_cancel())
        cancel.grid(row=7, column=0, sticky=tk.N+tk.S+tk.E+tk.W)

        self.submit = tk.Button(win.frame, text='Submit', command=lambda:self.bill_create())
        self.submit.grid(row=7, column=1, sticky=tk.N+tk.S+tk.E+tk.W)

        if(self.id > 0):
            self.order[1].configure(state="disable")

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
        
    def customer_changed(self, *args):
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

        if(self.id > 0):
            bill.bill_id = self.id
            db.bill_update(bill)        
        else:
            db.bill_create(bill)        
            
        self.ViewUpdated()
        messagebox.showinfo('Success!', 'Bill Created Successfully')

