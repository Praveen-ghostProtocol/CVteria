from tkinter import *
import tkinter as tk
from view.customer_list import CustomerList
from view.order_list import OrderList
from view.bill_list import BillList
from view.welcome import Welcome
from view.table_reservation_list import TableReservationList

from view.helper.comp_helper import ComponentHelper

from database.db import Database

top = tk.Tk()

class CVTeria(tk.Frame):
    def __init__(self, master=None):
        top.title("CVTeria")
        top.geometry("500x300")

        menubar = Menu(top, bg='black', fg='white',font=('Verdana',15))
        
        # Sets menubar background color and active select but does not remove 3d  effect/padding
        menubar.config(bg='black', fg='white',font=('Verdana',15))

        menubar.add_command(label="Welcome",command=self.welcome_page)
        menubar.add_command(label="Customer", command=self.customer_list)
        menubar.add_command(label="Order", command=self.order_list)
        menubar.add_command(label="Reserve Table", command=self.table_reservation_list)
        menubar.add_command(label="Pay Bill", command=self.bill_list)
        menubar.add_command(label="Quit!", command=top.quit)
        top.config(menu=menubar)
        db = Database()

        top.grid()
        
        #uncomment to setup db and seed data
        #db.setup()
        #db.seed()

        self.welcome_page()
        
    def welcome_page(self):
        helper = ComponentHelper()
        helper.remove_all_widgets(top)
        top.geometry("1280x720")    
        Welcome(top)
        print('welcome')
        
    def customer_list(self):
        helper = ComponentHelper()
        helper.remove_all_widgets(top)
        top.geometry("650x300")        
        cust = CustomerList(top)
        cust.createWidgets(top)
        cust.AddSubscribersForViewUpdatedEvent(self.customer_created)        

    def order_list(self):
        helper = ComponentHelper()
        helper.remove_all_widgets(top)
        top.geometry("400x300")        
        ord = OrderList(top)
        ord.createWidgets(top)
        ord.AddSubscribersForViewUpdatedEvent(self.order_created)

    def order_created(self):
        self.order_list()

    def customer_created(self):
        self.customer_list()
        
    def bill_list(self):
        helper = ComponentHelper()
        helper.remove_all_widgets(top)
        top.geometry("575x300")        
        obj = BillList(top)
        obj.createWidgets(top)
        obj.AddSubscribersForViewUpdatedEvent(self.bill_created)

    def bill_created(self):
        self.bill_list()

    def table_reservation_list(self):
        helper = ComponentHelper()
        helper.remove_all_widgets(top)
        top.geometry("480x300")        
        obj = TableReservationList(top)
        obj.createWidgets(top)
        obj.AddSubscribersForViewUpdatedEvent(self.table_reservation_created)

    def table_reservation_created(self):
        self.table_reservation_list()
            
app = CVTeria()
top.mainloop()