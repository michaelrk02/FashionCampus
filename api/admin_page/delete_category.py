from flask import request

from sqlalchemy import delete

from FashionCampus.database import session
from FashionCampus.common import get_user
from FashionCampus.model import Category

from FashionCampus.api.blueprints import admin_page

@admin_page.route('/categories/<category_id>', methods = ['DELETE'])
def admin_page_delete_category(category_id):
    db = session()

    user = get_user(db)
    if user == None:
        return {'message': 'unauthorized user'}, 401

    if user.type != 'seller':
        return {'message': 'you are not a seller'}, 403

    category = db.get(Category, category_id)
    if (category == None) or category.is_deleted:
        return {'message': 'category does not exist or has been deleted'}, 404

    category.is_deleted = True
    db.add(category)
    db.commit()

    return {'message': 'category deleted successfully'}, 200
