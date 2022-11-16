import enum

from sqlalchemy.orm import declarative_base

Model = declarative_base()

class UserType(enum.Enum):
    seller = 'seller'
    buyer = 'buyer'

class ProductSize(enum.Enum):
    s = 's'
    m = 'm'
    l = 'l'
    xl = 'xl'

class ProductCondition(enum.Enum):
    old = 'old'
    new = 'new'

class ShippingMethod(enum.Enum):
    regular = 'regular'
    next_day = 'next_day'

def enum_describe(value):
    return ' '.join(value.split('_')).capitalize()
