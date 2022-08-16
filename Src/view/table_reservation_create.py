import tkinter as tk
from tkinter import *

from datetime import datetime, timedelta
from tkinter import messagebox
from tkinter.ttk import Treeview
from model.table_reservation import TableReservation
from view.helper.comp_helper import ComponentHelper
from database.db import Database
import sys
from view.event import Event


class TableReservationCreate():
    customer = tk.OptionMenu
    table = tk.OptionMenu
    datetime = ''
    pax = 2
    popup = tk.Menu
    tv = Treeview
    id = 0
    
    def __init__(self, win):
        print('create table reservation constructor')
        self.OnViewUpdated = Event()

    def ViewUpdated(self):
        self.OnViewUpdated()
         
    def AddSubscribersForViewUpdatedEvent(self,objMethod):
        self.OnViewUpdated += objMethod
         
    def RemoveSubscribersForViewUpdatedEvent(self,objMethod):
        self.OnViewUpdated -= objMethod

    def createWidgets(self, win, id=0):
        top=win.winfo_toplevel()

        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)

        win.rowconfigure(1, weight=1)
        win.columnconfigure(1, weight=1)

        helper = ComponentHelper()
        win.frame = helper.add_background(win, "./images/table_resev_add_del.gif", 0.90)

        db = Database()
        self.table_list = db.table_get_all()
        table_arr = []
        table_arr.append('Please Select')
        for data in self.table_list:
            table_arr.append(data.table_number)

        self.cust_list = db.customer_get_all()
        cust_arr = []
        cust_arr.append('Please Select')
        for data in self.cust_list:
            cust_arr.append(data.customer_name)

        obj = TableReservation()

        db = Database()
        if(id > 0):            
            self.id = id
            list = db.table_reservation_get_by_id(id)
            for data in list:
                obj.reservation_id=data.reservation_id
                obj.table_id = data.table_id
                obj.table_number = data.table_number
                obj.pax = data.pax
                obj.datetime = data.datetime
                obj.customer_id = data.customer_id
                obj.customer = data.customer

        for data in self.table_list:
            if(data.table_number == obj.table_number):
                obj.location = data.location
                obj.number_of_seats = data.number_of_seats

        helper = ComponentHelper()
        self.customer = helper.create_label_options_menu(win.frame, 0,'Customer', cust_arr, self.item_changed, obj.customer)
        self.table = helper.create_label_options_menu(win.frame, 1,'Table', table_arr, self.table_changed, obj.table_number)
        self.number_of_seats = helper.create_label_label(win.frame, 2,'Number of Seats', obj.number_of_seats)
        self.location = helper.create_label_label(win.frame, 3,'Location', obj.location)
        self.datetime = helper.create_label_entry(win.frame, 4,'DateTime ', obj.datetime)
        self.pax = helper.create_label_entry(win.frame, 5,'Pax', obj.pax)
        
        self.submit = tk.Button(win.frame, text='Cancel', command=lambda:self.table_reservation_cancel())
        self.submit.grid(row=6, column=0, sticky=tk.N+tk.S+tk.E+tk.W)

        self.submit = tk.Button(win.frame, text='Submit', command=lambda:self.table_reservation_create())
        self.submit.grid(row=6, column=1, sticky=tk.N+tk.S+tk.E+tk.W)

    def table_changed(self, *args):
        for data in self.table_list:
            if(data.table_number == args[0]):
                self.number_of_seats.config(text=data.number_of_seats)
                self.location.config(text=data.location)
        
    def table_reservation_cancel(self):
        self.ViewUpdated()
        
    def table_reservation_create(self):
        if self.customer[0].get() == "Please Select":
            messagebox.showerror('Failure!', 'Please Select Customer!')
            return
        if self.table[0].get() == "Please Select":
            messagebox.showerror('Failure!', 'Please Select Table!')
            return
        if self.datetime.get().strip() == "":
            messagebox.showerror('Failure!', 'Please Enter DateTime!')
            return   

        try:
            res = bool(datetime.strptime(self.datetime.get().strip(), '%Y-%m-%d  %H:%M:%S'))
        except BaseException as e:
            print(e)
            messagebox.showerror('Failure!', 'Please enter DateTime in YYYY-mm-dd HH:MM:SS format')
            return   

        if datetime.strptime(self.datetime.get().strip(), '%Y-%m-%d %H:%M:%S') < datetime.now():
            messagebox.showerror('Failure!', 'DateTime should be in the future')
            return   
        if self.pax.get() == "":
            messagebox.showerror('Failure!', 'Please Enter the number of people!')
            return
        if self.pax.get() == "0":
            messagebox.showerror('Failure!', 'Please Enter at least 1 person')
            return
        if int(self.pax.get()) > int(self.number_of_seats.cget("text")):
            messagebox.showerror('Failure!', str(self.table[0].get()) + ' can accomodate only '+ str(self.number_of_seats.cget("text")) + ' people')
            return


        db = Database()
        if(self.id == 0):
            reserv_list = db.table_reservation_get_all()
            for data in reserv_list:
                
                dt = datetime.strptime(str(data.datetime), '%Y-%m-%d %H:%M:%S')
                dt_one = dt + timedelta(hours=1)
                user_dt = datetime.strptime(self.datetime.get().strip(), '%Y-%m-%d %H:%M:%S')
                
                if((dt <= user_dt <= dt_one) and data.table_number == self.table[0].get()):
                    messagebox.showerror('Failure!', 'Table already booked from ' + str(dt) + " to " + str(dt_one))
                    return
        
        reserv = TableReservation()
        for data in self.table_list:
            if data.table_number == self.table[0].get():
                reserv.table_id = data.table_id
        
        for data in self.cust_list:
            if data.customer_name == self.customer[0].get():
                reserv.customer_id = data.customer_id

        reserv.pax = self.pax.get()
        reserv.datetime = self.datetime.get()
        
        try:            
            if(self.id > 0):
                reserv.reservation_id = self.id
                db.table_reservation_update(reserv)
            else:
                db.table_reservation_create(reserv)
            messagebox.showinfo('Success!', 'Table Reserved Successfully')
        except:
            type, value, traceback = sys.exc_info()
            messagebox.showerror('Failure!', value)

        self.ViewUpdated()            
                    
    def item_changed(self, *args):
        print(self)
