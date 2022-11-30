from flask import request

from FashionCampus.database import session
from FashionCampus.common import get_user
from FashionCampus.model import Seller

from FashionCampus.api.blueprints import admin_page

@admin_page.route('/sales', methods = ['GET'])
def admin_page_get_total_sales():
    db = session()

    user = get_user(db)
    if user == None:
        return {'message': 'unauthorized user'}, 401

    seller = db.get(Seller, user.id)
    if seller == None:
        return {'message': 'you are not a seller'}, 403

    return {'total': seller.sales}, 200
