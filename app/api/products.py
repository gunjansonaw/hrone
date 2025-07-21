from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List
from app.crud.product import create_product, get_products
from app.models.product import Product, ProductCreate

router = APIRouter()

@router.post("/", response_model=Product, status_code=201)
async def create_product_endpoint(product: ProductCreate):
    return await create_product(product)

@router.get("/", response_model=List[Product])
async def list_products(
    name: Optional[str] = Query(None),
    size: Optional[str] = Query(None),
    limit: int = Query(10, gt=0),
    offset: int = Query(0, ge=0)
):
    return await get_products(name=name, size=size, limit=limit, offset=offset)