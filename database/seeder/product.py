import random

from faker import Faker

from FashionCampus.model import Category, Product, ProductImage

def create_category(db):
    fake = Faker()

    category = Category(
        name = fake.word().capitalize()
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
        condition = random.choice(['old', 'new']),
        price = random.randint(50000, 500000)
    )

    db.add(product)
    db.commit()

    if has_images:
        for i in range(random.randint(1, 5)):
            image = ProductImage(
                product_id = product.id,
                order = i + 1,
                path = ''
            )

            db.add(image)
            db.commit()
