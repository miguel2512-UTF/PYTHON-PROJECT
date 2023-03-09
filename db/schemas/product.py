def product_schema (product) -> dict:
    
    return {
        "id": str(product["_id"]),
        "code": str(product["code"]),
        "name": str(product["name"]),
        "description": str(product["description"]),
        "price": int(product["price"]),
        "stock": int(product["stock"]),
        "image": str(product["image"]),
        "state": bool(product["state"])
    }

def products_schema (products: list) -> list:
    return [product_schema(product) for product in products]