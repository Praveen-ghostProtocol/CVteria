from datetime import datetime

class Bill():
    def __init__(self):
        print('Bill')

    bill_id = 0
    cafe_order_header_id=0
    payment_mode_id = 0
    mode_of_payment = 'cash'
    datetime = datetime.now()
    customer_id = 0
    customer = ''
    table_id = 0
    table_number = ''
    total_amount=0
    discount = 0
    final_amount = 0
