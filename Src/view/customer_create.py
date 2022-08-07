import tkinter as tk

from model.customer import Customer
from view.helper.comp_helper import ComponentHelper
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
    
    def __init__(self, win, cust=Customer):
        print('create customer constructor')
        self.createWidgets(win, cust)

    def createWidgets(self, win, cust=Customer):
        top=win.winfo_toplevel()

        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)

        win.rowconfigure(1, weight=1)
        win.columnconfigure(1, weight=1)

        helper = ComponentHelper()
        self.name = helper.create_label_entry(win, 0,'Customer Name', cust.customer_name)
        self.phone = helper.create_label_entry(win, 1,'Phone Number', cust.phone_number)
        self.gender = helper.create_label_entry(win, 2,'Gender', cust.gender)
        self.email = helper.create_label_entry(win, 3,'Email Id', cust.email_id)
        self.dob = helper.create_label_entry(win, 4,'Date Of Birth', cust.DOB)
        self.doa = helper.create_label_entry(win, 5,'Anniversary Date', cust.anniversary_date)
        
        self.submit = tk.Button(win, text='Submit', command=lambda:self.customer_create())
        self.submit.grid(row=6, column=1, sticky=tk.N+tk.S+tk.E+tk.W)

    def customer_create(self):
        db = Database()

        cust = Customer()
        cust.customer_name = self.name.get()
        cust.phone_number = self.phone.get()
        cust.gender = self.gender.get()
        cust.email_id = self.email.get()
        cust.DOB = self.dob.get()
        cust.anniversary_date = self.doa.get()

        db.customer_create(cust)