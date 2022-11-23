from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.types import JSON
from sqlalchemy.schema import FetchedValue
from sqlalchemy.orm import relationship

from .model import Model, ProductSize, ShippingMethod

class CartItem(Model):
    __tablename__ = 'cart_item'

    id = Column('id', String(36), primary_key = True, autoincrement = False, server_default = FetchedValue())
    buyer_id = Column('buyer_id', String(36), ForeignKey('buyer.user_id'), nullable = False)
    product_id = Column('product_id', String(36), ForeignKey('product.id'), nullable = False)
    details_quantity = Column('details_quantity', Integer, nullable = False)
    details_size = Column('details_size', Enum(ProductSize), nullable = False)

    buyer = relationship('Buyer', back_populates = 'cart_items')
    product = relationship('Product')

    __table_args__ = (
        UniqueConstraint('buyer_id', 'product_id'),
    )

class Order(Model):
    __tablename__ = 'order'

    id = Column('id', String(36), primary_key = True, autoincrement = False, server_default = FetchedValue())
    buyer_id = Column('buyer_id', String(36), ForeignKey('buyer.user_id'), nullable = False)
    created_at = Column('created_at', DateTime, nullable = False, server_default = FetchedValue())
    gross = Column('gross', Integer, nullable = False)
    shipping_method = Column('shipping_method', Enum(ShippingMethod), nullable = False)
    shipping_address = Column('shipping_address', JSON, nullable = False)
    shipping_price = Column('shipping_price', Integer, nullable = False)
    total = Column('total', Integer, nullable = False)

    buyer = relationship('Buyer', back_populates = 'orders')
    items = relationship('OrderItem', back_populates = 'order')

class OrderItem(Model):
    __tablename__ = 'order_item'

    order_id = Column('order_id', String(36), ForeignKey('order.id'), primary_key = True, autoincrement = False)
    product_id = Column('product_id', String(36), ForeignKey('product.id'), primary_key = True, autoincrement = False)
    details_quantity = Column('details_quantity', Integer, nullable = False)
    details_size = Column('details_size', Enum(ProductSize), nullable = False)
    product_price = Column('product_price', Integer, nullable = False)

    order = relationship('Order', back_populates = 'items')
    product = relationship('Product')
