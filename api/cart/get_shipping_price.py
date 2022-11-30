from FashionCampus.database import session
from FashionCampus.common import get_gross_amount, get_shipping_price, get_user
from FashionCampus.model import ShippingMethod, enum_describe

from FashionCampus.api.blueprints import cart

@cart.route('/shipping_price', methods = ['GET'])
def cart_get_shipping_price():
    db = session()

    user = get_user(db)
    if user == None:
        return {'message': 'unauthorized user'}, 401

    if user.type != 'buyer':
        return {'message': 'you are not a buyer'}, 403

    gross_amount = get_gross_amount(db, user.id)

    return {
        'data': [
            {
                'name': enum_describe(method),
                'price': get_shipping_price(method, gross_amount)
            } for method in [ShippingMethod.regular, ShippingMethod.next_day]
        ]
    }, 200
