from sqlalchemy import delete

from FashionCampus.database import session
from FashionCampus.common import get_user
from FashionCampus.model import CartItem

from FashionCampus.api.blueprints import cart

@cart.route('/cart/<cart_id>', methods = ['DELETE'])
def cart_delete_cart_item(cart_id):
    db = session()

    user = get_user(db)
    if user == None:
        return {'message': 'unauthorized user'}, 401

    if user.type != 'buyer':
        return {'message': 'you are not a buyer'}, 403

    db.execute(delete(CartItem).where(CartItem.buyer_id == user.id, CartItem.id == cart_id))
    db.commit()

    return {'message': 'cart item deleted'}, 200
