import uuid
import os
import re
import base64

encoded_blob_regex = '^data:[a-zA-Z0-9_\-]+\/[a-zA-Z0-9_\-]+;base64,([a-zA-Z0-9+\/=]*)$'

def get_blob_path(blob):
    return os.path.join(os.getcwd(), './blob/%s' % (blob))

def save_blob(data):
    filename = str(uuid.uuid4())

    try:
        f = open(get_blob_path(filename), 'wb')

        f.write(data)
        f.close()
    except:
        return None

    return filename

def save_encoded_blob(encdata):
    match = re.match(encoded_blob_regex, encdata)
    if match == None:
        return None

    data = match[1].encode('utf-8')
    data = base64.b64decode(data)

    blob = save_blob(data)

    return blob

def delete_blob(blob):
    if blob != '':
        path = get_blob_path(blob)
        if os.path.isfile(path):
            os.remove(path)
