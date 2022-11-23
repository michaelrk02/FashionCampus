from flask import request

from FashionCampus.database import session
from FashionCampus.common import check_address, get_user
from FashionCampus.model import Buyer

from FashionCampus.api.blueprints import profile_page

@profile_page.route('/user/shipping_address', methods = ['POST'])
def profile_page_change_shipping_address():
    db = session()

    user = get_user(db)
    if user == None:
        return {'message': 'unauthorized user'}, 401

    buyer = db.get(Buyer, user.id)
    if buyer == None:
        return {'message': 'you are not a buyer'}, 403

    name = request.json.get('name', '')
    phone_number = request.json.get('phone_number', '')
    address = request.json.get('address', '')
    city = request.json.get('city', '')

    err = check_address(name, phone_number, address, city)
    if err != None:
        return {'message': err}, 400

    buyer.shipping_address = {
        'name': name,
        'phone_number': phone_number,
        'address': address,
        'city': city
    }
    db.add(buyer)
    db.commit()

    return {'message': 'address successfully changed'}, 200
