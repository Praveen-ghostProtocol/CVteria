import tkinter as tk

from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
from model import order_detail
  
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
    toolbar = object
    
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

    def createWidgets(self, win, toolbar):
        top=win.winfo_toplevel()
        self.toolbar = toolbar
        
        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)

        win.rowconfigure(1, weight=1)
        win.columnconfigure(1, weight=1)

        helper = ComponentHelper()
        win.frame = helper.add_background(win, "./images/order_list.gif")
                
        win.submit = tk.Button(win.frame, text='Add Order', command=lambda:self.order_create(win))
        win.submit.grid(row=2, column=0, sticky=tk.N+tk.S+tk.E+tk.W,padx=10,pady=10)

        help = tk.Label(win.frame, text='*Right click to Edit or Delete', background='#CC8066', foreground='white')
        help.grid(row=3, column=0, sticky=tk.W, pady=5)

        tv = self.CreateUI(win.frame)
        
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
        self.win.geometry("1280x785")
        self.toolbar(win)
        self.ord_create.createWidgets(win)
                
    def AddItem(self, tv, ord=OrderHeader):
        tv.insert("", 'end', iid=None, text=ord.order_header_id, values=(ord.table_number, ord.create_time, ord.total_amount))
        
    def edit(self):
        print("Edit", self.popup.selection)
        row = self.popup.row
        id = self.tv.item(row)['text']
        if(id == '' or int(id) == 0):
            messagebox.showerror('Failure!', 'Please select a Row!')
            return
        
        helper = ComponentHelper()
        helper.remove_all_widgets(self.win)
        self.win.geometry("1280x785")
        self.toolbar(self.win)
        self.ord_create.createWidgets(self.win, id)
        
    def delete(self):        
        row = self.popup.row
        id = self.tv.item(row)['text']
        if(id == '' or int(id) == 0):
            messagebox.showerror('Failure!', 'Please select a Row!')
            return

        db = Database()
        bill_exist = db.bill_get_buy_order_header_id(id)
        
        
        try:
            if len(bill_exist) > 0:
                messagebox.showerror('Failure!',"Cannot delete order, as there is an existing bill for it!")
                return
            else:
                db.order_delete(id)
            selected_item = self.tv.selection()[0]    
            self.tv.delete(selected_item)
        except:
            messagebox.showerror('Failure!', 'Please select an Item before Deleting!')
            return
        
        messagebox.showinfo('Success!', 'Order deleted Successfully')
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
        self.tv = Treeview(win, height=22)
        
        #Create menu
        self.popup = tk.Menu(win, tearoff=0)
        self.popup.add_command(label="Edit", command=self.edit)
        self.popup.add_separator()
        self.popup.add_command(label="Delete", command=self.delete)        

        self.tv.bind("<Button-3>", self.do_popup)        
        
        self.tv['columns'] = ('Table', 'Date Time', 'Total Amount')
        
        self.tv.heading("#0", text='#', anchor='w')
        self.tv.column("#0", anchor="w", width=50)

        self.tv.heading('Table', text='Table')
        self.tv.column('Table', anchor='center', width=300)

        self.tv.heading('Date Time', text='Date Time')
        self.tv.column('Date Time', anchor='center', width=150)

        self.tv.heading('Total Amount', text='Total Amount')
        self.tv.column('Total Amount', anchor='center', width=150)

        self.tv.grid(row=4, column=0, sticky = (N,S,W,E))
        self.treeview = self.tv
        
        return self.tv