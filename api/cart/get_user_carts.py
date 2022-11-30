from sqlalchemy import select

from FashionCampus.database import session
from FashionCampus.common import get_image_url, get_user
from FashionCampus.model import CartItem, Product, ProductImage

from FashionCampus.api.blueprints import cart

@cart.route('/cart', methods = ['GET'])
def cart_get_user_carts():
    db = session()

    user = get_user(db)
    if user == None:
        return {'message': 'unauthorized user'}, 401

    if user.type != 'buyer':
        return {'message': 'you are not a buyer'}, 403

    cart_items = db.execute(select(
        CartItem.id,
        CartItem.details_quantity,
        CartItem.details_size,
        Product.name.label('product_name'),
        Product.price.label('product_price'),
        ProductImage.path.label('product_image_path')
    ).join(CartItem.product).join(Product.images.and_(ProductImage.order == 1), isouter = True).where(CartItem.buyer_id == user.id)).fetchall()

    return {
        'data': [
            {
                'id': cart_item.id,
                'details': {
                    'quantity': cart_item.details_quantity,
                    'size': cart_item.details_size
                },
                'price': cart_item.product_price,
                'image': get_image_url(cart_item.product_image_path),
                'name': cart_item.product_name
            } for cart_item in cart_items
        ]
    }, 200
