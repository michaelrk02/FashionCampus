from flask import request

from sqlalchemy import select

from FashionCampus.database import session
from FashionCampus.common import delete_blob, get_blob_path, save_encoded_blob
from FashionCampus.model import Category
from FashionCampus.nn.prediction import predict

from FashionCampus.api.blueprints import product_list

@product_list.route('/products/search_image', methods = ['POST'])
def product_list_search_product_by_image():
    db = session()

    image = request.json.get('image', '')
    if image == '':
        return {'message': 'image must be given'}, 400

    blob = save_encoded_blob(image)
    if blob == None:
        return {'message': 'unable to create temporary image. please check whether the file is correct'}, 400

    prediction = predict(get_blob_path(blob))
    delete_blob(blob)

    category = db.execute(select(Category).where(Category.name == prediction)).scalar()

    return {
        'category_id': category.id if category != None else None,
        '_label': prediction
    }
