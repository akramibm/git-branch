import os
from typing import Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

# Initialize FastAPI app
app = FastAPI(
    title="Sample Python Application",
    description="A modern FastAPI app example",
    version="1.0.0",
)


# Pydantic model for request validation
class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None


# In-memory database simulation
items_db = {}


# 1. Root route
@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI application!"}


# 2. Health check route (Ideal for AWS / Kubernetes checks)
@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "api"}


# 3. GET endpoint with path & query parameters
@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item": items_db[item_id], "query": q}


# 4. POST endpoint with JSON request body validation
@app.post("/items/", status_code=201)
def create_item(item_id: int, item: Item):
    if item_id in items_db:
        raise HTTPException(
            status_code=400, detail="Item with this ID already exists"
        )
    items_db[item_id] = item
    return {"message": "Item created successfully", "data": item}


# Server entry point
if __name__ == "__main__":
    # Get port from environment or default to 8000
    port = int(os.environ.get("PORT", 8000))

    # Run application using Uvicorn server
    uvicorn.run("app:app", host="0.0.0.0", port=port, reload=True)