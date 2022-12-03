from flask import request

from sqlalchemy import select

from FashionCampus.common import get_image_url
from FashionCampus.database import session
from FashionCampus.model import Category, Product, ProductImage

from FashionCampus.api.blueprints import product_detail_page

@product_detail_page.route('/products/<product_id>', methods = ['GET'])
def product_detail_page_get_product_details(product_id):
    db = session()

    product = db.execute(select(
        Product.id,
        Product.name,
        Product.description,
        Product.price,
        Product.category_id,
        Category.name.label('category_name')
    ).join(Product.category).where(Product.id == product_id, Product.is_deleted == False)).fetchone()
    if product == None:
        return {'message': 'product not found'}, 404

    images = db.execute(select(ProductImage).where(ProductImage.product_id == product_id).order_by(ProductImage.order)).scalars()

    return {
        'data': {
            'id': str(product.id),
            'title': product.name,
            'size': ['s', 'm', 'l', 'xl'],
            'product_detail': product.description,
            'price': product.price,
            'images_url': [get_image_url(image.path) for image in images],
            'category_id': product.category_id,
            'category_name': product.category_name
        }
    }, 200
