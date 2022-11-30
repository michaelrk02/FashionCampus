from flask import request

from sqlalchemy import delete, select

from FashionCampus.database import session
from FashionCampus.common import get_user
from FashionCampus.model import Category

from FashionCampus.api.blueprints import admin_page

def admin_page_save_category_handler(category_id = ''):
    db = session()

    user = get_user(db)
    if user == None:
        return {'message': 'unauthorized user'}, 401

    if user.type != 'seller':
        return {'message': 'you are not a seller'}, 403

    category = None

    if request.method == 'PUT':
        if category_id == '':
            return {'message': 'category ID must be given'}, 400

        category = db.get(Category, category_id)
        if (category == None) or category.is_deleted:
            return {'message': 'category not found or has been deleted'}, 404

    category_name = request.json.get('category_name', '')

    if category_name == '':
        return {'message': 'category name must be given'}, 400

    existing = db.execute(select(Category).where(
        Category.name == category_name
    )).scalar()
    if existing != None:
        return {'message': 'category with existing name already exists'}, 403

    if request.method == 'POST':
        category = Category()

    category.name = category_name

    db.add(category)
    db.commit()

    return {'message': 'category saved successfully'}, 200

@admin_page.route('/categories', methods = ['POST'])
def admin_page_save_category_post():
    return admin_page_save_category_handler()

@admin_page.route('/categories/<category_id>', methods = ['PUT'])
def admin_page_save_category_put(category_id):
    return admin_page_save_category_handler(category_id)
