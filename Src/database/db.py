import mysql.connector as bot

from model.customer import Customer
from model.order import Order
from model.item import Item
from model.table import Table
from model.table_reservation import TableReservation
from model.payment_mode import PaymentMode
from model.bill import Bill

mydb = None

class Database():        
    def connect(self):
        mydb = bot.connect(
            host = 'localhost',
            user = 'root',
            password = 'Tiger@123',
            database = 'cvteria'
        )

        if mydb:
            print('connected to the db successfully!!')
        else:
            print('could not connect to DB')     
        return mydb   
    
    def customer_create(self, cust=Customer): 
        mydb = self.connect()        
        mycursor = mydb.cursor()
        
        sql = "insert into customer(customer_name,customer_phone_number, gender, email_id, DOB, DOA, create_time,update_time) VALUES (%s, %s, %s, %s, %s, %s, now(), now())"
        val = (cust.customer_name, cust.phone_number, cust.gender, cust.email_id, cust.DOB, cust.anniversary_date)
        
        mycursor.execute(sql, val)

        mydb.commit()
        print('customer created ')

    def order_create(self, ord=Order): 
        mydb = self.connect()        
        mycursor = mydb.cursor()

        sql = "insert into cafe_order(menu_id,cafe_table_id, qty, unit_price, gst, total_price, create_time,update_time) VALUES (%s, %s, %s, %s, %s, %s, now(), now())"
        val = (ord.item_id, ord.table_id, ord.qty, ord.price, ord.gst, ord.total_price)
        
        mycursor.execute(sql, val)
        
        mydb.commit()
        print('Order created ')

    def customer_get_all(self): 
        mydb = self.connect()
        mycursor = mydb.cursor()
        mycursor.execute("select customer_id, customer_name,customer_phone_number, gender, email_id, DOB, DOA, create_time,update_time from customer")
        
        list_of_customer = mycursor.fetchall()
        cust_list = []
        for data in list_of_customer:
            cust = Customer()
            cust.customer_id = data[0]
            cust.customer_name = data[1]
            cust.phone_number = data[2]
            cust.gender = data[3]
            cust.email_id = data[4]
            cust.DOB = data[5]
            cust.anniversary_date = data[6]
            cust_list.append(cust)
            print(f"|{cust.customer_id:4}")
        
        return cust_list
        
    def order_get_all(self): 
        mydb = self.connect()
        mycursor = mydb.cursor()
        mycursor.execute("select cafe_order_id, c.menu_id, item, c.cafe_table_id, cafe_table_number, qty, unit_price, gst, total_price, c.create_time from cafe_order c inner join menu m on c.menu_id = m.menu_id inner join cafe_table  t on c.cafe_table_id = t.cafe_table_id order by cafe_order_id")
        
        list = mycursor.fetchall()
        output_list = []
        for data in list:
            ord = Order()
            ord.order_id = data[0]
            ord.item_id = data[1]
            ord.item = data[2]
            ord.table_id = data[3]
            ord.table_number = data[4]
            ord.qty = data[5]
            ord.price = data[6]
            ord.gst = data[7]
            ord.total_price = data[8]
            ord.create_time = data[9]
            
            output_list.append(ord)
            print(f"|{ord.order_id:4}")
        
        return output_list

    def item_get_all(self): 
        mydb = self.connect()
        mycursor = mydb.cursor()
        mycursor.execute("select menu_id, item, price, description, spice_lvl, is_veg, m.category_id, category_name from menu m inner join category c on m.category_id = c.category_id")
        
        list = mycursor.fetchall()
        output_list = []
        for data in list:
            itm = Item()
            itm.item_id = data[0]
            itm.item = data[1]
            itm.price = data[2]
            itm.description = data[3]
            itm.spice_level = data[4]
            itm.veg = data[5]
            itm.category_id = data[6]
            itm.category = data[7]
            
            output_list.append(itm)
            print(f"|{itm.item_id:4}")
        
        return output_list
    
    def table_get_all(self): 
        mydb = self.connect()
        mycursor = mydb.cursor()
        mycursor.execute("select cafe_table_id, cafe_table_number, no_of_seats, location from cafe_table")
        
        list = mycursor.fetchall()
        output_list = []
        for data in list:
            itm = Table()
            itm.table_id = data[0]
            itm.table_number = data[1]
            itm.number_of_seats = data[2]
            itm.location = data[3]
            
            output_list.append(itm)
            print(f"|{itm.table_id:4}")
        
        return output_list
    
    def table_reservation_get_all(self): 
        mydb = self.connect()
        mycursor = mydb.cursor()
        mycursor.execute("select reservation_id, r.no_of_seats, date_time, r.customer_id, customer_name, r.cafe_table_id, cafe_table_number from reservation r inner join customer c on r.customer_id = c.customer_id inner join cafe_table ct on r.cafe_table_id = ct.cafe_table_id")
        
        list = mycursor.fetchall()
        output_list = []
        for data in list:
            itm = TableReservation()
            itm.reservation_id = data[0]
            itm.pax = data[1]
            itm.datetime = data[2]
            itm.customer_id = data[3]
            itm.customer = data[4]
            itm.table_id = data[5]
            itm.table_number = data[6]
            
            output_list.append(itm)
            print(f"|{itm.reservation_id:4}")
        
        return output_list

    def table_reservation_create(self, reserv=TableReservation): 
        mydb = self.connect()        
        mycursor = mydb.cursor()
        
        sql = "insert into reservation(no_of_seats,date_time, customer_id, cafe_table_id, create_time,update_time) VALUES (%s, %s, %s, %s, now(), now())"
        val = (reserv.pax, reserv.datetime, reserv.customer_id, reserv.table_id)
        
        mycursor.execute(sql, val)
        
        mydb.commit()
        print('Table Reservation created ')

    def payment_mode_get_all(self): 
        mydb = self.connect()
        mycursor = mydb.cursor()
        mycursor.execute("select payment_mode_id, payment_mode_name from payment_mode")
        
        list = mycursor.fetchall()
        output_list = []
        for data in list:
            itm = PaymentMode()
            itm.payment_mode_id = data[0]
            itm.payment_mode_name = data[1]
            
            output_list.append(itm)
            print(f"|{itm.payment_mode_id:4}")
        
        return output_list

    def bill_create(self, bill=Bill): 
        mydb = self.connect()        
        mycursor = mydb.cursor()
        
        sql = "insert into bill(cafe_table_id, total_price, customer_id, payment_mode_id, date_time, create_time,update_time) VALUES (%s, %s, %s, %s, %s, now(), now())"
        val = (bill.table_id, bill.total_price, bill.customer_id, bill.payment_mode_id, bill.datetime)
        
        mycursor.execute(sql, val)
        
        mydb.commit()
        print('Bill created ')

    def bill_get_all(self): 
        mydb = self.connect()
        mycursor = mydb.cursor()
        mycursor.execute("select bill_id, b.cafe_table_id, c.cafe_table_number, total_price, b.customer_id, c1.customer_name, b.payment_mode_id, p.payment_mode_name, date_time from bill b inner join cafe_table c on b.cafe_table_id = c.cafe_table_id inner join customer c1 on b.customer_id = c1.customer_id inner join payment_mode p on b.payment_mode_id = p.payment_mode_id")
        
        list = mycursor.fetchall()
        output_list = []
        for data in list:
            bill = Bill()
            bill.bill_id = data[0]
            bill.cafe_table_id = data[1]
            bill.table_number = data[2]
            bill.total_price = data[3]
            bill.customer_id = data[4]
            bill.customer = data[5]
            bill.payment_mode_id = data[6]
            bill.mode_of_payment = data[7]
            bill.datetime = data[8]
            
            output_list.append(bill)
            print(f"|{bill.bill_id:4}")
        
        return output_list
