import tkinter as tk

from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *
  
from model.customer import Customer
from model.table_reservation import TableReservation
from view.helper.comp_helper import ComponentHelper
from view.table_reservation_create import TableReservationCreate
from database.db import Database
from view.event import Event

class TableReservationList():
    tv = Treeview
    win = object
    toolbar = object
    
    def __init__(self, win):
        print('table list constructor')
        self.tbl_reservation_create = TableReservationCreate(win)
        self.tbl_reservation_create.AddSubscribersForViewUpdatedEvent(self.table_reservation_created)
        self.OnViewUpdated = Event()
        self.win = win

    def ViewUpdated(self):
        self.OnViewUpdated()
         
    def AddSubscribersForViewUpdatedEvent(self,objMethod):
        self.OnViewUpdated += objMethod
         
    def RemoveSubscribersForViewUpdatedEvent(self,objMethod):
        self.OnViewUpdated -= objMethod

    def createWidgets(self, win, toolbar):
        top=win.winfo_toplevel()
        self.toolbar = toolbar
        
        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)

        win.rowconfigure(1, weight=1)
        win.columnconfigure(1, weight=1)

        helper = ComponentHelper()
        win.frame = helper.add_background(win, "./images/table_reservation.gif")
                
        win.submit = tk.Button(win.frame, text='Add Table Reservation', command=lambda:self.table_reservation_create(win))
        win.submit.grid(row=2, column=0, sticky=tk.N+tk.S+tk.E+tk.W,padx=10,pady=10)

        help = tk.Label(win.frame, text='*Right click to Edit or Delete', background='#CC8066', foreground='white')
        help.grid(row=3, column=0, sticky=tk.W, pady=5)

        tv = self.CreateUI(win.frame)

        db = Database()
        reserv_list = db.table_reservation_get_all()
        for data in reserv_list:
            self.AddItem(tv, data)

    def table_reservation_created(self):
        self.ViewUpdated()
        print('order created')

    def table_reservation_create(self, win):
        helper = ComponentHelper()
        helper.remove_all_widgets(win)
        win.geometry("1280x785")
        self.toolbar(win)
        self.tbl_reservation_create.createWidgets(win)
                
    def AddItem(self, tv, reserv=TableReservation):
        tv.insert("", 'end', iid=None, text=reserv.reservation_id, values=(reserv.table_number, reserv.pax, reserv.datetime, reserv.customer))

    def edit(self):
        print("Edit", self.popup.selection)
        row = self.popup.row
        id = self.tv.item(row)['text']
        if(id == '' or int(id) == 0):
            messagebox.showerror('Failure!', 'Please select a Row!')
            return

        helper = ComponentHelper()
        helper.remove_all_widgets(self.win)
        self.win.geometry("1280x785")
        self.toolbar(self.win)
        self.tbl_reservation_create.createWidgets(self.win, id)
        
    def delete(self):        
        row = self.popup.row
        id = self.tv.item(row)['text']
        if(id == '' or int(id) == 0):
            messagebox.showerror('Failure!', 'Please select a Row!')
            return

        db = Database()
        db.table_reservation_delete(id)

        try:
            selected_item = self.tv.selection()[0]    
            self.tv.delete(selected_item)
        except:
            messagebox.showerror('Failure!', 'Please select an Item before Deleting!')
            return
                
        messagebox.showinfo('Success!', 'Deleted Successfully')
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
        
    def CreateUI(self, win):
        self.tv = Treeview(win, height=22)

        #Create menu
        self.popup = tk.Menu(win, tearoff=0)
        self.popup.add_command(label="Edit", command=self.edit)
        self.popup.add_separator()
        self.popup.add_command(label="Delete", command=self.delete)        

        self.tv.bind("<Button-3>", self.do_popup)        
        
        self.tv['columns'] = ('Table Number', 'Pax', 'DateTime', 'Customer')
        
        self.tv.heading("#0", text='#', anchor='w')
        self.tv.column("#0", anchor="w", width=50)

        self.tv.heading('Table Number', text='Table Number')
        self.tv.column('Table Number', anchor='center', width=150)

        self.tv.heading('Pax', text='Pax')
        self.tv.column('Pax', anchor='center', width=100)
        
        self.tv.heading('DateTime', text='DateTime')
        self.tv.column('DateTime', anchor='center', width=150)
        
        self.tv.heading('Customer', text='Customer')
        self.tv.column('Customer', anchor='center', width=200)

        self.tv.grid(row=4, column=0, sticky = (N,S,W,E))
        self.treeview = self.tv
        
        return self.tv
