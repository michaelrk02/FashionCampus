import re
import base64

from .storage import encoded_blob_regex, save_blob

def get_image_url(path):
    return '/image/%s' % (path)
