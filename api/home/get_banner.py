import urllib.parse

from flask import request

from sqlalchemy import select

from FashionCampus.database import session
from FashionCampus.common import get_image_url
from FashionCampus.model import Product, ProductImage

from FashionCampus.api.blueprints import home

@home.route('/home/banner', methods = ['GET'])
def home_get_banner():
    db = session()

    products = db.execute(select(
        Product.id,
        Product.name,
        ProductImage.path.label('image_path')
    ).join(Product.images.and_(ProductImage.order == 1), isouter = True).where(Product.is_deleted == False).order_by(Product.created_at.desc()).limit(5)).fetchall()

    return {
        'data': [
            {
                'id': str(p.id),
                'image': get_image_url(p.image_path),
                'title': p.name
            } for p in products
        ]
    }, 200
