from sqlalchemy import Column, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.schema import FetchedValue

from .model import Model, ProductCondition

class Product(Model):
    __tablename__ = 'product'
    id = Column('id', String(36), primary_key = True, autoincrement = False, server_default = FetchedValue())
    seller_id = Column('seller_id', String(36), ForeignKey('user.id'), nullable = False)
    category_id = Column('category_id', String(36), ForeignKey('category.id'), nullable = False)
    name = Column('name', String(128), nullable = False)
    description = Column('description', Text, nullable = False)
    condition = Column('condition', Enum(ProductCondition), nullable = False)
    price = Column('price', Integer, nullable = False)

class ProductImage(Model):
    __tablename__ = 'product_image'
    product_id = Column('product_id', String(36), ForeignKey('product.id'), primary_key = True, autoincrement = False)
    image_id = Column('image_id', String(36), primary_key = True, autoincrement = False, server_default = FetchedValue())
    order = Column('order', Integer, nullable = False)
    path = Column('path', Text, nullable = False)
