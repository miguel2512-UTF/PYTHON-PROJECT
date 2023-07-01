from db.client import db_client
from db.models.product import Product
from db.schemas.product import product_schema, products_schema
from bson import ObjectId

class ProductService():

    def findAll():
        products = list(db_client.product.find())
        products_list = products_schema(products)

        return products_list
    
    def find_one(field: str, value):
        product = db_client.product.find_one({field: value})
        product = product_schema(product)

        return product

    def insert_one(product: dict):
        del product["id"]
        product_id = db_client.product.insert_one(product).inserted_id
        new_product = db_client.product.find_one({ "_id": product_id })

        return product_schema(new_product)
    
    def save(product: dict):
        if product["id"]:
            id_product = product["id"]
            db_client.product.find_one_and_replace({"_id": ObjectId(id_product)}, product)
        else:
            del product["id"]
            id_product = db_client.product.insert_one(product).inserted_id

        product = db_client.product.find_one({ "_id": ObjectId(id_product) })

        return product_schema(product)
    
    def delete(id):
        delete_product = db_client.product.find_one_and_delete({"_id": ObjectId(id)})   
        delete_product = product_schema(delete_product)

        return delete_product