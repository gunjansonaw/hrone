from app.database import get_db

def get_orders_collection():
    return get_db()["orders"]