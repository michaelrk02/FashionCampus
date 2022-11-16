from sqlalchemy import Column, String
from sqlalchemy.schema import FetchedValue

from .model import Model

class Category(Model):
    __tablename__ = 'category'
    id = Column('id', String(36), primary_key = True, autoincrement = False, server_default = FetchedValue())
    name = Column('name', String(128), nullable = False)
