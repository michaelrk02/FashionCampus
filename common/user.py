import os
import jwt
import re

from sqlalchemy import select

from flask import request

from FashionCampus.model import User

def get_user(db):
    token = request.headers.get('Authentication')
    if token == None:
        return None

    try:
        claims = jwt.decode(token, os.getenv('APP_KEY'), algorithms = ['HS256'])

        user = db.get(User, claims['sub'])

        return user
    except:
        return None

    return None

def check_address(name, phone_number, address, city):
    if name == '':
        return 'address name must be given'

    if phone_number == '':
        return 'address phone number must be given'

    if not re.match('^[0-9+()\-\s]+$', phone_number):
        return 'address phone number must be a valid format'

    if address == '':
        return 'address line must be given'

    if city == '':
        return 'address city must be given'

    return None
