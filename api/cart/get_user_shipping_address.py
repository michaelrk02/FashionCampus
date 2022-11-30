from flask import request

from FashionCampus.database import session
from FashionCampus.common import get_user
from FashionCampus.model import Buyer

from FashionCampus.api.blueprints import cart

@cart.route('/user/shipping_address', methods = ['GET'])
def cart_get_user_shipping_address():
    db = session()

    user = get_user(db)
    if user == None:
        return {'message': 'unauthorized user'}, 401

    buyer = db.get(Buyer, user.id)
    if buyer == None:
        return {'message': 'you are not a buyer'}, 403

    return {
        'id': user.id,
        'name': buyer.shipping_address['name'],
        'phone_number': buyer.shipping_address['phone_number'],
        'address': buyer.shipping_address['address'],
        'city': buyer.shipping_address['city']
    }, 200
