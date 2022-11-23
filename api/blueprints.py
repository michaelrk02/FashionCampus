from flask import Blueprint

universal = Blueprint('universal', __name__)
home = Blueprint('home', __name__)
authentication = Blueprint('authentication', __name__)
product_list = Blueprint('product_list', __name__)
product_detail_page = Blueprint('product_detail_page', __name__)
cart = Blueprint('cart', __name__)
profile_page = Blueprint('profile_page', __name__)
admin_page = Blueprint('admin_page', __name__)
