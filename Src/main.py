from tkinter import *
import tkinter as tk
from view.helper.comp_helper import ComponentHelper
from view.customer_list import CustomerList
from view.order_list import OrderList
from view.bill_list import BillList
from view.welcome import Welcome
from view.table_reservation_list import TableReservationList

from database.db import Database

top = tk.Tk()

class CVTeria(tk.Frame):
    def __init__(self, master=None):
        top.title("CVTeria")
        top.geometry("500x300")

        top.grid()

        #uncomment to setup db and seed data
        # db = Database()
        # db.setup()
        # db.seed()

        self.welcome_page()
        
    def welcome_page(self):
        helper = ComponentHelper()
        helper.remove_all_widgets(top)
        top.geometry("1280x785")
        self.add_toolbar(top)
        Welcome(top)
        print('welcome')
        
    def customer_list(self):
        helper = ComponentHelper()
        helper.remove_all_widgets(top)
        top.geometry("1280x785")
        cust = CustomerList(top)
        self.add_toolbar(top)
        cust.createWidgets(top, self.add_toolbar)
        cust.AddSubscribersForViewUpdatedEvent(self.customer_created)        

    def order_list(self):
        helper = ComponentHelper()
        helper.remove_all_widgets(top)
        top.geometry("1280x785")       
        ord = OrderList(top)
        self.add_toolbar(top)
        ord.createWidgets(top, self.add_toolbar)
        ord.AddSubscribersForViewUpdatedEvent(self.order_created)

    def order_created(self):
        self.order_list()

    def customer_created(self):
        self.customer_list()
        
    def bill_list(self):
        helper = ComponentHelper()
        helper.remove_all_widgets(top)
        top.geometry("1280x785")
        obj = BillList(top)
        self.add_toolbar(top)
        obj.createWidgets(top, self.add_toolbar)
        obj.AddSubscribersForViewUpdatedEvent(self.bill_created)

    def bill_created(self):
        self.bill_list()

    def table_reservation_list(self):
        helper = ComponentHelper()
        helper.remove_all_widgets(top)
        top.geometry("1280x785")
        obj = TableReservationList(top)
        self.add_toolbar(top)
        obj.createWidgets(top, self.add_toolbar)
        obj.AddSubscribersForViewUpdatedEvent(self.table_reservation_created)

    def table_reservation_created(self):
        self.table_reservation_list()

    def add_toolbar(self, win):
        canvas= tk.Canvas(win, bg='#CC8066')
        canvas.grid(row=0, column=0, sticky=tk.N+tk.S+tk.E+tk.W)

        button = tk.Button(canvas, text='Welcome', bg='#CC8066', fg='white',font=('Comic Sans MS',15), command=self.welcome_page)
        button.grid(row=0, column=1, sticky=tk.N+tk.S+tk.E+tk.W,padx=(65, 65), pady=(10, 10))
        
        button = tk.Button(canvas, text='Customer', bg='#CC8066', fg='white',font=('Comic Sans MS',15), command=self.customer_list)
        button.grid(row=0, column=2, sticky=tk.N+tk.S+tk.E+tk.W,padx=(65, 65), pady=(10, 10))

        button = tk.Button(canvas, text='Order', bg='#CC8066', fg='white',font=('Comic Sans MS',15), command=self.order_list)
        button.grid(row=0, column=3, sticky=tk.N+tk.S+tk.E+tk.W,padx=(65, 65), pady=(10, 10))

        button = tk.Button(canvas, text='Reserve', bg='#CC8066', fg='white',font=('Comic Sans MS',15), command=self.table_reservation_list)
        button.grid(row=0, column=4, sticky=tk.N+tk.S+tk.E+tk.W,padx=(65, 65), pady=(10, 10))

        button = tk.Button(canvas, text='Bill', bg='#CC8066', fg='white',font=('Comic Sans MS',15), command=self.bill_list)
        button.grid(row=0, column=5, sticky=tk.N+tk.S+tk.E+tk.W,padx=(65, 65), pady=(10, 10))

        button = tk.Button(canvas, text='Quit', bg='#CC8066', fg='white',font=('Comic Sans MS',15), command=top.quit)
        button.grid(row=0, column=6, sticky=tk.N+tk.S+tk.E+tk.W,padx=(65, 65), pady=(10, 10))

app = CVTeria()
top.mainloop()