from sqlalchemy import Column, Enum, ForeignKey, Integer, String
from sqlalchemy.types import JSON
from sqlalchemy.schema import FetchedValue

from .model import Model, UserType

class User(Model):
    __tablename__ = 'user'
    id = Column('id', String(36), primary_key = True, autoincrement = False, server_default = FetchedValue())
    name = Column('name', String(128), nullable = False)
    email = Column('email', String(254), nullable = False)
    password_hash = Column('password_hash', String(64), nullable = False)
    password_salt = Column('password_salt', String(16), nullable = False)
    type = Column('type', Enum(UserType), nullable = False)

class Seller(Model):
    __tablename__ = 'seller'
    user_id = Column('user_id', String(36), ForeignKey('user.id'), primary_key = True, nullable = False)
    sales = Column('sales', Integer, nullable = False, server_default = FetchedValue())

class Buyer(Model):
    __tablename__ = 'buyer'
    user_id = Column('user_id', String(36), ForeignKey('user.id'), primary_key = True, autoincrement = False)
    shipping_address = Column('shipping_address', JSON, nullable = False)
    balance = Column('balance', Integer, nullable = False, server_default = FetchedValue())
