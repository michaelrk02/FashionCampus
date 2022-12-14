from flask import request

from sqlalchemy import func, select

from FashionCampus.database import session
from FashionCampus.common import get_image_url
from FashionCampus.model import Category, Product, ProductImage

from FashionCampus.api.blueprints import product_list

@product_list.route('/products', methods = ['GET'])
def product_list_get_product_list():

    def apply_filter(stmt, sort_by, categories, price, conditions, product_name, counting = False):
        stmt = stmt.select_from(Product). \
            join(Product.category.and_(Category.is_deleted == False)). \
            join(Product.images.and_(ProductImage.order == 1), isouter = True). \
            where(Product.is_deleted == False)

        if not counting:
            if sort_by == '':
                stmt = stmt.order_by(Product.name)

            if sort_by == 'Price a_z':
                stmt = stmt.order_by(Product.price.asc())

            if sort_by == 'Price z_a':
                stmt = stmt.order_by(Product.price.desc())

        if categories[0] != '':
            stmt = stmt.where(Product.category_id.in_(categories))

        if price != '':
            range = price.split(',')
            stmt = stmt.where(Product.price >= int(range[0]), Product.price <= int(range[1]))

        if conditions[0] != '':
            stmt = stmt.where(Product.condition.in_(conditions))

        # frontend fix
        if product_name == 'undefined':
            product_name = ''

        stmt = stmt.where(Product.name.ilike('%%%s%%' % (product_name)))

        return stmt

    db = session()

    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 15))
    sort_by = request.args.get('sort_by', '')
    categories = request.args.get('category', '').split(',')
    price = request.args.get('price', '')
    conditions = request.args.get('condition', '').split(',')
    product_name = request.args.get('product_name', '')


    stmt = select(
        Product.id,
        Product.name,
        Product.price,
        ProductImage.path.label('image_path')
    )
    stmt = apply_filter(stmt, sort_by, categories, price, conditions, product_name)

    count_stmt = select(func.count())
    count_stmt = apply_filter(count_stmt, sort_by, categories, price, conditions, product_name, True)
    count = db.execute(count_stmt).scalar()

    products = db.execute(stmt.limit(page_size).offset((page - 1) * page_size)).fetchall()

    return {
        'data': [
            {
                'id': str(p.id),
                'image': get_image_url(p.image_path),
                'title': p.name,
                'price': p.price
            } for p in products
        ],
        'total_rows': count
    }, 200
