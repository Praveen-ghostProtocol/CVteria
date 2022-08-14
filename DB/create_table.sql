-- Active: 1655650273149@@127.0.0.1@3306@cvteria

CREATE TABLE size(  
    size_id int NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT 'Primary Key',
    create_time DATETIME COMMENT 'Create Time',
    update_time DATETIME COMMENT 'Update Time',
    size_name VARCHAR(255)    
);

CREATE TABLE category(  
    category_id int NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT 'Primary Key',
    create_time DATETIME COMMENT 'Create Time',
    update_time DATETIME COMMENT 'Update Time',
    category_name VARCHAR(255)    
);

CREATE TABLE payment_mode(  
    payment_mode_id int NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT 'Primary Key',
    create_time DATETIME COMMENT 'Create Time',
    update_time DATETIME COMMENT 'Update Time',
    payment_mode_name VARCHAR(255)    
);

CREATE TABLE menu(  
    menu_id int NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT 'Primary Key',
    create_time DATETIME COMMENT 'Create Time',
    update_time DATETIME COMMENT 'Update Time',
    item VARCHAR(255),
    price FLOAT,
    image VARCHAR(255),
    size_id INT, INDEX size_id (size_id),CONSTRAINT fk_size_id FOREIGN KEY (size_id) REFERENCES size(size_id),
    description VARCHAR(255),
    spice_lvl INT,
    is_veg BOOLEAN,
    category_id INT, INDEX category_id (category_id),CONSTRAINT fk_category_id FOREIGN KEY (category_id) REFERENCES category(category_id)
);

CREATE TABLE cafe_table(  
    cafe_table_id int NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT 'Primary Key',
    create_time DATETIME COMMENT 'Create Time',
    update_time DATETIME COMMENT 'Update Time',
    no_of_seats INT,
    cafe_table_number VARCHAR(255),
    location VARCHAR(255)  
);

CREATE TABLE customer(  
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

CREATE TABLE reservation(  
    reservation_id int NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT 'Primary Key',
    create_time DATETIME COMMENT 'Create Time',
    update_time DATETIME COMMENT 'Update Time',
    no_of_seats INT,
    date_time DATETIME,
    customer_id INT, INDEX customer_id (customer_id),CONSTRAINT fk_customer_id FOREIGN KEY (customer_id) REFERENCES customer(customer_id),
    cafe_table_id INT, INDEX cafe_table_id (cafe_table_id),CONSTRAINT fk_cafe_table_id FOREIGN KEY (cafe_table_id) REFERENCES cafe_table(cafe_table_id)
);

CREATE TABLE cafe_order_header(  
    cafe_order_header_id int NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT 'Primary Key',
    create_time DATETIME COMMENT 'Create Time',
    update_time DATETIME COMMENT 'Update Time',
    cafe_table_id INT, INDEX cafe_table_id(cafe_table_id),CONSTRAINT fk_cafe_order_cafe_table_id FOREIGN KEY (cafe_table_id) REFERENCES cafe_table(cafe_table_id),
    total_amount FLOAT
);

CREATE TABLE cafe_order_detail(  
    cafe_order_detail_id int NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT 'Primary Key',
    cafe_order_header_id INT, INDEX cafe_order_header_id(cafe_order_header_id),CONSTRAINT fk_cafe_order_header_id FOREIGN KEY (cafe_order_header_id) REFERENCES cafe_order_header(cafe_order_header_id),
    create_time DATETIME COMMENT 'Create Time',
    update_time DATETIME COMMENT 'Update Time',
    menu_id INT, INDEX menu_id(menu_id),CONSTRAINT fk_cafe_order_menu_id FOREIGN KEY (menu_id) REFERENCES menu(menu_id),
    qty INT,
    unit_price float,
    gst float,
    amount FLOAT
);

CREATE TABLE bill(  
    bill_id int NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT 'Primary Key',
    cafe_order_header_id INT, INDEX cafe_order_header_id(cafe_order_header_id),CONSTRAINT fk_cafe_order_header_id FOREIGN KEY (cafe_order_header_id) REFERENCES cafe_order_header(cafe_order_header_id),
    create_time DATETIME COMMENT 'Create Time',
    update_time DATETIME COMMENT 'Update Time',
    customer_id INT, INDEX customer_id (customer_id),CONSTRAINT fk_bill_customer_id FOREIGN KEY (customer_id) REFERENCES customer(customer_id),
    payment_mode_id INT, INDEX payment_mode_id (payment_mode_id),CONSTRAINT fk_payment_mode_id FOREIGN KEY (payment_mode_id) REFERENCES payment_mode(payment_mode_id),
    date_time DATETIME
);

insert into size(size_name,create_time,update_time) VALUES('Demi',now(),now());
insert into size(size_name,create_time,update_time) VALUES('Short',now(),now());
insert into size(size_name,create_time,update_time) VALUES('Tall',now(),now());
insert into size(size_name,create_time,update_time) VALUES('Venti',now(),now());
insert into size(size_name,create_time,update_time) VALUES('Grande',now(),now());
insert into size(size_name,create_time,update_time) VALUES('Trenta',now(),now());

insert into category(category_name,create_time,update_time) VALUES('Starters',now(),now());
insert into category(category_name,create_time,update_time) VALUES('Main Course',now(),now());

insert into payment_mode(payment_mode_name,create_time,update_time) VALUES('Cash',now(),now());
insert into payment_mode(payment_mode_name,create_time,update_time) VALUES('Card',now(),now());
insert into payment_mode(payment_mode_name,create_time,update_time) VALUES('UPI',now(),now());

insert into menu(item, price, size_id, description, spice_lvl, is_veg, category_id, create_time,update_time) VALUES('Idli', 50, null, 'Idli or idly is a type of savoury rice cake', 0, True, 1, now(),now());
insert into menu(item, price, size_id, description, spice_lvl, is_veg, category_id, create_time,update_time) VALUES('Dosa', 100, null, null, 1, True, 1, now(),now());

insert into cafe_table(cafe_table_number, no_of_seats, location, create_time,update_time) VALUES('Table 01', 2, '1st Floor, North East', now(),now());
insert into cafe_table(cafe_table_number, no_of_seats, location, create_time,update_time) VALUES('Table 02', 4, '1st Floor, South', now(),now());
insert into cafe_table(cafe_table_number, no_of_seats, location, create_time,update_time) VALUES('Table 03', 6, '1st Floor, Center', now(),now());
	
SELECT * from size;