from flask import request

from sqlalchemy import select

from FashionCampus.database import session
from FashionCampus.common import get_user
from FashionCampus.model import CartItem, Product, ProductSize

from FashionCampus.api.blueprints import product_detail_page

@product_detail_page.route('/cart', methods = ['POST'])
def product_detail_page_add_to_cart():
    db = session()

    user = get_user(db)
    if user == None:
        return {'message': 'unauthorized user'}, 401

    if user.type != 'buyer':
        return {'message': 'you are not a buyer'}, 403

    product_id = request.json.get('id', '')
    quantity = int(request.json.get('quantity', 0))
    size = request.json.get('size', '')

    if product_id == '':
        return {'message': 'item product ID must be given'}, 400

    if quantity <= 0:
        return {'message': 'quantity must be a positive integer'}, 400

    if not hasattr(ProductSize, size):
        return {'message': 'invalid product size'}, 400

    product = db.execute(select(Product).where(Product.id == product_id, Product.is_deleted == False)).scalar()
    if product == None:
        return {'message': 'product not found'}, 404

    cart_item = db.execute(select(CartItem).where(CartItem.buyer_id == user.id, CartItem.product_id == product_id, CartItem.details_size == size)).scalar()
    if cart_item == None:
        cart_item = CartItem(
            buyer_id = user.id,
            product_id = product_id,
            details_quantity = quantity,
            details_size = size
        )
    else:
        cart_item.details_quantity += quantity

    db.add(cart_item)
    db.commit()

    return {'message': 'item added to cart'}, 200
