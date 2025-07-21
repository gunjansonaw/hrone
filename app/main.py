from fastapi import FastAPI
from app.database import ping_db
from app.api import products, orders

app = FastAPI()

app.include_router(products.router, prefix="/products", tags=["products"])
app.include_router(orders.router, prefix="/orders", tags=["orders"])

@app.on_event("startup")
async def startup_event():
    if not ping_db():
        raise RuntimeError("Failed to connect to MongoDB Atlas")
    print("✅ Successfully connected to MongoDB Atlas")

@app.get("/")
async def root():
    return {"message": "E-commerce API"}