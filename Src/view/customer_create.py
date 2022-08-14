from sqlite3 import Date
import tkinter as tk
from tkinter import messagebox

from model.customer import Customer
from view.helper.comp_helper import ComponentHelper
from view.event import Event
from database.db import Database

import mysql.connector as mysql

class CustomerCreate():
    name = tk.Entry
    phone = tk.Entry
    gender = tk.Entry
    email = tk.Entry
    dob = tk.Entry
    doa = tk.Entry
    table_list = []
    customer_list = []
    cust_id = 0
    
    def __init__(self, win, cust=Customer):
        print('create customer constructor')
        self.OnViewUpdated = Event()

    def ViewUpdated(self):
        self.OnViewUpdated()
         
    def AddSubscribersForViewUpdatedEvent(self,objMethod):
        self.OnViewUpdated += objMethod
         
    def RemoveSubscribersForViewUpdatedEvent(self,objMethod):
        self.OnViewUpdated -= objMethod

    def createWidgets(self, win, cust_id=0):
        top=win.winfo_toplevel()

        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)

        win.rowconfigure(1, weight=1)
        win.columnconfigure(1, weight=1)

        cust = Customer()
        
        db = Database()
        if(cust_id > 0):            
            self.cust_id = cust_id
            cust_list = db.customer_get_by_id(cust_id)
            for data in cust_list:
                cust.customer_id = self.cust_id
                cust.customer_name = data.customer_name
                cust.phone_number = data.phone_number
                cust.gender = data.gender
                cust.email_id = data.email_id
                cust.DOB = data.DOB
                cust.anniversary_date = data.anniversary_date

        helper = ComponentHelper()
        self.name = helper.create_label_entry(win, 0,'Customer Name', cust.customer_name)
        self.phone = helper.create_label_entry(win, 1,'Phone Number', cust.phone_number)
        self.gender = helper.create_label_entry(win, 2,'Gender', cust.gender)
        self.email = helper.create_label_entry(win, 3,'Email Id', cust.email_id)
        self.dob = helper.create_label_entry(win, 4,'Date Of Birth', cust.DOB)
        self.doa = helper.create_label_entry(win, 5,'Anniversary Date', cust.anniversary_date)
        
        self.submit = tk.Button(win, text='Submit', command=lambda:self.customer_create())
        self.submit.grid(row=6, column=0, sticky=tk.N+tk.S+tk.E+tk.W)

        self.cancel = tk.Button(win, text='Cancel', command=lambda:self.customer_cancel())
        self.cancel.grid(row=6, column=1, sticky=tk.N+tk.S+tk.E+tk.W)

    def customer_cancel(self):
        self.ViewUpdated()
        
    def customer_create(self):
        if self.name.get() == "":
            messagebox.showerror('Failure!', 'Please Enter Customer Name!')
            return
        if self.phone.get() == "":
            messagebox.showerror('Failure!', 'Please Enter The Phone Number!')
            return
        if self.gender.get() == "":
            messagebox.showerror('Failure!', 'Please Enter Gender!')
            return
        if self.email.get() == "":
            messagebox.showerror('Failure!', 'Please Enter The Email ID!')
            return
        db = Database()

        cust = Customer()
        cust.customer_name = self.name.get()
        cust.phone_number = self.phone.get()
        cust.gender = self.gender.get()
        cust.email_id = self.email.get()
        cust.DOB = self.dob.get()
        cust.anniversary_date = self.doa.get()

        if(int(self.cust_id) > 0):
            cust.customer_id = self.cust_id
            db.customer_update(cust)
            messagebox.showinfo('Success!', 'Customer Updated Successfully')
        else:
            db.customer_create(cust)
            messagebox.showinfo('Success!', 'Customer Created Successfully')
        
        self.ViewUpdated()
        