from sqlalchemy import Column, Enum, ForeignKey, Integer, String
from sqlalchemy.types import JSON
from sqlalchemy.schema import FetchedValue
from sqlalchemy.orm import relationship

from .model import Model, UserType

class User(Model):
    __tablename__ = 'user'

    id = Column('id', String(36), primary_key = True, autoincrement = False, server_default = FetchedValue())
    name = Column('name', String(128), nullable = False)
    email = Column('email', String(254), nullable = False)
    password_hash = Column('password_hash', String(64), nullable = False)
    password_salt = Column('password_salt', String(16), nullable = False)
    phone_number = Column('phone_number', String(24), nullable = False)
    type = Column('type', Enum(UserType), nullable = False)

    seller = relationship('Seller', back_populates = 'user')
    buyer = relationship('Buyer', back_populates = 'user')

class Seller(Model):
    __tablename__ = 'seller'

    user_id = Column('user_id', String(36), ForeignKey('user.id'), primary_key = True, nullable = False)
    sales = Column('sales', Integer, nullable = False, server_default = FetchedValue())

    user = relationship('User', back_populates = 'seller')

class Buyer(Model):
    __tablename__ = 'buyer'

    user_id = Column('user_id', String(36), ForeignKey('user.id'), primary_key = True, autoincrement = False)
    shipping_address = Column('shipping_address', JSON, nullable = False)
    balance = Column('balance', Integer, nullable = False, server_default = FetchedValue())

    user = relationship('User', back_populates = 'buyer')
    cart_items = relationship('CartItem', back_populates = 'buyer')
    orders = relationship('Order', back_populates = 'buyer')
