import mysql.connector as bot
from model.category import Category

from model.customer import Customer
from model.order_header import OrderHeader
from model.order_detail import OrderDetail
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
    
    def setup(self):
        #CREATE DATBASE
        con = bot.connect(host="localhost",user="root",password="Tiger@123",charset='utf8')
        cur = con.cursor()        
        cur.execute("""
            CREATE DATABASE IF NOT EXISTS cvteria
            """)

        mydb = self.connect()        
        mycursor = mydb.cursor()
        
        #CREATE TABLES
        #size
        mycursor.execute("""
            CREATE TABLE IF NOT EXISTS
            size(  
                size_id int NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT 'Primary Key',
                create_time DATETIME COMMENT 'Create Time',
                update_time DATETIME COMMENT 'Update Time',
                size_name VARCHAR(255)    
            );                         
            """)

        #category
        mycursor.execute("""
            CREATE TABLE IF NOT EXISTS
            category(  
                category_id int NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT 'Primary Key',
                create_time DATETIME COMMENT 'Create Time',
                update_time DATETIME COMMENT 'Update Time',
                category_name VARCHAR(255)    
            );
            """)
        
        #payment_mode
        mycursor.execute("""
            CREATE TABLE IF NOT EXISTS
            payment_mode(  
                payment_mode_id int NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT 'Primary Key',
                create_time DATETIME COMMENT 'Create Time',
                update_time DATETIME COMMENT 'Update Time',
                payment_mode_name VARCHAR(255)    
            );
            """)

        #menu
        mycursor.execute("""
            CREATE TABLE IF NOT EXISTS
            menu(  
                menu_id int NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT 'Primary Key',
                create_time DATETIME COMMENT 'Create Time',
                update_time DATETIME COMMENT 'Update Time',
                item VARCHAR(255),
                price FLOAT,
                image VARCHAR(255),
                size_id INT, INDEX size_id (size_id),CONSTRAINT fk_size_id FOREIGN KEY (size_id) REFERENCES size(size_id)   ,
                description VARCHAR(255),
                spice_lvl INT,
                is_veg BOOLEAN,
                category_id INT, INDEX category_id (category_id),CONSTRAINT fk_category_id FOREIGN KEY (category_id) REFERENCES category(category_id) 
            );
            """)

        #cafe_table
        mycursor.execute("""
            CREATE TABLE IF NOT EXISTS
            cafe_table(  
                cafe_table_id int NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT 'Primary Key',
                create_time DATETIME COMMENT 'Create Time',
                update_time DATETIME COMMENT 'Update Time',
                no_of_seats INT,
                cafe_table_number VARCHAR(255),
                location VARCHAR(255)  
            );
            """)

        #customer
        mycursor.execute("""
            CREATE TABLE IF NOT EXISTS
            customer(  
                customer_id int NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT 'Primary Key',
                create_time DATETIME COMMENT 'Create Time',
                update_time DATETIME COMMENT 'Update Time',
                customer_name VARCHAR(255), 
                customer_phone_number VARCHAR(255),
                gender BOOLEAN,
                email_id VARCHAR(255),
                DOB DATE,
                DOA DATE
            );
            """)

        #reservation
        mycursor.execute("""
            CREATE TABLE IF NOT EXISTS
            reservation(  
                reservation_id int NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT 'Primary Key',
                create_time DATETIME COMMENT 'Create Time',
                update_time DATETIME COMMENT 'Update Time',
                no_of_seats INT,
                date_time DATETIME,
                customer_id INT, INDEX customer_id (customer_id),CONSTRAINT fk_customer_id FOREIGN KEY (customer_id) REFERENCES customer(customer_id) ,
                cafe_table_id INT, INDEX cafe_table_id (cafe_table_id),CONSTRAINT fk_cafe_table_id FOREIGN KEY (cafe_table_id) REFERENCES cafe_table(cafe_table_id) 
            );
            """)

        #cafe_order_header
        mycursor.execute("""
            CREATE TABLE IF NOT EXISTS
            cafe_order_header(  
                cafe_order_header_id int NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT 'Primary Key',
                create_time DATETIME COMMENT 'Create Time',
                update_time DATETIME COMMENT 'Update Time',
                cafe_table_id INT, INDEX cafe_table_id(cafe_table_id),CONSTRAINT fk_cafe_order_header_cafe_table_id FOREIGN KEY (cafe_table_id) REFERENCES cafe_table(cafe_table_id) ,
                total_amount FLOAT
            );
            """)

        #cafe_order_detail
        mycursor.execute("""
            CREATE TABLE IF NOT EXISTS
            cafe_order_detail(  
                cafe_order_detail_id int NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT 'Primary Key',
                cafe_order_header_id INT, INDEX cafe_order_header_id(cafe_order_header_id),CONSTRAINT fk_cafe_order_header_id FOREIGN KEY (cafe_order_header_id) REFERENCES cafe_order_header(cafe_order_header_id) ,
                create_time DATETIME COMMENT 'Create Time',
                update_time DATETIME COMMENT 'Update Time',
                menu_id INT, INDEX menu_id(menu_id),CONSTRAINT fk_cafe_order_detail_menu_id FOREIGN KEY (menu_id) REFERENCES menu(menu_id) ,
                qty INT,
                unit_price float,
                gst float,
                amount FLOAT
            );
            """)

        #bill
        mycursor.execute("""
            CREATE TABLE IF NOT EXISTS
            bill(  
                bill_id int NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT 'Primary Key',
                cafe_order_header_id INT, INDEX cafe_order_header_id(cafe_order_header_id),CONSTRAINT fk_cafe_order_header_id_bill FOREIGN KEY (cafe_order_header_id) REFERENCES cafe_order_header(cafe_order_header_id) ,
                discount float,
                final_amount float,	
                create_time DATETIME COMMENT 'Create Time',
                update_time DATETIME COMMENT 'Update Time',
                customer_id INT, INDEX customer_id (customer_id),CONSTRAINT fk_bill_customer_id FOREIGN KEY (customer_id) REFERENCES customer(customer_id) ,
                payment_mode_id INT, INDEX payment_mode_id (payment_mode_id),CONSTRAINT fk_payment_mode_id FOREIGN KEY (payment_mode_id) REFERENCES payment_mode(payment_mode_id) ,
                date_time DATETIME
            );
            """)
        mydb.commit()
            
    def seed(self):
        mydb = self.connect()        
        mycursor = mydb.cursor()
        #INSERT DEFAULT RECORDS
        #size
        mycursor.execute("insert into size(size_name,create_time,update_time) VALUES('Demi',now(),now());")
        mycursor.execute("insert into size(size_name,create_time,update_time) VALUES('Short',now(),now());")
        mycursor.execute("insert into size(size_name,create_time,update_time) VALUES('Tall',now(),now());")
        mycursor.execute("insert into size(size_name,create_time,update_time) VALUES('Venti',now(),now());")
        mycursor.execute("insert into size(size_name,create_time,update_time) VALUES('Grande',now(),now());")
        mycursor.execute("insert into size(size_name,create_time,update_time) VALUES('Trenta',now(),now());")
        
        mydb.commit()
        
        #category
        mycursor.execute("insert into category(category_name,create_time,update_time) VALUES('Hot Beverages',now(),now());")
        mycursor.execute("insert into category(category_name,create_time,update_time) VALUES('Cold Beverages',now(),now());")
        mycursor.execute("insert into category(category_name,create_time,update_time) VALUES('Quick Bites',now(),now());")
        mycursor.execute("insert into category(category_name,create_time,update_time) VALUES('Sandwiches',now(),now());")
        mycursor.execute("insert into category(category_name,create_time,update_time) VALUES('Desserts',now(),now());")
        mycursor.execute("insert into category(category_name,create_time,update_time) VALUES('Donuts',now(),now());")
        mycursor.execute("insert into category(category_name,create_time,update_time) VALUES('English Breakfast',now(),now());")
        mycursor.execute("insert into category(category_name,create_time,update_time) VALUES('Soups',now(),now());")
        mycursor.execute("insert into category(category_name,create_time,update_time) VALUES('Grab-n-Go',now(),now());")
        mydb.commit()
        
        #payment_mode
        mycursor.execute("insert into payment_mode(payment_mode_name,create_time,update_time) VALUES('Cash',now(),now());")
        mycursor.execute("insert into payment_mode(payment_mode_name,create_time,update_time) VALUES('Card',now(),now());")
        mycursor.execute("insert into payment_mode(payment_mode_name,create_time,update_time) VALUES('UPI',now(),now());")
        mydb.commit()

        #menu
        mycursor.execute("insert into menu(item, price, size_id, description, spice_lvl, is_veg, category_id, create_time,update_time) VALUES('Cappucino', 399, null, null, 0, True, 1, now(),now());")
        mycursor.execute("insert into menu(item, price, size_id, description, spice_lvl, is_veg, category_id, create_time,update_time) VALUES('Yamamoto Tea', 299, null, null, 0, True, 1, now(),now());")
        mycursor.execute("insert into menu(item, price, size_id, description, spice_lvl, is_veg, category_id, create_time,update_time) VALUES('Miguel Drink', 249, null, null, 0, True, 1, now(),now());")
        mycursor.execute("insert into menu(item, price, size_id, description, spice_lvl, is_veg, category_id, create_time,update_time) VALUES('Hot Chocolate', 349, null, null, 0, True, 1, now(),now());")
        mycursor.execute("insert into menu(item, price, size_id, description, spice_lvl, is_veg, category_id, create_time,update_time) VALUES('Frappe', 399, null, null, 0, True, 2, now(),now());")
        mycursor.execute("insert into menu(item, price, size_id, description, spice_lvl, is_veg, category_id, create_time,update_time) VALUES('Iced Tea', 299, null, null, 0, True, 2, now(),now());")
        mycursor.execute("insert into menu(item, price, size_id, description, spice_lvl, is_veg, category_id, create_time,update_time) VALUES('Oreo Milkshake', 249, null, null, 0, True, 2, now(),now());")
        mycursor.execute("insert into menu(item, price, size_id, description, spice_lvl, is_veg, category_id, create_time,update_time) VALUES('Blue Lagoon Mojito', 199, null, null, 0, True, 2, now(),now());")
        mycursor.execute("insert into menu(item, price, size_id, description, spice_lvl, is_veg, category_id, create_time,update_time) VALUES('Corn Cheese Balls', 349, null, null, 1, True, 3, now(),now());")
        mycursor.execute("insert into menu(item, price, size_id, description, spice_lvl, is_veg, category_id, create_time,update_time) VALUES('Potato Wedges', 199, null, null, 1, True, 3, now(),now());")
        mycursor.execute("insert into menu(item, price, size_id, description, spice_lvl, is_veg, category_id, create_time,update_time) VALUES('Peri Peri Fries', 299, null, null, 2, True, 3, now(),now());")
        mycursor.execute("insert into menu(item, price, size_id, description, spice_lvl, is_veg, category_id, create_time,update_time) VALUES('Merry Mellow Chicken Bites', 249, null, null, 3, False, 3, now(),now());")
        mycursor.execute("insert into menu(item, price, size_id, description, spice_lvl, is_veg, category_id, create_time,update_time) VALUES('White Italian Tomato Sandwich', 249, null, null, 1, True, 4, now(),now());")
        mycursor.execute("insert into menu(item, price, size_id, description, spice_lvl, is_veg, category_id, create_time,update_time) VALUES('Mexican Grilled Cheese Sandwich', 299, null, null, 2, True, 4, now(),now());")
        mycursor.execute("insert into menu(item, price, size_id, description, spice_lvl, is_veg, category_id, create_time,update_time) VALUES('Chicken Tikka Sandwich', 249, null, null, 3, False, 4, now(),now());")
        mycursor.execute("insert into menu(item, price, size_id, description, spice_lvl, is_veg, category_id, create_time,update_time) VALUES('Mutton Sheekh Sandwich', 299, null, null, 3, False, 4, now(),now());")
        mycursor.execute("insert into menu(item, price, size_id, description, spice_lvl, is_veg, category_id, create_time,update_time) VALUES('Tiramisu', 249, null, null, 0, True, 5, now(),now());")
        mycursor.execute("insert into menu(item, price, size_id, description, spice_lvl, is_veg, category_id, create_time,update_time) VALUES('Sizzling Chocolate Brownie', 299, null, null, 0, True, 5, now(),now());")
        mycursor.execute("insert into menu(item, price, size_id, description, spice_lvl, is_veg, category_id, create_time,update_time) VALUES('Cheesecake', 149, null, null, 0, True, 5, now(),now());")
        mycursor.execute("insert into menu(item, price, size_id, description, spice_lvl, is_veg, category_id, create_time,update_time) VALUES('Gelato Ice Cream', 149, null, null, 0, True, 5, now(),now());")
        mycursor.execute("insert into menu(item, price, size_id, description, spice_lvl, is_veg, category_id, create_time,update_time) VALUES('Oreo Cookies and Creme Donut', 149, null, null, 0, True, 6, now(),now());")
        mycursor.execute("insert into menu(item, price, size_id, description, spice_lvl, is_veg, category_id, create_time,update_time) VALUES('Glazed Blueberry Donut', 249, null, null, 0, True, 6, now(),now());")
        mycursor.execute("insert into menu(item, price, size_id, description, spice_lvl, is_veg, category_id, create_time,update_time) VALUES('Reeses Classic Donut', 249, null, null, 0, True, 6, now(),now());")
        mycursor.execute("insert into menu(item, price, size_id, description, spice_lvl, is_veg, category_id, create_time,update_time) VALUES('Chocolate Iced Raspberry Donut', 149, null, null, 0, True, 6, now(),now());")
        mycursor.execute("insert into menu(item, price, size_id, description, spice_lvl, is_veg, category_id, create_time,update_time) VALUES('Croissant', 99, null, null, 0, True, 7, now(),now());")
        mycursor.execute("insert into menu(item, price, size_id, description, spice_lvl, is_veg, category_id, create_time,update_time) VALUES('Bagel', 99, null, null, 0, True, 7, now(),now());")
        mycursor.execute("insert into menu(item, price, size_id, description, spice_lvl, is_veg, category_id, create_time,update_time) VALUES('Sunny side up', 149, null, null, 1, False, 7, now(),now());")
        mycursor.execute("insert into menu(item, price, size_id, description, spice_lvl, is_veg, category_id, create_time,update_time) VALUES('Bacon and Mushroom Peas', 249, null, null, 1, False, 7, now(),now());")
        mycursor.execute("insert into menu(item, price, size_id, description, spice_lvl, is_veg, category_id, create_time,update_time) VALUES('Hot N Sour Soup', 99, null, null, 1, True, 8, now(),now());")
        mycursor.execute("insert into menu(item, price, size_id, description, spice_lvl, is_veg, category_id, create_time,update_time) VALUES('Sweet Corn Soup', 99, null, null, 1, True, 8, now(),now());")
        mycursor.execute("insert into menu(item, price, size_id, description, spice_lvl, is_veg, category_id, create_time,update_time) VALUES('Cream of Mushroom Soup', 99, null, null, 0, True, 8, now(),now());")
        mycursor.execute("insert into menu(item, price, size_id, description, spice_lvl, is_veg, category_id, create_time,update_time) VALUES('Clear Chicken Soup', 99, null, null, 1, False, 8, now(),now());")
        mycursor.execute("insert into menu(item, price, size_id, description, spice_lvl, is_veg, category_id, create_time,update_time) VALUES('Veg Frankie', 199, null, null, 1, True, 9, now(),now());")
        mycursor.execute("insert into menu(item, price, size_id, description, spice_lvl, is_veg, category_id, create_time,update_time) VALUES('Chicken Frankie', 199, null, null, 2, False, 9, now(),now());")
        mycursor.execute("insert into menu(item, price, size_id, description, spice_lvl, is_veg, category_id, create_time,update_time) VALUES('Choco Chip Cookies', 99, null, null, 0, True, 9, now(),now());")
        mycursor.execute("insert into menu(item, price, size_id, description, spice_lvl, is_veg, category_id, create_time,update_time) VALUES('Spicy Chips', 99, null, null, 2, True, 9, now(),now());")
        mydb.commit()

        #cafe_table
        mycursor.execute("insert into cafe_table(cafe_table_number, no_of_seats, location, create_time,update_time) VALUES('Table 01', 2, '1st Floor, North East', now(),now());")
        mycursor.execute("insert into cafe_table(cafe_table_number, no_of_seats, location, create_time,update_time) VALUES('Table 02', 4, '1st Floor, South', now(),now());")
        mycursor.execute("insert into cafe_table(cafe_table_number, no_of_seats, location, create_time,update_time) VALUES('Table 03', 6, '1st Floor, Center', now(),now());")        
        mycursor.execute("insert into cafe_table(cafe_table_number, no_of_seats, location, create_time,update_time) VALUES('Table 04', 2, '2nd Floor, North East', now(),now());")
        mycursor.execute("insert into cafe_table(cafe_table_number, no_of_seats, location, create_time,update_time) VALUES('Table 05', 4, '2nd Floor, South', now(),now());")
        mycursor.execute("insert into cafe_table(cafe_table_number, no_of_seats, location, create_time,update_time) VALUES('Table 06', 6, '2nd Floor, Center', now(),now());")
        mycursor.execute("insert into cafe_table(cafe_table_number, no_of_seats, location, create_time,update_time) VALUES('Table 07', 2, '3rd Floor, North East', now(),now());")
        mycursor.execute("insert into cafe_table(cafe_table_number, no_of_seats, location, create_time,update_time) VALUES('Table 08', 4, '3rd Floor, South', now(),now());")
        mycursor.execute("insert into cafe_table(cafe_table_number, no_of_seats, location, create_time,update_time) VALUES('Table 09', 6, '3rd Floor, Center', now(),now());")
        mydb.commit()
            
    def customer_create(self, cust=Customer): 
        mydb = self.connect()        
        mycursor = mydb.cursor()
        
        sql = "insert into customer(customer_name,customer_phone_number, gender, email_id, DOB, DOA, create_time,update_time) VALUES (%s, %s, %s, %s, %s, %s, now(), now())"
        val = (cust.customer_name, cust.phone_number, cust.gender, cust.email_id, cust.DOB, cust.anniversary_date)
        
        mycursor.execute(sql, val)

        mydb.commit()
        print('customer created ')

    def customer_update(self, cust=Customer):
        mydb = self.connect()        
        mycursor = mydb.cursor()
        
        sql = "update customer set customer_name=%s,customer_phone_number=%s, gender=%s, email_id=%s, DOB=%s, DOA=%s, update_time=now() where customer_id=%s"
        val = (cust.customer_name, cust.phone_number, cust.gender, cust.email_id, cust.DOB, cust.anniversary_date, cust.customer_id)
        
        mycursor.execute(sql, val)

        mydb.commit()
        print('customer updated')

    def customer_delete(self, customer_id): 
        mydb = self.connect()        
        mycursor = mydb.cursor()
        
        sql = "delete from customer where customer_id=" + str(customer_id)
        
        mycursor.execute(sql)

        mydb.commit()
        print('customer updated')
        
    def bill_delete(self, bill_id): 
        mydb = self.connect()        
        mycursor = mydb.cursor()
        
        sql = "delete from bill where bill_id=" + str(bill_id)
        
        mycursor.execute(sql)

        mydb.commit()
        print('bill updated')
        
    def order_delete(self, cafe_order_header_id): 
        mydb = self.connect()        
        mycursor = mydb.cursor()
        
        sql = "delete from cafe_order_detail where cafe_order_header_id=" + str(cafe_order_header_id)
        
        mycursor.execute(sql)
        
        sql = "delete from cafe_order_header where cafe_order_header_id=" + str(cafe_order_header_id)
        
        mycursor.execute(sql)

        mydb.commit()
        print('order updated')

    def customer_get_all(self): 
        mydb = self.connect()
        mycursor = mydb.cursor()
        mycursor.execute("select customer_id, customer_name,customer_phone_number, gender, email_id, DOB, DOA, create_time,update_time from customer order by customer_id desc")
        
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

    def customer_get_by_id(self, customer_id): 
        mydb = self.connect()
        mycursor = mydb.cursor()
        mycursor.execute("select customer_id, customer_name,customer_phone_number, gender, email_id, DOB, DOA, create_time,update_time from customer where customer_id=" + str(customer_id))
        
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
        
    def order_header_create(self, ord=OrderHeader): 
        mydb = self.connect()        
        mycursor = mydb.cursor()

        sql = "insert into cafe_order_header(cafe_table_id, total_amount, create_time,update_time) VALUES (%s, %s, now(), now())"
        val = (ord.table_id, ord.total_amount)
        
        mycursor.execute(sql, val)
        
        mydb.commit()
        print('Order created ')
        return mycursor.lastrowid

    def order_header_update(self, ord=OrderHeader): 
        mydb = self.connect()        
        mycursor = mydb.cursor()

        sql = "update cafe_order_header set total_amount = %s, update_time=now() where cafe_order_header_id=%s"
        val = (ord.total_amount, ord.order_header_id)
        
        mycursor.execute(sql, val)
        
        mydb.commit()
        print('Order updated')
        return mycursor.lastrowid

    def order_detail_update(self, ord=OrderDetail): 
        mydb = self.connect()        
        mycursor = mydb.cursor()

        sql = "update cafe_order_detail set menu_id=%s, qty=%s, unit_price=%s, gst=%s, amount=%s, update_time=now() where cafe_order_detail_id = %s"
        val = (ord.item_id, ord.qty, ord.price, ord.gst, ord.amount, ord.order_detail_id)
        
        mycursor.execute(sql, val)
        
        mydb.commit()
        print('Order detail updated')

    def order_detail_create(self, ord=OrderDetail): 
        mydb = self.connect()        
        mycursor = mydb.cursor()

        sql = "insert into cafe_order_detail(cafe_order_header_id, menu_id, qty, unit_price, gst, amount, create_time,update_time) VALUES (%s, %s, %s, %s, %s, %s, now(), now())"
        val = (ord.order_header_id, ord.item_id, ord.qty, ord.price, ord.gst, ord.amount)
        
        mycursor.execute(sql, val)
        
        mydb.commit()
        print('Order created ')

    def order_header_get_all(self): 
        mydb = self.connect()
        mycursor = mydb.cursor()
        mycursor.execute("select cafe_order_header_id, c.cafe_table_id, cafe_table_number, total_amount, c.create_time from cafe_order_header c inner join cafe_table  t on c.cafe_table_id = t.cafe_table_id order by cafe_order_header_id desc")
        
        list = mycursor.fetchall()
        output_list = []
        for data in list:
            ord = OrderHeader()
            ord.order_header_id = data[0]
            ord.table_id = data[1]
            ord.table_number = data[2]
            ord.total_amount = data[3]
            ord.create_time = data[4]
            
            output_list.append(ord)
            print(f"|{ord.order_header_id:4}")
        
        return output_list

    def order_header_get_upaid(self): 
        mydb = self.connect()
        mycursor = mydb.cursor()
        mycursor.execute("""select c.cafe_order_header_id, c.cafe_table_id, cafe_table_number, total_amount, c.create_time 
                from cafe_order_header c 
                left outer join bill b on c.cafe_order_header_id = b.cafe_order_header_id
                inner join cafe_table  t on c.cafe_table_id = t.cafe_table_id 
                where b.bill_id is null
                order by cafe_order_header_id desc""")
        
        list = mycursor.fetchall()
        output_list = []
        for data in list:
            ord = OrderHeader()
            ord.order_header_id = data[0]
            ord.table_id = data[1]
            ord.table_number = data[2]
            ord.total_amount = data[3]
            ord.create_time = data[4]
            
            output_list.append(ord)
            print(f"|{ord.order_header_id:4}")
        
        return output_list

    def order_header_get_by_id(self, cafe_order_header_id): 
        mydb = self.connect()
        mycursor = mydb.cursor()

        sql = "select cafe_order_header_id, c.cafe_table_id, cafe_table_number, total_amount, c.create_time from cafe_order_header c inner join cafe_table  t on c.cafe_table_id = t.cafe_table_id where c.cafe_order_header_id = '" + str(cafe_order_header_id) + "' order by cafe_order_header_id desc"
        
        mycursor.execute(sql)
        
        list = mycursor.fetchall()
        output_list = []
        for data in list:
            ord = OrderHeader()
            ord.order_header_id = data[0]
            ord.table_id = data[1]
            ord.table_number = data[2]
            ord.total_amount = data[3]
            ord.create_time = data[4]
            
            output_list.append(ord)
            print(f"|{ord.order_header_id:4}")
        
        return output_list

    def order_detail_get_all(self): 
        mydb = self.connect()
        mycursor = mydb.cursor()
        mycursor.execute("select cafe_order_detail_id, cafe_order_header_id, c.cafe_table_id, cafe_table_number, c.menu_id, item, qty, unit_price, gst, amount, c.create_time from cafe_order_detail c inner join menu m on c.menu_id = m.menu_id inner join cafe_table  t on c.cafe_table_id = t.cafe_table_id order by cafe_order_detail_id")
        
        list = mycursor.fetchall()
        output_list = []
        for data in list:
            ord = OrderDetail()
            ord.cafe_order_detail_id = data[0]
            ord.cafe_order_header_id = data[1]
            ord.table_id = data[2]
            ord.table_number = data[3]
            ord.item_id = data[4]
            ord.item = data[5]
            ord.qty = data[6]
            ord.price = data[7]
            ord.gst = data[8]
            ord.amount = data[9]
            ord.create_time = data[10]
            
            output_list.append(ord)
            print(f"|{ord.cafe_order_detail_id:4}")
        
        return output_list

    def order_detail_get_by_id(self, cafe_order_header_id): 
        mydb = self.connect()
        mycursor = mydb.cursor()
        
        sql = "select c.cafe_order_detail_id, c.cafe_order_header_id, c.menu_id, item, qty, unit_price, gst, amount, c.create_time from cafe_order_detail c inner join menu m on c.menu_id = m.menu_id where c.cafe_order_header_id = '" + str(cafe_order_header_id) + "' order by c.cafe_order_detail_id"
        
        mycursor.execute(sql)
        
        list = mycursor.fetchall()
        output_list = []
        for data in list:
            ord = OrderDetail()
            ord.cafe_order_detail_id = data[0]
            ord.cafe_order_header_id = data[1]
            ord.item_id = data[2]
            ord.item = data[3]
            ord.qty = data[4]
            ord.price = data[5]
            ord.gst = data[6]
            ord.amount = data[7]
            ord.create_time = data[8]
            
            output_list.append(ord)
            print(f"|{ord.cafe_order_detail_id:4}")
        
        return output_list

    def order_detail_delete_by_id(self, cafe_order_header_id): 
        mydb = self.connect()
        mycursor = mydb.cursor()
        
        sql = "delete from cafe_order_detail where cafe_order_header_id = " + str(cafe_order_header_id)
        
        mycursor.execute(sql)
        mydb.commit()
        print('Order detail deleted:', cafe_order_header_id)

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
    
    def item_get_by_category_id(self, category_id): 
        mydb = self.connect()
        mycursor = mydb.cursor()
        mycursor.execute("select menu_id, item, price, description, spice_lvl, is_veg, m.category_id, category_name from menu m inner join category c on m.category_id = c.category_id where m.category_id=" + str(category_id))
        
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
        mycursor.execute("select reservation_id, r.no_of_seats, date_time, r.customer_id, customer_name, r.cafe_table_id, cafe_table_number from reservation r inner join customer c on r.customer_id = c.customer_id inner join cafe_table ct on r.cafe_table_id = ct.cafe_table_id order by reservation_id desc")
        
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

    def table_reservation_get_by_id(self, reservation_id): 
        mydb = self.connect()
        mycursor = mydb.cursor()
        mycursor.execute("select reservation_id, r.no_of_seats, date_time, r.customer_id, customer_name, r.cafe_table_id, cafe_table_number from reservation r inner join customer c on r.customer_id = c.customer_id inner join cafe_table ct on r.cafe_table_id = ct.cafe_table_id where reservation_id = " + str(reservation_id))
        
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

    def table_reservation_update(self, reserv=TableReservation): 
        mydb = self.connect()        
        mycursor = mydb.cursor()
        
        sql = "update reservation set no_of_seats=%s,date_time=%s, customer_id=%s, cafe_table_id=%s, update_time=now() where reservation_id=%s"
        val = (reserv.pax, reserv.datetime, reserv.customer_id, reserv.table_id, reserv.reservation_id)
        
        mycursor.execute(sql, val)
        
        mydb.commit()
        print('Table Reservation created ')

    def table_reservation_delete(self, reservation_id): 
        mydb = self.connect()        
        mycursor = mydb.cursor()
        
        sql = "delete from reservation where reservation_id=" + str(reservation_id)
        
        mycursor.execute(sql)
        
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
        
        sql = "insert into bill(cafe_order_header_id,discount,final_amount,customer_id, payment_mode_id, date_time, create_time,update_time) VALUES (%s, %s, %s, %s, %s, %s, now(), now())"
        val = (bill.cafe_order_header_id, bill.discount,bill.final_amount,bill.customer_id, bill.payment_mode_id, bill.datetime)
        
        mycursor.execute(sql, val)
        
        mydb.commit()
        print('Bill created ')

    def bill_update(self, bill=Bill): 
        mydb = self.connect()        
        mycursor = mydb.cursor()
        
        sql = "update bill set customer_id=%s, payment_mode_id=%s,discount=%s,final_amount=%s, update_time=now() where bill_id=%s"
        val = (bill.customer_id, bill.payment_mode_id, bill.discount,bill.final_amount,bill.bill_id)
        
        mycursor.execute(sql, val)
        
        mydb.commit()
        print('Bill created ')

    def bill_get_all(self): 
        mydb = self.connect()
        mycursor = mydb.cursor()
        mycursor.execute("""select b.bill_id, b.cafe_order_header_id, b.customer_id, c1.customer_name, b.payment_mode_id, p.payment_mode_name,b.discount,b.final_amount,b.date_time, c.cafe_table_id, c.cafe_table_number, ch.total_amount 
                from bill b 
                inner join cafe_order_header ch on b.cafe_order_header_id = ch.cafe_order_header_id
                inner join cafe_table c on ch.cafe_table_id = c.cafe_table_id 
                inner join customer c1 on b.customer_id = c1.customer_id 
                inner join payment_mode p on b.payment_mode_id = p.payment_mode_id
                order by b.bill_id desc
                """)
        
        list = mycursor.fetchall()
        output_list = []
        for data in list:
            bill = Bill()
            bill.bill_id = data[0]
            bill.cafe_order_header_id = data[1]            
            bill.customer_id = data[2]
            bill.customer = data[3]
            bill.payment_mode_id = data[4]
            bill.mode_of_payment = data[5]
            bill.discount = data[6]
            bill.final_amount = data[7]
            bill.datetime = data[8]
            bill.table_id = data[9]
            bill.table_number = data[10]
            bill.total_amount = data[11]
            
            output_list.append(bill)
            print(f"|{bill.bill_id:4}")
        
        return output_list
    
    def bill_get_by_id(self, bill_id): 
        mydb = self.connect()
        mycursor = mydb.cursor()
        mycursor.execute("""select b.bill_id, b.cafe_order_header_id, b.customer_id, c1.customer_name, b.payment_mode_id, p.payment_mode_name,b.discount,b.final_amount, b.date_time, c.cafe_table_id, c.cafe_table_number, ch.total_amount 
                from bill b 
                inner join cafe_order_header ch on b.cafe_order_header_id = ch.cafe_order_header_id
                inner join cafe_table c on ch.cafe_table_id = c.cafe_table_id 
                inner join customer c1 on b.customer_id = c1.customer_id 
                inner join payment_mode p on b.payment_mode_id = p.payment_mode_id
                where b.bill_id = """ + str(bill_id) +
                """ order by b.bill_id desc""")
        
        list = mycursor.fetchall()
        output_list = []
        for data in list:
            bill = Bill()
            bill.bill_id = data[0]
            bill.cafe_order_header_id = data[1]            
            bill.customer_id = data[2]
            bill.customer = data[3]
            bill.payment_mode_id = data[4]
            bill.mode_of_payment = data[5]
            bill.discount = data[6]
            bill.final_amount = data[7]
            bill.datetime = data[8]
            bill.table_id = data[9]
            bill.table_number = data[10]
            bill.total_amount = data[11]
            
            output_list.append(bill)
            print(f"|{bill.bill_id:4}")
        
        return output_list

    def bill_get_buy_order_header_id(self,cafe_order_header_id): 
        mydb = self.connect()
        mycursor = mydb.cursor()
        
        sql = "select bill_id from bill where cafe_order_header_id = "+str(cafe_order_header_id)
        mycursor.execute(sql)
        list = mycursor.fetchall()
        output_list = []
        for data in list:
            bill = Bill()
            bill.bill_id = data[0]
            
            output_list.append(bill)
            print(f"|{bill.bill_id:4}")
        
        return output_list

    def bill_get_buy_customer_id(self,customer_id): 
        mydb = self.connect()
        mycursor = mydb.cursor()
        
        sql = "select bill_id from bill where customer_id = "+str(customer_id)
        mycursor.execute(sql)
        list = mycursor.fetchall()
        output_list = []
        for data in list:
            bill = Bill()
            bill.bill_id = data[0]
            
            output_list.append(bill)
            print(f"|{bill.bill_id:4}")
        
        return output_list
    
    def category_get_all(self): 
        mydb = self.connect()
        mycursor = mydb.cursor()
        mycursor.execute("""select category_id, category_name from category order by category_id""")
        
        list = mycursor.fetchall()
        output_list = []
        for data in list:
            cat = Category()
            cat.category_id = data[0]
            cat.category_name = data[1]            
            
            output_list.append(cat)
            print(f"|{cat.category_id:4}")
        
        return output_list
