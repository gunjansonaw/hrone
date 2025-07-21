from fastapi import APIRouter, HTTPException, Query
from app.models.order import get_orders_collection
from app.models.product import get_products_collection
from app.schemas.order import OrderCreate, OrderListResponse, OrderResponse, OrderItemResponse, ProductDetails
from bson import ObjectId
from typing import List

router = APIRouter(prefix="/orders")

@router.post("/", status_code=201, response_model=dict)
async def create_order(order: OrderCreate):
    orders_collection = get_orders_collection()
    products_collection = get_products_collection()
    
    total = 0.0
    items = []
    
    for item in order.items:
        product = products_collection.find_one({"_id": ObjectId(item.productId)})
        if not product:
            raise HTTPException(status_code=404, detail=f"Product {item.productId} not found")
        
        items.append({
            "productId": ObjectId(item.productId),
            "qty": item.qty
        })
        total += product["price"] * item.qty
    
    order_data = {
        "userId": order.userId,
        "items": items,
        "total": total
    }
    
    result = orders_collection.insert_one(order_data)
    return {"id": str(result.inserted_id)}

@router.get("/{user_id}", response_model=OrderListResponse)
async def get_orders(
    user_id: str,
    limit: int = Query(10),
    offset: int = Query(0)
):
    orders_collection = get_orders_collection()
    products_collection = get_products_collection()
    
    query = {"userId": user_id}
    total = orders_collection.count_documents(query)
    orders = orders_collection.find(query).skip(offset).limit(limit)
    
    response_data = []
    for order in orders:
        order_items = []
        for item in order["items"]:
            product = products_collection.find_one({"_id": item["productId"]})
            if product:
                order_items.append(OrderItemResponse(
                    productDetails=ProductDetails(
                        name=product["name"],
                        id=str(product["_id"])
                    ),
                    qty=item["qty"]
                ))
        
        response_data.append(OrderResponse(
            id=str(order["_id"]),
            items=order_items,
            total=order["total"]
        ))
    
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