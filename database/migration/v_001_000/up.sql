CREATE TYPE USER_TYPE AS ENUM('seller', 'buyer');
CREATE TYPE PRODUCT_SIZE AS ENUM('s', 'm', 'l', 'xl');
CREATE TYPE PRODUCT_CONDITION AS ENUM('old', 'new');
CREATE TYPE SHIPPING_METHOD AS ENUM('regular', 'next_day');

CREATE TABLE "user" (
    "id" UUID NOT NULL DEFAULT UUID_GENERATE_V4(),
    "name" VARCHAR(128) NOT NULL,
    "email" VARCHAR(254) NOT NULL,
    "password_hash" CHAR(64) NOT NULL,
    "password_salt" CHAR(16) NOT NULL,
    "phone_number" VARCHAR(24) NOT NULL,
    "type" USER_TYPE NOT NULL,

    CONSTRAINT "PK_User" PRIMARY KEY ("id")
);

CREATE TABLE "seller" (
    "user_id" UUID NOT NULL,
    "sales" INT NOT NULL DEFAULT 0,

    CONSTRAINT "PK_Seller" PRIMARY KEY ("user_id"),
    CONSTRAINT "FK_Seller_User" FOREIGN KEY ("user_id") REFERENCES "user" ("id")
);

CREATE TABLE "category" (
    "id" UUID NOT NULL DEFAULT UUID_GENERATE_V4(),
    "name" VARCHAR(128) NOT NULL,
    "is_deleted" BOOLEAN NOT NULL DEFAULT FALSE,

    CONSTRAINT "PK_Category" PRIMARY KEY ("id"),
    CONSTRAINT "UID_Category_Name" UNIQUE ("name")
);

CREATE TABLE "product" (
    "id" UUID NOT NULL DEFAULT UUID_GENERATE_V4(),
    "seller_id" UUID NOT NULL,
    "category_id" UUID NOT NULL,
    "name" VARCHAR(128) NOT NULL,
    "description" TEXT NOT NULL,
    "condition" PRODUCT_CONDITION NOT NULL,
    "price" INT NOT NULL,
    "is_deleted" BOOLEAN NOT NULL DEFAULT FALSE,

    CONSTRAINT "PK_Product" PRIMARY KEY ("id"),
    CONSTRAINT "FK_Product_Seller" FOREIGN KEY ("seller_id") REFERENCES "seller" ("user_id"),
    CONSTRAINT "FK_Product_Category" FOREIGN KEY ("category_id") REFERENCES "category" ("id")
);

CREATE TABLE "product_image" (
    "product_id" UUID NOT NULL,
    "image_id" UUID NOT NULL DEFAULT UUID_GENERATE_V4(),
    "order" INT NOT NULL,
    "path" TEXT NOT NULL,

    CONSTRAINT "PK_ProductImage" PRIMARY KEY ("product_id", "image_id"),
    CONSTRAINT "FK_ProductImage_Product" FOREIGN KEY ("product_id") REFERENCES "product" ("id"),
    CONSTRAINT "UID_ProductImage_ProductId_Order" UNIQUE ("product_id", "order")
);

CREATE TABLE "buyer" (
    "user_id" UUID NOT NULL,
    "shipping_address" JSON NOT NULL,
    "balance" INT NOT NULL DEFAULT 0,

    CONSTRAINT "PK_Buyer" PRIMARY KEY ("user_id"),
    CONSTRAINT "FK_Buyer_User" FOREIGN KEY ("user_id") REFERENCES "user" ("id")
);

CREATE TABLE "cart_item" (
    "id" UUID NOT NULL DEFAULT UUID_GENERATE_V4(),
    "buyer_id" UUID NOT NULL,
    "product_id" UUID NOT NULL,
    "details_quantity" INT NOT NULL,
    "details_size" PRODUCT_SIZE NOT NULL,

    CONSTRAINT "PK_CartItem" PRIMARY KEY ("id"),
    CONSTRAINT "FK_CartItem_Buyer" FOREIGN KEY ("buyer_id") REFERENCES "buyer" ("user_id"),
    CONSTRAINT "FK_CartItem_Product" FOREIGN KEY ("product_id") REFERENCES "product" ("id"),
    CONSTRAINT "UID_CartItem_BuyerId_ProductId_DetailsSize" UNIQUE ("buyer_id", "product_id", "details_size")
);

CREATE TABLE "order" (
    "id" UUID NOT NULL DEFAULT UUID_GENERATE_V4(),
    "buyer_id" UUID NOT NULL,
    "created_at" TIMESTAMP NOT NULL DEFAULT NOW(),
    "gross" INT NOT NULL,
    "shipping_method" SHIPPING_METHOD NOT NULL,
    "shipping_address" JSON NOT NULL,
    "shipping_price" INT NOT NULL,
    "total" INT NOT NULL,

    CONSTRAINT "PK_Order" PRIMARY KEY ("id"),
    CONSTRAINT "FK_Order_Buyer" FOREIGN KEY ("buyer_id") REFERENCES "buyer" ("user_id")
);

CREATE TABLE "order_item" (
    "id" UUID NOT NULL DEFAULT UUID_GENERATE_V4(),
    "order_id" UUID NOT NULL,
    "product_id" UUID NOT NULL,
    "details_quantity" INT NOT NULL,
    "details_size" PRODUCT_SIZE NOT NULL,
    "product_price" INT NOT NULL,

    CONSTRAINT "PK_OrderItem" PRIMARY KEY ("id"),
    CONSTRAINT "FK_OrderItem_Order" FOREIGN KEY ("order_id") REFERENCES "order" ("id"),
    CONSTRAINT "FK_OrderItem_Product" FOREIGN KEY ("product_id") REFERENCES "product" ("id"),
    CONSTRAINT "UID_OrderItem_OrderId_ProductId_DetailsSize" UNIQUE ("order_id", "product_id", "details_size")
);
