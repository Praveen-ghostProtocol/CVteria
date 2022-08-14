import tkinter as tk

from tkinter import *
from tkinter.ttk import *
  
from model.item import Item
from model.order_header import OrderHeader

from view.helper.comp_helper import ComponentHelper
from view.order_create import OrderCreate
from view.view import View
from view.event import Event

from database.db import Database

class OrderList():
    i=1
    tv = Treeview
    win = object
    
    def __init__(self, win):
        print('order list constructor')
        self.ord_create = OrderCreate()
        self.ord_create.AddSubscribersForViewUpdatedEvent(self.order_created)
        self.OnViewUpdated = Event()
        self.win = win
         
    def ViewUpdated(self):
        self.OnViewUpdated()
         
    def AddSubscribersForViewUpdatedEvent(self,objMethod):
        self.OnViewUpdated += objMethod
         
    def RemoveSubscribersForViewUpdatedEvent(self,objMethod):
        self.OnViewUpdated -= objMethod

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
        order_list = db.order_header_get_all()
        for data in order_list:
            self.AddItem(tv, data)

    def order_created(self):
        self.ViewUpdated()
        print('order created')

    def order_create(self, win):
        helper = ComponentHelper()
        helper.remove_all_widgets(win)
        win.geometry("800x700")
        self.ord_create.createWidgets(win)
                
    def AddItem(self, tv, ord=OrderHeader):
        tv.insert("", 'end', iid=None, text=ord.order_header_id, values=(ord.table_number, ord.create_time, ord.total_amount))
        
    def edit(self):
        print("Edit", self.popup.selection)

        helper = ComponentHelper()
        helper.remove_all_widgets(self.win)
        self.win.geometry("800x700")
        row = self.popup.row
        order_header_id = self.tv.item(row)['text']
        self.ord_create.createWidgets(self.win, order_header_id)
        
    def delete(self):
        print("Delete", self.popup.selection)

    def do_popup(self, event):
        # display the popup menu
        try:
            self.popup.selection = self.treeview.set(self.treeview.identify_row(event.y))
            self.popup.row = self.treeview.identify_row(event.y)
            self.popup.post(event.x_root, event.y_root)
        finally:
            # make sure to release the grab (Tk 8.0a1 only)
            self.popup.grab_release()    

    def CreateUI(self, win):
        self.tv = Treeview(win)
        
        #Create menu
        self.popup = tk.Menu(win, tearoff=0)
        self.popup.add_command(label="Edit", command=self.edit)
        self.popup.add_separator()
        self.popup.add_command(label="Delete", command=self.delete)        

        self.tv.bind("<Button-3>", self.do_popup)        
        
        self.tv['columns'] = ('Table', 'Date Time', 'Total Amount')
        
        self.tv.heading("#0", text='#', anchor='w')
        self.tv.column("#0", anchor="w", width=25)

        self.tv.heading('Table', text='Table')
        self.tv.column('Table', anchor='center', width=100)

        self.tv.heading('Date Time', text='Date Time')
        self.tv.column('Date Time', anchor='center', width=120)

        self.tv.heading('Total Amount', text='Total Amount')
        self.tv.column('Total Amount', anchor='center', width=100)

        self.tv.grid(row=8, column=1, sticky = (N,S,W,E))
        self.treeview = self.tv
        
        return self.tv