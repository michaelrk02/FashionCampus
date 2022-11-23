import random

from sqlalchemy import select
from faker import Faker

from FashionCampus.model import CartItem, Order, OrderItem

def add_to_cart(db, buyer_id, product_id):
    item = db.execute(select(CartItem).where(CartItem.buyer_id == buyer_id, CartItem.product_id == product_id)).fetchone()
    if item != None:
        return

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
    order_gross = 0;
    for product_id in product_ids:
        quantity = random.randint(1, 5)

        item = {
            'product_id': product_id,
            'details_quantity': quantity,
            'details_size': random.choice(['s', 'm', 'l', 'xl']),
            'product_price': quantity * random.randint(50000, 150000)
        }
        order_items.append(item)
        order_gross += item['product_price']

    shipping_price = random.randint(20000, 50000)
    order_total = order_gross + shipping_price

    order = Order(
        buyer_id = buyer_id,
        created_at = fake.date_time_between('-1y'),
        gross = order_gross,
        shipping_method = random.choice(['regular', 'next_day']),
        shipping_address = {
            'name': fake.name(),
            'phone_number': fake.phone_number(),
            'address': fake.address(),
            'city': fake.city()
        },
        shipping_price = shipping_price,
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
