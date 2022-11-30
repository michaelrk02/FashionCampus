from flask import request

from sqlalchemy import delete, select

from FashionCampus.database import session
from FashionCampus.common import get_user
from FashionCampus.model import Category, Product, ProductCondition, ProductImage, enum_make

from FashionCampus.api.blueprints import admin_page

@admin_page.route('/products', methods = ['POST', 'PUT'])
def admin_page_save_product():
    db = session()

    user = get_user(db)
    if user == None:
        return {'message': 'unauthorized user'}, 401

    if user.type != 'seller':
        return {'message': 'you are not a seller'}, 403

    product = None

    product_id = request.json.get('product_id', '')
    if request.method == 'PUT':
        if product_id == '':
            return {'message': 'product ID must be given'}, 400

        product = db.get(Product, product_id)
        if (product == None) or product.is_deleted:
            return {'message': 'product not found or has been deleted'}, 404

    product_name = request.json.get('product_name', '')
    description = request.json.get('description', '')
    images = request.json.get('images', [])
    condition = enum_make(request.json.get('condition', ''))
    category_id = request.json.get('category_id', '')
    price = int(request.json.get('price', 0))

    if product_name == '':
        return {'message': 'product name must be given'}, 400

    if not hasattr(ProductCondition, condition):
        return {'message': 'invalid product condition'}, 400

    if category_id == '':
        return {'message': 'category ID must be given'}, 400

    category = db.get(Category, category_id)
    if (category == None) or category.is_deleted:
        return {'message': 'category not found or has been deleted'}, 404

    if price <= 0:
        return {'message': 'price must be a positive integer'}, 400

    existing = db.execute(select(Product).where(
        Product.name == product_name,
        Product.category_id == category_id,
        Product.condition == condition
    )).scalar()
    if existing != None:
        return {'message': 'product with existing name, category, and condition already exists'}, 403

    if request.method == 'POST':
        product = Product()
    else:
        if product.seller_id != user.id:
            return {'message': 'invalid seller'}, 403

    product.seller_id = user.id
    product.category_id = category_id
    product.name = product_name
    product.description = description
    product.condition = condition
    product.price = price

    db.add(product)
    db.commit()

    if request.method == 'PUT':
        db.execute(delete(ProductImage).where(ProductImage.product_id == product_id))
        db.commit()

    for i, image in enumerate(images):
        product_image = ProductImage(
            product_id = product.id,
            order = i + 1,
            path = image
        )

        db.add(product_image)
        db.commit()

    return {'message': 'product saved successfully'}, 200
