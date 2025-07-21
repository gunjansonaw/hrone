from fastapi import APIRouter, HTTPException, Query
from app.models.product import get_products_collection
from app.models.inventory import get_inventory_collection
from app.schemas.product import ProductCreate, ProductResponse, ProductListResponse
from bson import ObjectId
import re

router = APIRouter(prefix="/products")

@router.post("/", status_code=201, response_model=dict)
async def create_product(product: ProductCreate):
    products_collection = get_products_collection()
    inventory_collection = get_inventory_collection()
    
    product_data = {
        "name": product.name,
        "price": product.price
    }
    product_result = products_collection.insert_one(product_data)
    
    for size in product.sizes:
        inventory_collection.insert_one({
            "product_id": product_result.inserted_id,
            "size": size.size,
            "quantity": size.quantity
        })
    
    return {"id": str(product_result.inserted_id)}

@router.get("/", response_model=ProductListResponse)
async def list_products(
    name: str = Query(None),
    size: str = Query(None),
    limit: int = Query(10),
    offset: int = Query(0)
):
    products_collection = get_products_collection()
    inventory_collection = get_inventory_collection()
    
    query = {}
    
    if name:
        query["name"] = {"$regex": re.compile(name, re.IGNORECASE)}
    
    if size:
        inventory_items = inventory_collection.find({"size": size})
        product_ids = [item["product_id"] for item in inventory_items]
        query["_id"] = {"$in": product_ids}
    
    total = products_collection.count_documents(query)
    products = products_collection.find(query).skip(offset).limit(limit)
    
    response_data = [
        ProductResponse(id=str(product["_id"]), name=product["name"], price=product["price"])
        for product in products
    ]
    
    next_offset = offset + limit if offset + limit < total else None
    prev_offset = offset - limit if offset - limit >= 0 else None
    
    return {
        "data": response_data,
        "page": {
            "next": str(next_offset) if next_offset is not None else None,
            "limit": limit,
            "previous": str(prev_offset) if prev_offset is not None else None
        }
    }