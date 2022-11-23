from flask import Flask

from FashionCampus.api.blueprints import universal as bp_universal
from FashionCampus.api.blueprints import home as bp_home
from FashionCampus.api.blueprints import authentication as bp_authentication
from FashionCampus.api.blueprints import product_list as bp_product_list
from FashionCampus.api.blueprints import product_detail_page as bp_product_detail_page
from FashionCampus.api.blueprints import cart as bp_cart
from FashionCampus.api.blueprints import profile_page as bp_profile_page
from FashionCampus.api.blueprints import admin_page as bp_admin_page

import FashionCampus.api.universal
import FashionCampus.api.home
import FashionCampus.api.authentication
import FashionCampus.api.product_list
import FashionCampus.api.product_detail_page
import FashionCampus.api.cart
import FashionCampus.api.profile_page
import FashionCampus.api.admin_page

app = Flask(__name__)

app.register_blueprint(bp_universal)
app.register_blueprint(bp_home)
app.register_blueprint(bp_authentication)
app.register_blueprint(bp_product_list)
app.register_blueprint(bp_product_detail_page)
app.register_blueprint(bp_cart)
app.register_blueprint(bp_profile_page)
app.register_blueprint(bp_admin_page)

@app.route('/', methods = ['GET'])
def hello_world():
    return {'message': 'Hello world'}, 200
