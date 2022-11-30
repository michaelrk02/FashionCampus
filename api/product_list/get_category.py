from flask import request

from sqlalchemy import select

from FashionCampus.database import session
from FashionCampus.model import Category

from FashionCampus.api.blueprints import product_list

@product_list.route('/categories', methods = ['GET'])
def product_list_get_category():
    db = session()

    categories = db.execute(select(Category).where(Category.is_deleted == False).order_by(Category.name)).scalars()

    return {
        'data': [
            {
                'id': str(c.id),
                'title': c.name
            } for c in categories
        ]
    }, 200
