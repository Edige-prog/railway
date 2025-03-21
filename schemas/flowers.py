from typing import List, Optional

from pydantic import BaseModel



class FlowerCreate(BaseModel):
    name: str
    price: float
    quantity: int

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Lily",
                "price": 800,
                "quantity": 20,
            }
        }


class FlowerInfo(BaseModel):
    id: int
    name: str
    price: float
    quantity: int

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Rose",
                "price": 500,
                "quantity": 101,
            }
        }


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    price: Optional[float] = None
    quantity: Optional[int] = None