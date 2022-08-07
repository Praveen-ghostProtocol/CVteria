from datetime import datetime

class Bill():
    def __init__(self):
        print('Bill')

    bill_id = 1
    table_id = 0
    table_number = 'dummy'
    total_price = 100
    discount = 10
    payment_mode_id = 1
    mode_of_payment = 'cash'
    datetime = datetime.now
    customer_id = 1
    customer = ''
