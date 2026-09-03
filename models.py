from pydantic import BaseModel, Field

class ItemCreate(BaseModel):
    name: str = Field(min_length=1)
    category: str
    price: int = Field(ge=0)
    quantity: int = Field(ge=0)


class ItemResponse(BaseModel):
    id: int
    name: str = Field(min_length=1)
    category: str
    price: int = Field(ge=0)
    quantity: int = Field(ge=0)