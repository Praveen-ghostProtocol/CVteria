from datetime import datetime, timedelta
import tkinter as tk
from tkinter import messagebox

from model.customer import Customer
from view.helper.comp_helper import ComponentHelper
from view.event import Event
from database.db import Database

import mysql.connector as mysql
import re

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
    
    def __init__(self, win):
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

        helper = ComponentHelper()
        win.frame = helper.add_background(win, "./images/customer_add_delete.gif")

        cust = Customer()
        cust.gender = "Please Select"
        db = Database()
        if(cust_id > 0):            
            self.cust_id = cust_id
            cust_list = db.customer_get_by_id(cust_id)
            for data in cust_list:
                cust.customer_id = self.cust_id
                cust.customer_name = data.customer_name
                cust.phone_number = data.phone_number
                if data.gender == 1:
                    cust.gender = "Male"
                elif data.gender == 2:
                    cust.gender = "Female"
                else:
                    cust.gender = "Other"
                cust.gender = data.gender
                cust.email_id = data.email_id
                cust.DOB = data.DOB
                cust.anniversary_date = data.anniversary_date

        helper = ComponentHelper()
        self.name = helper.create_label_entry(win.frame, 1,'Customer Name', cust.customer_name)
        self.phone = helper.create_label_entry(win.frame, 2,'Phone Number', cust.phone_number)
        self.gender = helper.create_label_options_menu(win.frame, 3,'Gender', ['Male','Female','Other'], self.item_changed,cust.gender )
        self.email = helper.create_label_entry(win.frame, 4,'Email Id', cust.email_id)
        self.dob = helper.create_label_entry(win.frame, 5,'Date Of Birth', cust.DOB)
        self.doa = helper.create_label_entry(win.frame, 6,'Anniversary Date', cust.anniversary_date)
        
        self.cancel = tk.Button(win.frame, text='Cancel', command=lambda:self.customer_cancel())
        self.cancel.grid(row=7, column=0, sticky=tk.N+tk.S+tk.E+tk.W)

        self.submit = tk.Button(win.frame, text='Submit', command=lambda:self.customer_create())
        self.submit.grid(row=7, column=1, sticky=tk.N+tk.S+tk.E+tk.W)

    def item_changed(self):
        pass
        
    def customer_cancel(self):
        self.ViewUpdated()
        
    def customer_create(self):
        if self.name.get() == "":
            messagebox.showerror('Failure!', 'Please Enter Customer Name!')
            return
        if self.phone.get() == "":
            messagebox.showerror('Failure!', 'Please Enter The Phone Number!')
            return
        if len(self.phone.get()) < 5:
            messagebox.showerror('Failure!', 'Phone Number should be atleast 5 digits long!')
            return
        if len(self.phone.get()) > 15:
            messagebox.showerror('Failure!', 'Phone Number cannot be longer than 15 digits!')
            return
        if self.gender[0].get() == "" or self.gender[0].get() == "Please Select":
            messagebox.showerror('Failure!', 'Please Enter Gender!')
            return
        if self.email.get() == "":
            messagebox.showerror('Failure!', 'Please Enter The Email ID!')
            return

        try:
            res = bool(datetime.strptime(self.dob.get().strip(), '%Y-%m-%d'))
        except BaseException as e:
            print(e)
            messagebox.showerror('Failure!', 'Please enter appropriate Birthday in YYYY-mm-dd format')
            return   

        if datetime.strptime(self.dob.get().strip(), '%Y-%m-%d') < (datetime.now() - timedelta(days=365*150)):
            messagebox.showerror('Failure!', 'Age should not be more than 150 years')
            return   

        if datetime.strptime(self.dob.get().strip(), '%Y-%m-%d') > (datetime.now() - timedelta(days=365*18)):
            messagebox.showerror('Failure!', 'Age should be at least 18 years')
            return   

        try:
            res = bool(datetime.strptime(self.doa.get().strip(), '%Y-%m-%d'))
        except:
            messagebox.showerror('Failure!', 'Please enter appropriate Anniversary Date in YYYY-mm-dd format')
            return   

        if datetime.strptime(self.doa.get().strip(), '%Y-%m-%d') < (datetime.now() - timedelta(days=365*150)):
            messagebox.showerror('Failure!', 'Anniversary should not be more than 150 years')
            return   

        if datetime.strptime(self.doa.get().strip(), '%Y-%m-%d') < (datetime.strptime(self.dob.get().strip(), '%Y-%m-%d') + timedelta(days=365*18)):
            messagebox.showerror('Failure!', '18 Years gap should be there between Anniversary and Date of Birth')
            return   

        if datetime.strptime(self.dob.get().strip(), '%Y-%m-%d') > datetime.now():
            messagebox.showerror('Failure!', 'Date of Birth cannot be a future date')
            return   

        if datetime.strptime(self.doa.get().strip(), '%Y-%m-%d') > datetime.now():
            messagebox.showerror('Failure!', 'Anniversary Date cannot be a future date')
            return   

        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'        

        if(re.fullmatch(regex, self.email.get())):
            print("Valid Email")
        else:
            messagebox.showerror('Failure!', 'Please Enter valid Email ID!')
            return

        db = Database()

        cust = Customer()
        cust.customer_name = self.name.get()
        cust.phone_number = self.phone.get()
        if self.gender[0].get() == 'Male':
            cust.gender = 1
        elif self.gender[0].get() == "Female":
            cust.gender = 2
        else:
            cust.gender = 3
            
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
        