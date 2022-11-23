from flask import request

from FashionCampus.database import session
from FashionCampus.common import get_user

from FashionCampus.api.blueprints import profile_page

@profile_page.route('/user', methods = ['GET'])
def profile_page_user_details():
    db = session()

    user = get_user(db)
    if user == None:
        return {'message': 'unauthorized user'}, 401

    return {
        'name': user.name,
        'email': user.email,
        'phone_number': user.phone_number
    }, 200
