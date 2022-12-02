import urllib.parse

from flask import request

from sqlalchemy import select

from FashionCampus.database import session
from FashionCampus.common import get_image_url
from FashionCampus.model import Category

from FashionCampus.api.blueprints import home

@home.route('/home/category', methods = ['GET'])
def home_get_category():
    db = session()

    categories = db.execute(select(Category).where(Category.is_deleted == False).order_by(Category.name)).scalars()

    return {
        'data': [
            {
                'id': str(c.id),
                'image': get_image_url('named?name=%s' % (urllib.parse.quote_plus('Category_%s' % (c.name)))),
                'title': c.name
            } for c in categories
        ]
    }, 200
