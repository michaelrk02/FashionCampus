import enum

from sqlalchemy.orm import declarative_base

Model = declarative_base()

class UserType(str, enum.Enum):
    seller = 'seller'
    buyer = 'buyer'

class ProductSize(str, enum.Enum):
    s = 's'
    m = 'm'
    l = 'l'
    xl = 'xl'

class ProductCondition(str, enum.Enum):
    new = 'new'
    used = 'used'

class ShippingMethod(str, enum.Enum):
    regular = 'regular'
    next_day = 'next_day'

def enum_describe(value):
    return ' '.join(value.split('_'))

def enum_make(value):
    return '_'.join(value.split(' '))
