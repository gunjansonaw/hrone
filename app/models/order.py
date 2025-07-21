from pydantic import BaseModel, Field, ConfigDict
from typing import List
from datetime import datetime
from bson import ObjectId
from .product import PyObjectId

class OrderItem(BaseModel):
    product_id: str
    bought_quantity: int
    size: str

class OrderBase(BaseModel):
    user_id: str
    items: List[OrderItem]
    total_amount: float
    status: str = "pending"

class OrderCreate(OrderBase):
    pass

class Order(OrderBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
    )