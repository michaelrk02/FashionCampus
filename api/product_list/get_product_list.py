from flask import request

from sqlalchemy import select

from FashionCampus.database import session
from FashionCampus.common import get_image_url
from FashionCampus.model import Category, Product, ProductImage

from FashionCampus.api.blueprints import product_list

@product_list.route('/products', methods = ['GET'])
def product_list_get_product_list():
    db = session()

    stmt = select(
        Product.id,
        Product.name,
        Product.price,
        ProductImage.path.label('image_path')
    ). \
    select_from(Product). \
    join(Product.category.and_(Category.is_deleted == False)). \
    join(Product.images.and_(ProductImage.order == 1)). \
    where(Product.is_deleted == False)

    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 15))
    sort_by = request.args.get('sort_by', '')
    category = request.args.get('category', '')
    price = request.args.get('price', '')
    condition = request.args.get('condition', '')
    product_name = request.args.get('product_name', '')

    stmt = stmt.limit(page_size).offset((page - 1) * page_size)

    if sort_by == '':
        stmt = stmt.order_by(Product.name)

    if sort_by == 'Price a_z':
        stmt = stmt.order_by(Product.price.asc())

    if sort_by == 'Price z_a':
        stmt = stmt.order_by(Product.price.desc())

    if category != '':
        stmt = stmt.where(Product.category_id == category)

    if price != '':
        range = price.split(',')
        stmt = stmt.where(Product.price >= int(range[0]), Product.price <= int(range[1]))

    if condition != '':
        stmt = stmt.where(Product.condition == condition)

    stmt = stmt.where(Product.name.ilike('%%%s%%' % (product_name)))

    products = db.execute(stmt).fetchall()

    return {
        'data': [
            {
                'id': str(p.id),
                'image': get_image_url(p.image_path),
                'title': p.name,
                'price': p.price
            } for p in products
        ],
        'total_rows': len(products)
    }, 200
