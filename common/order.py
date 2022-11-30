from sqlalchemy import select

from FashionCampus.model import CartItem, Product, ShippingMethod

def get_gross_amount(db, buyer_id):
    gross_amount = 0

    cart_items = db.execute(select(
        CartItem.details_quantity,
        Product.price.label('product_price')
    ).join(CartItem.product).where(CartItem.buyer_id == buyer_id)).fetchall()

    for cart_item in cart_items:
        gross_amount += cart_item.details_quantity * cart_item.product_price

    return gross_amount

def get_shipping_price(shipping_method, gross_amount):
    if shipping_method == ShippingMethod.regular:
        if gross_amount < 200000:
            return round(0.15 * gross_amount)
        else:
            return round(0.2 * gross_amount)
    elif shipping_method == ShippingMethod.next_day:
        if gross_amount < 300000:
            return round(0.2 * gross_amount)
        else:
            return round(0.25 * gross_amount)

    return 0
