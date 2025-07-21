from app.database import get_db

def get_inventory_collection():
    return get_db()["inventory"]