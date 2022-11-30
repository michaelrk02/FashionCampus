from flask import request

from sqlalchemy import select

from FashionCampus.database import session
from FashionCampus.common import get_user
from FashionCampus.model import Buyer, Order, User

from FashionCampus.api.blueprints import admin_page

@admin_page.route('/orders', methods = ['GET'])
def admin_page_get_orders():
    db = session()

    user = get_user(db)
    if user == None:
        return {'message': 'unauthorized user'}, 401

    if user.type != 'seller':
        return {'message': 'you are not a seller'}, 403

    sort_by = request.args.get('sort_by', '')
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 15))

    stmt = select(
        Order.id,
        User.name.label('user_name'),
        Order.created_at,
        User.id.label('user_id'),
        User.email.label('user_email'),
        Order.total
    ).select_from(Order).join(Order.buyer).join(Buyer.user).limit(page_size).offset((page - 1) * page_size)

    if sort_by == '':
        stmt = stmt.order_by(Order.created_at.desc())
    elif sort_by == 'Price a_z':
        stmt = stmt.order_by(Order.total.asc())
    elif sort_by == 'Price z_a':
        stmt = stmt.order_by(Order.total.desc())

    orders = db.execute(stmt).fetchall()

    return {
        'data': [
            {
                'id': order.id,
                'user_name': order.user_name,
                'created_at': order.created_at,
                'user_id': order.user_id,
                'user_email': order.user_email,
                'total': order.total
            } for order in orders
        ]
    }, 200
