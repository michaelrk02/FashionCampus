import re

from flask import request

from FashionCampus.api.blueprints import authentication

from FashionCampus.database import session
from FashionCampus.common import password_make
from FashionCampus.model import User, Buyer

@authentication.route('/sign-up', methods = ['POST'])
def authentication_signup():
    db = session()

    name = request.json.get('name', '')
    email = request.json.get('email', '')
    phone_number = request.json.get('phone_number', '')
    password = request.json.get('password', '')

    if name == '':
        return {'message': 'name must be given'}, 400

    if email == '':
        return {'message': 'email must be given'}, 400

    if not re.match('^[a-zA-Z0-9_\-\.]+@[a-zA-Z0-9_\-\.]+$', email):
        return {'message': 'email must be valid'}, 400

    if phone_number == '':
        return {'message': 'phone number must be given'}, 400

    if not re.match('^[0-9+()\-\s]+$', phone_number):
        return {'message': 'phone number must be valid'}, 400

    if password == '':
        return {'message': 'password must be given'}, 400

    if len(password) < 8:
        return {'message': 'password must be at least 8 characters'}, 400

    if not re.search('[a-z]', password):
        return {'message': 'password should contain a lowercase character'}, 400

    if not re.search('[A-Z]', password):
        return {'message': 'password should contain an uppercase character'}, 400

    if not re.search('[0-9]', password):
        return {'message': 'password should contain a number'}, 400

    password_hash, password_salt = password_make(password)

    user = User(
        name = name,
        email = email,
        password_hash = password_hash,
        password_salt = password_salt,
        phone_number = phone_number,
        type = 'buyer'
    )

    db.add(user)
    db.commit()

    buyer = Buyer(
        user_id = user.id,
        shipping_address = {
            'name': name,
            'phone_number': phone_number,
            'address': '',
            'city': ''
        }
    )

    db.add(buyer)
    db.commit()

    return {'message': 'success, user created'}, 200
