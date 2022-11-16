import random

from faker import Faker

from FashionCampus.model import CartItem, Order, OrderItem

def add_to_cart(db, buyer_id, product_id):
    item = CartItem(
        buyer_id = buyer_id,
        product_id = product_id,
        details_quantity = random.randint(1, 5),
        details_size = random.choice(['s', 'm', 'l', 'xl'])
    )

    db.add(item)
    db.commit()

def create_order(db, buyer_id, product_ids):
    fake = Faker()

    order_items = []
    order_total = 0;
    for product_id in product_ids:
        item = {
            'product_id': product_id,
            'details_quantity': random.randint(1, 5),
            'details_size': random.choice(['s', 'm', 'l', 'xl']),
            'product_price': random.randint(50000, 150000)
        }
        order_items.append(item)
        order_total += item['product_price'] * item['details_quantity']

    order = Order(
        buyer_id = buyer_id,
        created_at = fake.date_time_between('-1y'),
        shipping_method = random.choice(['regular', 'next_day']),
        shipping_address = {
            'name': fake.name(),
            'phone_number': fake.phone_number(),
            'address': fake.address(),
            'city': fake.city()
        },
        total = order_total
    )

    db.add(order)
    db.commit()

    for item_values in order_items:
        item = OrderItem(
            order_id = order.id,
            product_id = item_values['product_id'],
            details_quantity = item_values['details_quantity'],
            details_size = item_values['details_size'],
            product_price = item_values['product_price']
        )

        db.add(item)
        db.commit()
