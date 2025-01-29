import redis
from fastapi import FastAPI, Depends
from typing import List, Dict
import json

app = FastAPI()

# Redis Configuration
redis_client = redis.Redis(host='localhost', port=6379, db=0)

# Simulation product data
products: List[Dict] = [
    {"id": 1, "name": "Product A", "price": 10},
    {"id": 2, "name": "Product B", "price": 20},
    {"id": 3, "name": "Product C", "price": 30},
]

def get_products_from_cache():
    cached_products = redis_client.get("products")
    if cached_products:
        return json.loads(cached_products.decode('utf-8'))
    return None

def set_products_to_cache(products: List[Dict]):
    redis_client.setex("products", 60, json.dumps(products)) # Expire in 1 hour

@app.get("/products")
async def get_products():
    #get data from redis (1)
    cached_products = get_products_from_cache()
    if cached_products:
        print("Data is taken from cache")
        return cached_products #(2)

    print("Data is taken from the database")
    set_products_to_cache(products) #(3)
    return products