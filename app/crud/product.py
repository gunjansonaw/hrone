from typing import List, Optional
from app.models.product import Product, ProductCreate
from app.database import db
from bson import ObjectId
import re

async def create_product(product: ProductCreate) -> Product:
    product_dict = product.model_dump()
    product_dict["created_at"] = product_dict.get("created_at")
    result = await db.products.insert_one(product_dict)
    created_product = await db.products.find_one({"_id": result.inserted_id})
    return Product(**created_product)

async def get_products(
    name: Optional[str] = None,
    size: Optional[str] = None,
    limit: int = 10,
    offset: int = 0
) -> List[Product]:
    query = {}
    
    if name:
        query["name"] = {"$regex": name, "$options": "i"}
    
    if size:
        query["sizes"] = size
    
    products = []
    cursor = db.products.find(query).skip(offset).limit(limit)
    
    async for product in cursor:
        products.append(Product(**product))
    
    return products