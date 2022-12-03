import random

from faker import Faker

from FashionCampus.common import get_blob_path, save_blob
from FashionCampus.model import Category, Product, ProductImage

def create_category(db, name):
    fake = Faker()

    category = Category(
        name = name
    )

    db.add(category)
    db.commit()

def create_product(db, seller_id, category_id, has_images = True):
    fake = Faker()

    product = Product(
        seller_id = seller_id,
        category_id = category_id,
        name = fake.sentence(3),
        description = fake.paragraph(),
        condition = random.choice(['new', 'used']),
        price = random.randint(50000, 500000)
    )

    db.add(product)
    db.commit()

    category = db.get(Category, category_id)

    if has_images:
        for i in range(random.randint(1, 5)):
            path = ''

            try:
                f = open(get_blob_path('named/Category_%s' % (category.name)), 'rb')
                data = f.read()
                path = save_blob(data)
                f.close()
            except:
                pass

            image = ProductImage(
                product_id = product.id,
                order = i + 1,
                path = path
            )

            db.add(image)
            db.commit()
