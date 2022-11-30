from flask import request

from sqlalchemy import delete, select

from FashionCampus.database import session
from FashionCampus.common import check_address, get_gross_amount, get_shipping_price, get_user
from FashionCampus.model import Buyer, CartItem, Order, OrderItem, Product, Seller, ShippingMethod

from FashionCampus.api.blueprints import cart

@cart.route('/order', methods = ['POST'])
def cart_create_order():
    db = session()

    user = get_user(db)
    if user == None:
        return {'message': 'unauthorized user'}, 401

    buyer = db.get(Buyer, user.id)
    if buyer == None:
        return {'message': 'you are not a buyer'}, 403

    shipping_method = '_'.join(request.json.get('shipping_method', '').lower().split(' '))
    shipping_address = request.json.get('shipping_address')

    if not hasattr(ShippingMethod, shipping_method):
        return {'message': 'invalid shipping method'}, 400

    if shipping_address == None:
        return {'message': 'shipping address must be given'}, 400

    err = check_address(
        shipping_address.get('name', ''),
        shipping_address.get('phone_number', ''),
        shipping_address.get('address', ''),
        shipping_address.get('city', '')
    )
    if err != None:
        return {'message': 'shipping address: %s' % (err)}, 400

    gross_amount = get_gross_amount(db, buyer.user_id)
    shipping_price = get_shipping_price(shipping_method, gross_amount)
    grand_total = gross_amount + shipping_price

    if buyer.balance < grand_total:
        return {'message': 'insufficient balance'}, 403

    order = Order(
        buyer_id = buyer.user_id,
        gross = gross_amount,
        shipping_method = shipping_method,
        shipping_address = shipping_address,
        shipping_price = shipping_price,
        total = grand_total
    )

    db.add(order)
    db.commit()

    cart_items = db.execute(select(
        CartItem.product_id,
        CartItem.details_quantity,
        CartItem.details_size,
        Product.price.label('product_price'),
        Product.seller_id.label('product_seller_id')
    ).join(CartItem.product).where(CartItem.buyer_id == buyer.user_id)).fetchall()

    for cart_item in cart_items:
        order_item = OrderItem(
            order_id = order.id,
            product_id = cart_item.product_id,
            details_quantity = cart_item.details_quantity,
            details_size = cart_item.details_size,
            product_price = cart_item.details_quantity * cart_item.product_price
        )

        db.add(order_item)
        db.commit()

        seller = db.get(Seller, cart_item.product_seller_id)
        seller.sales += order_item.product_price
        db.add(seller)
        db.commit()

    db.execute(delete(CartItem).where(CartItem.buyer_id == buyer.user_id))
    db.commit()

    buyer.balance -= grand_total

    db.add(buyer)
    db.commit()

    return {'message': 'order has been created'}, 201
