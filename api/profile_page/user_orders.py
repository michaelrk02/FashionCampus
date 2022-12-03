from flask import request

from sqlalchemy import select

from FashionCampus.database import session
from FashionCampus.common import get_image_url, get_user
from FashionCampus.model import Order, OrderItem, Product, ProductImage, enum_describe

from FashionCampus.api.blueprints import profile_page

@profile_page.route('/user/order', methods = ['GET'])
def profile_page_user_orders():
    db = session()

    user = get_user(db)
    if user == None:
        return {'message': 'unauthorized user'}, 401

    orders = db.execute(select(Order).where(Order.buyer_id == user.id).order_by(Order.created_at.desc())).scalars().all()

    order_items = {}
    for order in orders:
        items = db.execute(
            select(
                OrderItem.product_id,
                OrderItem.details_quantity,
                OrderItem.details_size,
                OrderItem.product_price,
                ProductImage.path.label('product_image_path'),
                Product.name.label('product_name')
            ).
            join(OrderItem.product).
            join(Product.images.and_(ProductImage.order == 1), isouter = True).
            where(OrderItem.order_id == order.id)
        ).fetchall()

        order_items[order.id] = [
            {
                'id': str(item.product_id),
                'details': {
                    'quantity': item.details_quantity,
                    'size': item.details_size
                },
                'price': item.product_price,
                'image': get_image_url(item.product_image_path),
                'name': item.product_name
            } for item in items
        ]

    return {
        'data': [
            {
                'id': order.id,
                'created_at': order.created_at,
                'products': order_items[order.id],
                'shipping_method': enum_describe(order.shipping_method),
                'shipping_address': order.shipping_address
            } for order in orders
        ]
    }, 200
