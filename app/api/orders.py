from fastapi import APIRouter, HTTPException, Query
from typing import List
from app.crud.order import create_order, get_orders_by_user
from app.models.order import Order, OrderCreate

router = APIRouter()

@router.post("/", response_model=Order, status_code=201)
async def create_order_endpoint(order: OrderCreate):
    return await create_order(order)

@router.get("/{user_id}", response_model=List[Order])
async def list_orders_by_user(
    user_id: str,
    limit: int = Query(10, gt=0),
    offset: int = Query(0, ge=0)
):
    return await get_orders_by_user(user_id, limit=limit, offset=offset)