# E-commerce API

A FastAPI backend for an e-commerce platform with MongoDB Atlas.

## Features

- Create and list products with filtering
- Create and list orders by user
- MongoDB Atlas integration
- Pagination support

## API Endpoints

### Products
- `POST /products` - Create a product
- `GET /products` - List products (filter by name/size)

### Orders
- `POST /orders` - Create an order
- `GET /orders/{user_id}` - List orders by user

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt