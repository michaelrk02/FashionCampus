import os
import jwt
import time

from flask import request
from sqlalchemy import select

from FashionCampus.api.blueprints import authentication

from FashionCampus.database import session
from FashionCampus.common import password_check
from FashionCampus.model import User

@authentication.route('/sign-in', methods = ['POST'])
def authentication_signin():
    db = session()

    email = request.json.get('email')
    password = request.json.get('password')

    if email == None:
        return {'message': 'email must be given'}, 400

    if password == None:
        return {'message': 'password must be given'}, 400

    user = db.execute(select(User).where(User.email == email)).scalar()
    if user == None:
        return {'message': 'user with specified e-mail does not exist'}, 404

    if not password_check(password, user.password_hash, user.password_salt):
        return {'message': 'invalid password for the specified user'}, 401

    token = jwt.encode(
        {
            'sub': str(user.id),
            'exp': int(time.time()) + 86400
        },
        os.getenv('APP_KEY'),
        algorithm = 'HS256'
    )

    return {
        'user_information': {
            'name': user.name,
            'email': user.email,
            'phone_number': user.phone_number,
            'type': user.type
        },
        'token': token,
        'message': 'login success'
    }, 200
