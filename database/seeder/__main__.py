import random

from FashionCampus.database import session
from FashionCampus.model import Buyer, CartItem, Category, Order, OrderItem, Product, ProductImage, Seller, User

from .user import create_user
from .product import create_category, create_product
from .order import add_to_cart, create_order

print('Seeding database ...')

db = session()

#
# Reset all tables
#

print('Resetting all tables ...')

db.query(OrderItem).delete()
db.query(Order).delete()
db.query(CartItem).delete()
db.query(Buyer).delete()
db.query(ProductImage).delete()
db.query(Product).delete()
db.query(Category).delete()
db.query(Seller).delete()
db.query(User).delete()

#
# Seed users
#

print('Generating users ...')

create_user(db, 'seller')

for _ in range(4):
    create_user(db, 'buyer')

#
# Seed products
#

print('Generating products ...')

for _ in range(4):
    create_category(db)

sellers = db.query(Seller).all()
categories = db.query(Category).all()

for s in sellers:
    create_product(db, s.user_id, random.choice(categories).id, False)
    for _ in range(7):
        create_product(db, s.user_id, random.choice(categories).id, True)

#
# Seed orders
#

print('Generating orders ...')

buyers = db.query(Buyer).all()
products = db.query(Product).all()

for b in buyers:
    add_to_cart(db, b.user_id, random.choice(products).id)

    for _ in range(1, 10):
        create_order(db, b.user_id, [p.id for p in random.sample(products, random.randint(1, 5))])

print('Database seeding completed')
