import tkinter as tk

from tkinter import *
from tkinter.ttk import *
  
from model.item import Item
from model.order import Order
from view.helper.comp_helper import ComponentHelper

from database.db import Database

class OrderCreate():
    i=1
    item = tk.OptionMenu
    table = tk.OptionMenu
    qty = tk.Entry
    price = tk.Label
    gst = tk.Label
    total_price = tk.Label
    description = tk.Label
    spice_lvl = tk.Label
    veg = tk.Label
    category = tk.Label
    item_list = []
    table_list = []
    orders = []
    
    def __init__(self, win):
        print('create order constructor')
        self.item_list = []
        self.table_list = []
        self.orders = []
        self.createWidgets(win)

    def createWidgets(self, win):
        top=win.winfo_toplevel()

        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)

        win.rowconfigure(1, weight=1)
        win.columnconfigure(1, weight=1)

        db = Database()
        self.item_list = db.item_get_all()
        item_arr = []
        item_arr.append('Please Select')
        for data in self.item_list:
            item_arr.append(data.item)
        
        self.table_list = db.table_get_all()
        table_arr = []
        table_arr.append('Please Select')
        for data in self.table_list:
            table_arr.append(data.table_number)
        
        helper = ComponentHelper()
        self.item = helper.create_label_options_menu(win, 0,'Item Name', item_arr, self.item_changed)
        self.table = helper.create_label_options_menu(win, 1,'Table', table_arr, self.table_changed)
        self.qty = helper.create_label_entry(win, 2,'Quantity', 1)
        self.price = helper.create_label_label(win, 3,'Price', 0)
        self.description = helper.create_label_label(win, 4,'Description', '')
        self.spice_lvl = helper.create_label_label(win, 5,'Spice Level', 1)
        self.veg = helper.create_label_label(win, 6,'Veg', 'Yes')
        self.category = helper.create_label_label(win, 7,'Category', 'Main Course')
        self.gst = helper.create_label_label(win, 8,'GST', '18')
        self.total_price = helper.create_label_label(win, 9,'Total Price', 1)
                
        win.submit = tk.Button(win, text='Add Item', command=lambda:self.AddItem(tv))
        win.submit.grid(row=10, column=1, sticky=tk.N+tk.S+tk.E+tk.W,padx=10,pady=10)

        tv = self.CreateUI(win, 11)
        
        win.submit = tk.Button(win, text='Submit Order', command=lambda:self.order_create())
        win.submit.grid(row=12, column=1, sticky=tk.N+tk.S+tk.E+tk.W,padx=10,pady=10)

    def item_changed(self, *args):
        print(self)
        self.price.config(text=0)
        self.description.config(text='')
        self.spice_lvl.config(text=1)
        self.veg.config(text='Yes')
        self.category.config(text='')
        self.gst.config(text=18)

        for data in self.item_list:
            if data.item == args[0]:                
                self.price.config(text=data.price)
                self.description.config(text=data.description)
                self.spice_lvl.config(text=data.spice_level)
                self.veg.config(text=data.veg)
                self.category.config(text=data.category)
                #self.gst.config(text=data.gst)

    def table_changed(self, *args):
        print(self)
        self.output_label['text'] = f'You selected: {self.option_var.get()}'

    def order_create(self):
        db = Database()

        for ord in self.orders:            
            order = Order()
            order.item_id = ord.item_id
            order.table_number = ord.table_number
            order.qty = ord.qty
            order.price = ord.price
            order.gst = ord.gst
            order.total_price = ord.total_price

            db.order_create(order)

    def AddItem(self, tv):
        order = Order()

        for data in self.item_list:
            if data.item == self.item.get():
                order.item_id = data.item_id
                order.item = self.item.get()

        for data in self.table_list:
            if data.table_number == self.table.get():
                order.table_number = data.table_number
                order.table_id = data.table_id
        
        order.qty = self.qty.get()
        order.price = self.price.cget("text")
        order.gst = self.gst.cget("text")
        order.total_price = float(order.qty) * float(order.price) * (1 + float(order.gst/100))
        
        self.orders.append(order)
        
        tv.insert("", 'end', iid=None, text=self.i, values=(order.item,order.qty, order.price, order.gst, order.total_price))
        self.i = self.i + 1
        
    def CreateUI(self, win, row):
        tv = Treeview(win)
        tv['columns'] = ('Item', 'Qty', 'Price', 'GST', 'Total Price')
        
        tv.heading("#0", text='S No', anchor='w')
        tv.column("#0", anchor="w", width=25)

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

        tv.grid(row=row, column=1, sticky = (N,S,W,E))
        self.treeview = tv
        
        return tv