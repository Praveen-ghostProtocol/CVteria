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
    toolbar = object
    
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

    def createWidgets(self, win, toolbar):
        top=win.winfo_toplevel()
        self.toolbar = toolbar
        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)

        win.rowconfigure(1, weight=1)
        win.columnconfigure(1, weight=1)

        helper = ComponentHelper()
        win.frame = helper.add_background(win, "./images/Customer_list.gif")
        
        win.submit = tk.Button(win.frame, text='Add Customer', command=lambda:self.customer_create(win))
        win.submit.grid(row=2, column=0, sticky=tk.N+tk.S+tk.E+tk.W,padx=10,pady=10)

        tv = self.CreateUI(win.frame)
        
        db = Database()
        cust_list = db.customer_get_all()
        for data in cust_list:
            self.AddItem(tv, data)

    def customer_create(self, win):
        helper = ComponentHelper()
        helper.remove_all_widgets(win)
        win.geometry("1280x785")
        self.toolbar(win)
        self.cust_create.createWidgets(win)

    def edit(self):
        print("Edit", self.popup.selection)

        helper = ComponentHelper()
        helper.remove_all_widgets(self.win)
        self.win.geometry("1280x785")
        row = self.popup.row
        cust_id = self.tv.item(row)['text']
        self.toolbar(self.win)
        self.cust_create.createWidgets(self.win, cust_id)
        
    def delete(self):        
        row = self.popup.row
        cust_id = self.tv.item(row)['text']
        db = Database()
        bill_exist = db.bill_get_buy_customer_id(cust_id)       
                
        try:
            if len(bill_exist) > 0:
                messagebox.showerror('Failure!',"Cannot delete customer, as there is an existing bill for them!")
                return
            else:
                db.customer_delete(cust_id)
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
        self.tv = Treeview(win, height=24)

        #Create menu
        self.popup = tk.Menu(win, tearoff=0)
        self.popup.add_command(label="Edit", command=self.edit)
        self.popup.add_separator()
        self.popup.add_command(label="Delete", command=self.delete)        

        self.tv.bind("<Button-3>", self.do_popup)        

        self.tv['columns'] = ('Customer Name', 'Phone Number', 'Gender', 'Email Id', 'DOB', 'Anniversary Date')
        
        self.tv.heading("#0", text='#', anchor='w')
        self.tv.column("#0", anchor="w", width=50)

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

        self.tv.grid(row=3, column=0, sticky = (N,S,W,E))
        self.treeview = self.tv
        
        return self.tv