from sqlalchemy import Boolean, Column, Enum, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.schema import FetchedValue
from sqlalchemy.orm import relationship

from .model import Model, ProductCondition

class Product(Model):
    __tablename__ = 'product'

    id = Column('id', String(36), primary_key = True, autoincrement = False, server_default = FetchedValue())
    seller_id = Column('seller_id', String(36), ForeignKey('seller.user_id'), nullable = False)
    category_id = Column('category_id', String(36), ForeignKey('category.id'), nullable = False)
    name = Column('name', String(128), nullable = False)
    description = Column('description', Text, nullable = False)
    condition = Column('condition', Enum(ProductCondition), nullable = False)
    price = Column('price', Integer, nullable = False)
    is_deleted = Column('is_deleted', Boolean, nullable = False, server_default = FetchedValue())

    seller = relationship('Seller')
    category = relationship('Category')
    images = relationship('ProductImage')

    __table_args__ = (
        UniqueConstraint('name', 'category_id', 'condition'),
    )

class ProductImage(Model):
    __tablename__ = 'product_image'

    product_id = Column('product_id', String(36), ForeignKey('product.id'), primary_key = True, autoincrement = False)
    image_id = Column('image_id', String(36), primary_key = True, autoincrement = False, server_default = FetchedValue())
    order = Column('order', Integer, nullable = False)
    path = Column('path', Text, nullable = False)
