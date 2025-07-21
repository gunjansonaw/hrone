from typing import List, Optional
from app.models.order import Order, OrderCreate
from app.database import db
from bson import ObjectId

async def create_order(order: OrderCreate) -> Order:
    order_dict = order.model_dump()
    order_dict["created_at"] = order_dict.get("created_at")
    result = await db.orders.insert_one(order_dict)
    created_order = await db.orders.find_one({"_id": result.inserted_id})
    return Order(**created_order)

async def get_orders_by_user(
    user_id: str,
    limit: int = 10,
    offset: int = 0
) -> List[Order]:
    orders = []
    cursor = db.orders.find({"user_id": user_id}).skip(offset).limit(limit)
    
    async for order in cursor:
        orders.append(Order(**order))
    
    return orders