import tkinter as tk

from tkinter import *
from tkinter.ttk import *
  
from model.customer import Customer
from view.helper.comp_helper import ComponentHelper
from view.customer_create import CustomerCreate
from database.db import Database

class CustomerList():
    def __init__(self, win):
        print('customer list constructor')
        self.createWidgets(win)

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
        cust = Customer() #populate this object when opening in edit mode
        cust_create = CustomerCreate(win, cust)
                
    def AddItem(self, tv, cust):
        tv.insert("", 'end', iid=None, text=cust.customer_id, values=(cust.customer_name, cust.phone_number, cust.gender, cust.email_id, cust.DOB, cust.anniversary_date))
        
    def CreateUI(self, win):
        tv = Treeview(win)
        tv['columns'] = ('Customer Name', 'Phone Number', 'Gender', 'Email Id', 'DOB', 'Anniversary Date')
        
        tv.heading("#0", text='#', anchor='w')
        tv.column("#0", anchor="w", width=25)

        tv.heading('Customer Name', text='Customer Name')
        tv.column('Customer Name', anchor='center', width=100)

        tv.heading('Phone Number', text='Phone Number')
        tv.column('Phone Number', anchor='center', width=100)
        
        tv.heading('Gender', text='Gender')
        tv.column('Gender', anchor='center', width=100)
        
        tv.heading('Email Id', text='Email Id')
        tv.column('Email Id', anchor='center', width=100)
        
        tv.heading('DOB', text='DOB')
        tv.column('DOB', anchor='center', width=100)

        tv.heading('Anniversary Date', text='Anniversary Date')
        tv.column('Anniversary Date', anchor='center', width=100)

        tv.grid(row=8, column=1, sticky = (N,S,W,E))
        self.treeview = tv
        
        return tv