from flask import request

from sqlalchemy import delete, select

from FashionCampus.database import session
from FashionCampus.common import get_user, delete_blob
from FashionCampus.model import Product, ProductImage

from FashionCampus.api.blueprints import admin_page

@admin_page.route('/products/<product_id>', methods = ['DELETE'])
def admin_page_delete_product(product_id):
    db = session()

    user = get_user(db)
    if user == None:
        return {'message': 'unauthorized user'}, 401

    if user.type != 'seller':
        return {'message': 'you are not a seller'}, 403

    product = db.get(Product, product_id)
    if (product == None) or product.is_deleted:
        return {'message': 'product does not exist or has been deleted'}, 404

    if product.seller_id != user.id:
        return {'message': 'invalid seller'}, 403

    images = db.execute(select(ProductImage).where(ProductImage.product_id == product_id)).scalars()
    for image in images:
        delete_blob(image.path)

    db.execute(delete(ProductImage).where(ProductImage.product_id == product_id))
    db.commit()

    product.is_deleted = True
    db.add(product)
    db.commit()

    return {'message': 'product deleted successfully'}, 200
