from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

from models import ItemCreate, ItemResponse
from database_models import Item

from database import (
    init_db,
    get_items,
    delete_item,
)

from service import (
    create_item_service,
    get_items_service,
    get_item_service,
    update_item_service,
    delete_item_service,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
def root():
    return {"message": "Item API is running"}


@app.post(
    "/items",
    response_model=ItemResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_item_api(item: ItemCreate):
    db_item = Item(
        name=item.name,
        category=item.category,
        price=item.price,
        quantity=item.quantity,
    )

    return create_item_service(db_item)


@app.get("/items", response_model=list[ItemResponse])
def get_items_api():
    return get_items_service()


@app.get("/items/{id}", response_model=ItemResponse)
def get_item_api(id: int):
    row = get_item_service(id)

    if row is None:
        raise HTTPException(status_code=404, detail="Item not found")

    return row


@app.delete(
    "/items/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_item_api(id: int):
    has_found = delete_item_service(id)

    if not has_found:
        raise HTTPException(status_code=404, detail="Item not found")


@app.put("/items/{id}", response_model=ItemResponse)
def update_item_api(id: int, item: ItemCreate):
    db_item = Item(
        id=id,
        name=item.name,
        category=item.category,
        price=item.price,
        quantity=item.quantity,
    )

    try:
        updated_item = update_item_service(db_item)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    if updated_item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    return updated_item
