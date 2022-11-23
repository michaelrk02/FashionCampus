from flask import request

from FashionCampus.database import session
from FashionCampus.common import get_user
from FashionCampus.model import Buyer

from FashionCampus.api.blueprints import profile_page

@profile_page.route('/user/balance', methods = ['GET'])
def profile_page_get_user_balance():
    db = session()

    user = get_user(db)
    if user == None:
        return {'message': 'unauthorized user'}, 401

    buyer = db.get(Buyer, user.id)
    if buyer == None:
        return {'message': 'you are not a buyer'}, 403

    return {'balance': buyer.balance}, 200
