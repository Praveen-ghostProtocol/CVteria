import tkinter as tk

from tkinter import *
from tkinter.ttk import *
  
from model.item import Item
from model.order import Order
from view.helper.comp_helper import ComponentHelper
from view.order_create import OrderCreate
from database.db import Database

class OrderList():
    def __init__(self, win):
        print('order list constructor')
        self.createWidgets(win)

    def createWidgets(self, win):
        top=win.winfo_toplevel()

        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)

        win.rowconfigure(1, weight=1)
        win.columnconfigure(1, weight=1)
                
        win.submit = tk.Button(win, text='Add Order', command=lambda:self.order_create(win))
        win.submit.grid(row=7, column=1, sticky=tk.N+tk.S+tk.E+tk.W,padx=10,pady=10)

        tv = self.CreateUI(win)
        
        db = Database()
        order_list = db.order_get_all()
        for data in order_list:
            self.AddItem(tv, data)

    def order_create(self, win):
        helper = ComponentHelper()
        helper.remove_all_widgets(win)
        win.geometry("950x650")
        cust = Item() #populate this object when opening in edit mode
        cust_create = OrderCreate(win)
                
    def AddItem(self, tv, ord=Order):
        tv.insert("", 'end', iid=None, text=ord.order_id, values=(ord.table_number, ord.create_time, ord.item, ord.qty, ord.price, ord.gst, ord.total_price))
        
    def CreateUI(self, win):
        tv = Treeview(win)
        tv['columns'] = ('Table', 'Date Time', 'Item', 'Qty', 'Price', 'GST', 'Total Price')
        
        tv.heading("#0", text='#', anchor='w')
        tv.column("#0", anchor="w", width=25)

        tv.heading('Table', text='Table')
        tv.column('Table', anchor='center', width=100)

        tv.heading('Date Time', text='Date Time')
        tv.column('Date Time', anchor='center', width=120)

        tv.heading('Item', text='Item')
        tv.column('Item', anchor='center', width=100)

        tv.heading('Qty', text='Qty')
        tv.column('Qty', anchor='center', width=100)
        
        tv.heading('Price', text='Price')
        tv.column('Price', anchor='center', width=100)
        
        tv.heading('GST', text='GST')
        tv.column('GST', anchor='center', width=100)
        
        tv.heading('Total Price', text='Total Price')
        tv.column('Total Price', anchor='center', width=100)

        tv.grid(row=8, column=1, sticky = (N,S,W,E))
        self.treeview = tv
        
        return tv