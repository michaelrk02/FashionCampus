from faker import Faker

from FashionCampus.model import User, Seller, Buyer
from FashionCampus.common import password_make

def create_user(db, type):
    fake = Faker()

    password_hash, password_salt = password_make('password')

    parent = User(
        name = fake.name(),
        email = fake.safe_email(),
        password_hash = password_hash,
        password_salt = password_salt,
        phone_number = fake.phone_number(),
        type = type
    )

    db.add(parent)
    db.commit()

    child = None
    if type == 'seller':
        child = Seller(
            user_id = parent.id
        )
    elif type == 'buyer':
        child = Buyer(
            user_id = parent.id,
            shipping_address = {
                'name': fake.name(),
                'phone_number': fake.phone_number(),
                'address': fake.address(),
                'city': fake.city()
            }
        )

    db.add(child)
    db.commit()
