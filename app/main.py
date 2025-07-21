from fastapi import FastAPI
from app.routes import products, orders

app = FastAPI()

app.include_router(products.router)
app.include_router(orders.router)

@app.get("/")
def read_root():
    return {"message": "E-commerce Backend API"}