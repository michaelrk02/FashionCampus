from sqlalchemy import Boolean, Column, String
from sqlalchemy.schema import FetchedValue

from .model import Model

class Category(Model):
    __tablename__ = 'category'

    id = Column('id', String(36), primary_key = True, autoincrement = False, server_default = FetchedValue())
    name = Column('name', String(128), nullable = False)
    is_deleted = Column('is_deleted', Boolean, nullable = False, server_default = FetchedValue())
