import hashlib
import re

from flask import request

from sqlalchemy import delete, select

from FashionCampus.database import session
from FashionCampus.common import get_user, save_encoded_blob,delete_blob
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

        if product.seller_id != user.id:
            return {'message': 'invalid seller'}, 403
    else:
        product = Product()

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

    condition = ProductCondition(condition)

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
        Product.condition == condition,
        Product.id != product_id if request.method == 'PUT' else True
    )).scalar()

    if existing != None:
        return {'message': 'product with existing name, category, and condition already exists'}, 403

    product.seller_id = user.id
    product.category_id = category_id
    product.name = product_name
    product.description = description
    product.condition = condition
    product.price = price

    db.add(product)
    db.commit()

    removed_images = set()
    existing_image_regex = '/image/([0-9a-f\-]+)'

    if request.method == 'PUT':
        old_images = db.execute(select(ProductImage).where(ProductImage.product_id == product_id)).scalars()
        for image in old_images:
            removed_images.add(image.path)

        for image in images:
            match = re.match(existing_image_regex, image)
            if match != None:
                blob = match[1]
                if blob in removed_images:
                    removed_images.remove(blob)

        for blob in removed_images:
            delete_blob(blob)

        db.execute(delete(ProductImage).where(ProductImage.product_id == product_id))
        db.commit()

    order = 1
    for image in images:
        match = re.match(existing_image_regex, image)
        if match != None:
            blob = match[1]
            product_image = ProductImage(
                product_id = product.id,
                order = order,
                path = blob
            )

            db.add(product_image)
            db.commit()

            order += 1
        else:
            blob = save_encoded_blob(image)
            if blob != None:
                product_image = ProductImage(
                    product_id = product.id,
                    order = order,
                    path = blob
                )

                db.add(product_image)
                db.commit()

                order += 1

    return {'message': 'product saved successfully'}, 200
