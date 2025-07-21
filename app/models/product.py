from app.database import get_db

def get_products_collection():
    return get_db()["products"]