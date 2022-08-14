import tkinter as tk

from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
from model import order_detail
  
from model.item import Item
from model.order_header import OrderHeader
from model.order_detail import OrderDetail

from view.helper.comp_helper import ComponentHelper
from view.view import View
from view.event import Event

from database.db import Database

class OrderCreate():
    i=1
    item = tk.OptionMenu
    table = tk.OptionMenu
    qty = tk.Entry
    price = tk.Label
    gst = tk.Label
    #amount = tk.Label
    description = tk.Label
    spice_lvl = tk.Label
    veg = tk.Label
    category = tk.Label
    item_list = []
    table_list = []
    order_details = []
    popup = tk.Menu
    tv = Treeview
    order_header_id = 0
    win=object
    
    def __init__(self):
        print('create order constructor')
        self.item_list = []
        self.table_list = []
        self.order_details = []
        self.OnViewUpdated = Event()
         
    def ViewUpdated(self):
        self.OnViewUpdated()
         
    def AddSubscribersForViewUpdatedEvent(self,objMethod):
        self.OnViewUpdated += objMethod
         
    def RemoveSubscribersForViewUpdatedEvent(self,objMethod):
        self.OnViewUpdated -= objMethod
        
    def createWidgets(self, win, order_header_id=''):
        top=win.winfo_toplevel()

        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)

        win.rowconfigure(1, weight=1)
        win.columnconfigure(1, weight=1)
        self.win = win

        db = Database()
        self.item_list = db.item_get_all()
        item_arr = []
        item_arr.append('Please Select')
        for data in self.item_list:
            item_arr.append(data.item)
        
        self.table_list = db.table_get_all()
        table_arr = []
        table_arr.append('Please Select')
        for data in self.table_list:
            table_arr.append(data.table_number)

        self.category_list = db.category_get_all()
        category_arr = []
        category_arr.append('Please Select')
        for data in self.category_list:
            category_arr.append(data.category_name)
        
        helper = ComponentHelper()
        
        order_header = OrderHeader()
        
        if(order_header_id != ''):            
            self.order_header_id = order_header_id
            order_header_list = db.order_header_get_by_id(order_header_id)
            for data in order_header_list:
                order_header.order_header_id = order_header_id
                order_header.table_id = data.table_id
                order_header.table_number = data.table_number
                order_header.total_amount = data.total_amount
        
        header = Frame(win)  
        header['padding'] = 1
        header['width'] = 500
        header['height'] = 100
        header['borderwidth'] = 1
        header['relief'] = 'sunken'
        header.grid(columnspan=2,sticky=tk.N+tk.S+tk.E+tk.W)
        
        self.table = helper.create_label_options_menu(header, 0,'Table', table_arr, self.table_changed, order_header.table_number)
        self.total_amount = helper.create_label_label(header, 1,'Total Amount', order_header.total_amount)
        
        self.category = helper.create_label_options_menu(win, 2,'Category', category_arr, self.category_changed)
        self.item = helper.create_label_options_menu(win, 3,'Item Name', item_arr, self.item_changed)
        self.qty = helper.create_label_entry(win, 4,'Quantity', 1)
        self.price = helper.create_label_label(win, 5,'Price', 0)
        self.description = helper.create_label_label(win, 6,'Description', '')
        self.spice_lvl = helper.create_label_label(win, 7,'Spice Level', 1)
        self.veg = helper.create_label_label(win, 8,'Veg', 'Yes')
        self.gst = helper.create_label_label(win, 9,'GST', '18')
        #self.amount = helper.create_label_label(win, 10,'Amount', 1)
                
        button_frame = Frame(win)  
        button_frame['padding'] = 1
        button_frame.grid(columnspan=2)

        self.add = tk.Button(button_frame, text='Add Item', command=lambda:self.AddItem(tv, False))
        self.add.grid(row=11, column=1, sticky=tk.N+tk.S+tk.E+tk.W,padx=10,pady=10)

        self.update = tk.Button(button_frame, text='Update', command=lambda:self.UpdateItem(tv))
        self.update.grid(row=11, column=2, sticky=tk.N+tk.S+tk.E+tk.W,padx=10,pady=10)

        self.cancel = tk.Button(button_frame, text='Cancel', command=lambda:self.Cancel())
        self.cancel.grid(row=11, column=3, sticky=tk.N+tk.S+tk.E+tk.W,padx=10,pady=10)

        self.enable_insert(True)

        help = tk.Label(button_frame, text='*Right click to Edit or Delete the Item')
        help.grid(row=12, column=1, sticky=tk.N+tk.S+tk.E+tk.W,padx=10,pady=10)
        
        tv = self.CreateUI(win, 13)

        if(order_header_id != ''):
            order_detail_list = db.order_detail_get_by_id(order_header_id)
            for data in order_detail_list:
                order_detail = OrderDetail()
                order_detail.order_detail_id = data.order_detail_id
                order_detail.order_header_id = order_header_id
                order_detail.item_id = data.item_id
                order_detail.item = data.item
                order_detail.qty = data.qty
                order_detail.price = data.price
                order_detail.amount = data.amount
                self.order_details.append(order_detail)
                tv.insert("", 'end', iid=None, text=self.i, values=(data.item, data.qty, data.price, data.gst, data.amount))
                self.i = self.i + 1
        
        submit_button_frame = Frame(win)  
        submit_button_frame['padding'] = 1
        submit_button_frame.grid(columnspan=2)

        self.submit = tk.Button(submit_button_frame, text='Submit Order', command=lambda:self.order_create())
        self.submit.grid(row=14, column=1, sticky=tk.N+tk.S+tk.E+tk.W,padx=10,pady=10)

        self.cancel_submit = tk.Button(submit_button_frame, text='Cancel', command=lambda:self.order_cancel())
        self.cancel_submit.grid(row=14, column=2, sticky=tk.N+tk.S+tk.E+tk.W,padx=10,pady=10)

    def category_changed(self, *args):
        self.price.config(text=0)
        self.description.config(text='')
        self.spice_lvl.config(text=1)
        self.veg.config(text='Yes')
        self.gst.config(text=18)
        
        category_id=0
        for data in self.category_list:
            if data.category_name == self.category[0].get():
                category_id = data.category_id
        
        self.item[0].set('')
        self.item[1]['menu'].delete(0, 'end')
        self.item[1]['menu'].add_command(label='Please Select', command=tk._setit(self.item[0], 'Please Select'))

        db = Database()
        self.item_list = db.item_get_by_category_id(category_id)
        item_arr = []
        item_arr.append('Please Select')
        for data in self.item_list:
            item_arr.append(data.item)
            #self.item[1]['menu'].add_command(label=data.item, command=lambda:self.item_changed(data.item))
            self.item[1]['menu'].add_command(label=data.item, command=tk._setit(self.item[0], data.item, self.item_changed))
        
    def order_cancel(self):
        self.ViewUpdated()

    def Cancel(self):
        self.enable_insert(True)

    def UpdateItem(self, tv):
        self.AddItem(tv, True)
        
    def enable_insert(self, flag):
        if flag:
            self.add["state"] = "normal"
            self.item[1].configure(state="normal")
            self.category[1].configure(state="normal")
            self.update["state"] = "disabled"
            self.cancel["state"] = "disabled"
        else:
            self.add["state"] = "disabled"
            self.item[1].configure(state="disabled")
            self.category[1].configure(state="disabled")
            self.update["state"] = "normal"
            self.cancel["state"] = "normal"
            
    def item_changed(self, *args):
        print(self)
        self.price.config(text=0)
        self.description.config(text='')
        self.spice_lvl.config(text=1)
        self.veg.config(text='Yes')
        self.gst.config(text=18)

        helper = ComponentHelper()
        helper.change_text(self.qty, 1)

        for data in self.item_list:
            if data.item == args[0]:                
                self.price.config(text=data.price)
                self.description.config(text=data.description)
                if(data.spice_level == 0):
                    self.spice_lvl.config(text='Low')
                elif(data.spice_level == 1):
                    self.spice_lvl.config(text='Medium')
                elif(data.spice_level == 2):
                    self.spice_lvl.config(text='High')
                
                if(data.veg == 1):
                    self.veg.config(text='Yes')
                
                #self.category[0].set(data.category)

    def table_changed(self, *args):
        print(self)
        #self.output_label['text'] = f'You selected: {self.option_var.get()}'

    def order_create(self):
        if self.table[0].get() == "Please Select":
            messagebox.showerror('Failure!', 'Please Select Table Number!')
            return
        if not self.order_details:
            messagebox.showerror('Failure!', 'Please Add atleast one item!')
            return
        
        db = Database()

        order_header = OrderHeader()
        for data in self.table_list:
            if data.table_number == self.table[0].get():
                order_header.table_id = data.table_id

        order_header.total_amount = self.total_amount.cget("text")

        if(self.order_header_id != '' and self.order_header_id != 0):            
            order_header.order_header_id = self.order_header_id
            self.order_header_id = db.order_header_update(order_header)
            db.order_detail_delete_by_id(self.order_header_id)
        else:
            self.order_header_id = db.order_header_create(order_header)
        
        for ord in self.order_details:
            order_detail = OrderDetail()
            order_detail.order_detail_id = ord.order_detail_id
            order_detail.order_header_id = self.order_header_id
            order_detail.item_id = ord.item_id
            order_detail.qty = ord.qty
            order_detail.price = ord.price
            order_detail.amount = ord.amount
            db.order_detail_create(order_detail)


        messagebox.showinfo('Success!', 'Order Created Successfully')
        self.ViewUpdated()
        
    def AddItem(self, tv, update):
        if self.table[0].get() == "Please Select":
            messagebox.showerror('Failure!', 'Please Select Table!')
            return

        if self.item[0].get() == "Please Select":
            messagebox.showerror('Failure!', 'Please Select Item Name!')
            return

        if self.qty.get() == "0" or self.qty.get() == "":
            messagebox.showerror('Failure!', 'Quantity Should be greater than Zero')
            return

        if int(self.qty.get()) > 9:
            messagebox.showerror('Failure!', 'Quantity Should be less than TEN')
            return

        if int(self.qty.get()) < 0:
            messagebox.showerror('Failure!', 'Quantity Should be greater than 0')
            return

        if(update == False):
            for row in self.order_details:
                if(row.item == self.item[0].get()):
                    messagebox.showerror('Failure!', 'Item already present in order, to make changes, edit the item')
                    return
                
        
        order_detail = OrderDetail()        
        for data in self.item_list:
            if data.item == self.item[0].get():
                order_detail.item_id = data.item_id
                order_detail.item = self.item[0].get()
        
        order_detail.qty = self.qty.get()
        order_detail.price = self.price.cget("text")
        order_detail.gst = self.gst.cget("text")
        order_detail.amount = float(order_detail.qty) * float(order_detail.price) * (1 + (float(order_detail.gst)/100))
                        
        if(update == True):
            x = tv.get_children()
            print(x)
            for row in x:
                values = tv.item(row)['values']
                if(values[0] == order_detail.item):
                    tv.item(row, text=tv.item(row)['text'], values=(order_detail.item, order_detail.qty, order_detail.price, order_detail.gst, order_detail.amount))
            for row in self.order_details:
                if(order_detail.item == row.item):
                    row.qty = order_detail.qty
                    row.amount = order_detail.amount
        else:            
            self.order_details.append(order_detail)
            tv.insert("", 'end', iid=None, text=self.i, values=(order_detail.item, order_detail.qty, order_detail.price, order_detail.gst, order_detail.amount))
            self.i = self.i + 1

        total_amount = 0
        for row in self.order_details:
            total_amount = total_amount + row.amount
        
        self.total_amount.config(text=total_amount)
        
        self.enable_insert(True)

    def edit(self):
        print("Edit", self.popup.selection)
        self.item[0].set(self.popup.selection['Item'])
        helper = ComponentHelper()
        helper.change_text(self.qty, self.popup.selection['Qty'])
        self.price.config(text=str(self.popup.selection['Price']))
        
        for data in self.item_list:
            if data.item == self.item[0].get():
                self.category[0].set(data.category)
        
        self.enable_insert(False)        
        
    def delete(self):
        print("Delete", self.popup.selection)
        try:
            selected_item = self.tv.selection()[0]    
            self.tv.delete(selected_item)
        except:
            messagebox.showerror('Failure!', 'Please select an Item before Deleting!')
            return

        ord_det = OrderDetail()
        for row in self.order_details:
            if(row.item == self.popup.selection['Item']):
                ord_det = row

        if(ord_det.amount > 0):
            self.order_details.remove(ord_det)

        total_amount = 0
        for row in self.order_details:
            total_amount = total_amount + row.amount

        self.total_amount.config(text=total_amount)

    def do_popup(self, event):
        # display the popup menu
        try:
            self.popup.selection = self.treeview.set(self.treeview.identify_row(event.y))
            self.popup.post(event.x_root, event.y_root)
        finally:
            # make sure to release the grab (Tk 8.0a1 only)
            self.popup.grab_release()    

    def CreateUI(self, win, row):
        #Create menu
        self.popup = tk.Menu(win, tearoff=0)
        self.popup.add_command(label="Edit", command=self.edit)
        self.popup.add_separator()
        self.popup.add_command(label="Delete", command=self.delete)        
                
        self.tv = Treeview(win)
        self.tv.bind("<Button-3>", self.do_popup)        
        
        self.tv['columns'] = ('Item', 'Qty', 'Price', 'GST', 'Amount')
        
        self.tv.heading("#0", text='S No', anchor='w')
        self.tv.column("#0", anchor="w", width=25)

        self.tv.heading('Item', text='Item')
        self.tv.column('Item', anchor='center', width=100)

        self.tv.heading('Qty', text='Qty')
        self.tv.column('Qty', anchor='center', width=100)
        
        self.tv.heading('Price', text='Price')
        self.tv.column('Price', anchor='center', width=100)
        
        self.tv.heading('GST', text='GST')
        self.tv.column('GST', anchor='center', width=100)
        
        self.tv.heading('Amount', text='Amount')
        self.tv.column('Amount', anchor='center', width=100)

        self.tv.grid(row=row, column=1, sticky = (N,S,W,E))
        self.treeview = self.tv
        
        return self.tv