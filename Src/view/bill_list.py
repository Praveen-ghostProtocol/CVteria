import tkinter as tk

from tkinter import *
from tkinter.ttk import *
  
from model.bill import Bill
from view.helper.comp_helper import ComponentHelper
from view.bill_create import BillCreate
from database.db import Database
from view.event import Event

class BillList():
    tv = Treeview
    win = object
    def __init__(self, win):
        print('bill list constructor')
        self.bil_create = BillCreate()
        self.bil_create.AddSubscribersForViewUpdatedEvent(self.bill_created)
        self.OnViewUpdated = Event()
        self.win = win
         
    def ViewUpdated(self):
        self.OnViewUpdated()
         
    def AddSubscribersForViewUpdatedEvent(self,objMethod):
        self.OnViewUpdated += objMethod
         
    def RemoveSubscribersForViewUpdatedEvent(self,objMethod):
        self.OnViewUpdated -= objMethod

    def bill_created(self):
        self.ViewUpdated()
        print('order created')

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
        self.bil_create.createWidgets(win)
                
    def AddItem(self, tv, bill=Bill):
        tv.insert("", 'end', iid=None, text=bill.bill_id, values=(bill.customer, bill.table_number, bill.total_amount, bill.mode_of_payment, bill.datetime))
        
    def edit(self):
        print("Edit", self.popup.selection)

        helper = ComponentHelper()
        helper.remove_all_widgets(self.win)
        self.win.geometry("800x700")
        row = self.popup.row
        id = self.tv.item(row)['text']
        self.bill_create.createWidgets(self.win, id)
        
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
        
        self.tv['columns'] = ( 'Customer', 'Table Number', 'Total Amount', 'Mode Of Payment', 'DateTime')
        
        self.tv.heading("#0", text='#', anchor='w')
        self.tv.column("#0", anchor="w", width=35)

        self.tv.heading('Customer', text='Customer')
        self.tv.column('Customer', anchor='center', width=100)

        self.tv.heading('Table Number', text='Table Number')
        self.tv.column('Table Number', anchor='center', width=100)

        self.tv.heading('Total Amount', text='Total Amount')
        self.tv.column('Total Amount', anchor='center', width=100)
        
        self.tv.heading('Mode Of Payment', text='Mode Of Payment')
        self.tv.column('Mode Of Payment', anchor='center', width=100)

        self.tv.heading('DateTime', text='DateTime')
        self.tv.column('DateTime', anchor='center', width=150)
        
        self.tv.grid(row=1, column=1, sticky = (N,S,W,E))
        self.treeview = self.tv
        
        return self.tv