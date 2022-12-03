from flask import request

from FashionCampus.database import session
from FashionCampus.common import check_address, get_user
from FashionCampus.model import Buyer

from FashionCampus.api.blueprints import profile_page

@profile_page.route('/user/balance', methods = ['POST'])
def profile_page_topup_balance():
    db = session()

    user = get_user(db)
    if user == None:
        return {'message': 'unauthorized user'}, 401

    buyer = db.get(Buyer, user.id)
    if buyer == None:
        return {'message': 'you are not a buyer'}, 403

    amount = int(request.json.get('amount', 0))
    if amount <= 0:
        return {'message': 'amount must be a positive integer'}, 400

    buyer.balance = buyer.balance + amount
    db.add(buyer)
    db.commit()

    return {'message': 'balance topped-up successfully'}, 200
