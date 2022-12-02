import os

from flask import request, send_file

from FashionCampus.common import get_blob_path

from FashionCampus.api.blueprints import universal

@universal.route('/image/<image_id>', methods = ['GET'])
def universal_get_image(image_id):
    path = None

    if image_id == 'named':
        name = os.path.basename(request.args.get('name', ''))
        if name == '':
            return {'message': 'invalid image name'}, 400

        path = get_blob_path('named/%s' % (name))
    else:
        path = get_blob_path(image_id)

    if not os.path.isfile(path):
        return {'message': 'image not found'}, 404

    return send_file(path)
