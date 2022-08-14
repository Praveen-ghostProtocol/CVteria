import tkinter as tk
from tkinter import messagebox

from tkinter import *
from tkinter.ttk import *
  
from model.customer import Customer
from view.helper.comp_helper import ComponentHelper
from view.customer_create import CustomerCreate
from view.event import Event
from database.db import Database

class CustomerList():
    tv = Treeview
    win = object

    def __init__(self, win):
        print('customer list constructor')
        self.win = win
        self.cust_create = CustomerCreate(win)
        self.cust_create.AddSubscribersForViewUpdatedEvent(self.cust_create_event)
        self.OnViewUpdated = Event()

    def ViewUpdated(self):
        self.OnViewUpdated()
         
    def AddSubscribersForViewUpdatedEvent(self,objMethod):
        self.OnViewUpdated += objMethod
         
    def RemoveSubscribersForViewUpdatedEvent(self,objMethod):
        self.OnViewUpdated -= objMethod

    def cust_create_event(self):
        self.ViewUpdated()
        print('customer created')

    def createWidgets(self, win):
        top=win.winfo_toplevel()

        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)

        win.rowconfigure(1, weight=1)
        win.columnconfigure(1, weight=1)
                
        win.submit = tk.Button(win, text='Add Customer', command=lambda:self.customer_create(win))
        win.submit.grid(row=7, column=1, sticky=tk.N+tk.S+tk.E+tk.W,padx=10,pady=10)

        tv = self.CreateUI(win)
        db = Database()
        cust_list = db.customer_get_all()
        for data in cust_list:
            self.AddItem(tv, data)

    def customer_create(self, win):
        helper = ComponentHelper()
        helper.remove_all_widgets(win)
        win.geometry("450x200")
        #cust = Customer() #populate this object when opening in edit mode
        self.cust_create.createWidgets(win)

    def edit(self):
        print("Edit", self.popup.selection)

        helper = ComponentHelper()
        helper.remove_all_widgets(self.win)
        self.win.geometry("400x200")
        row = self.popup.row
        cust_id = self.tv.item(row)['text']
        self.cust_create.createWidgets(self.win, cust_id)
        
    def delete(self):        
        row = self.popup.row
        cust_id = self.tv.item(row)['text']
        db = Database()
        db.customer_delete(cust_id)
        
        try:
            selected_item = self.tv.selection()[0]    
            self.tv.delete(selected_item)
        except:
            messagebox.showerror('Failure!', 'Please select an Item before Deleting!')
            return
        
        messagebox.showinfo('Success!', 'Customer deleted Successfully')
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
                
    def AddItem(self, tv, cust):
        tv.insert("", 'end', iid=None, text=cust.customer_id, values=(cust.customer_name, cust.phone_number, cust.gender, cust.email_id, cust.DOB, cust.anniversary_date))
        
    def CreateUI(self, win):
        self.tv = Treeview(win)

        #Create menu
        self.popup = tk.Menu(win, tearoff=0)
        self.popup.add_command(label="Edit", command=self.edit)
        self.popup.add_separator()
        self.popup.add_command(label="Delete", command=self.delete)        

        self.tv.bind("<Button-3>", self.do_popup)        

        self.tv['columns'] = ('Customer Name', 'Phone Number', 'Gender', 'Email Id', 'DOB', 'Anniversary Date')
        
        self.tv.heading("#0", text='#', anchor='w')
        self.tv.column("#0", anchor="w", width=25)

        self.tv.heading('Customer Name', text='Customer Name')
        self.tv.column('Customer Name', anchor='center', width=100)

        self.tv.heading('Phone Number', text='Phone Number')
        self.tv.column('Phone Number', anchor='center', width=100)
        
        self.tv.heading('Gender', text='Gender')
        self.tv.column('Gender', anchor='center', width=100)
        
        self.tv.heading('Email Id', text='Email Id')
        self.tv.column('Email Id', anchor='center', width=100)
        
        self.tv.heading('DOB', text='DOB')
        self.tv.column('DOB', anchor='center', width=100)

        self.tv.heading('Anniversary Date', text='Anniversary Date')
        self.tv.column('Anniversary Date', anchor='center', width=100)

        self.tv.grid(row=8, column=1, sticky = (N,S,W,E))
        self.treeview = self.tv
        
        return self.tv