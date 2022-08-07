from tkinter import *
import tkinter as tk

from model.customer import Customer
from model.table_reservation import TableReservation
from model.bill import Bill
from view.order_create import OrderCreate
from view.table_create import TableCreate
from view.table_reservation_create import TableReservationCreate
from view.bill_create import BillCreate
from view.customer_list import CustomerList
from view.order_list import OrderList
from view.bill_list import BillList

from view.helper.comp_helper import ComponentHelper
from view.table_reservation_list import TableReservationList

top = Tk()

class CVTeria(tk.Frame):
    def __init__(self, master=None):
        top.title("CVTeria")
        top.geometry("500x300")

        top.grid()
        menubar = Menu(top)
        menubar.add_command(label="Customer", command=self.customer_list)
        menubar.add_command(label="Order", command=self.order_list)
        menubar.add_command(label="Reserve Table", command=self.table_reservation_list)
        menubar.add_command(label="Pay Bill", command=self.bill_list)
        menubar.add_command(label="Quit!", command=top.quit)
        top.config(menu=menubar)  

    def customer_list(self):
        helper = ComponentHelper()
        helper.remove_all_widgets(top)
        top.geometry("650x300")        
        cust_create = CustomerList(top)

    def order_list(self):
        helper = ComponentHelper()
        helper.remove_all_widgets(top)
        top.geometry("750x300")        
        OrderList(top)

    def bill_list(self):
        helper = ComponentHelper()
        helper.remove_all_widgets(top)
        top.geometry("575x300")        
        BillList(top)

    def table_reservation_list(self):
        helper = ComponentHelper()
        helper.remove_all_widgets(top)
        top.geometry("480x300")        
        TableReservationList(top)
            
app = CVTeria()
top.mainloop()