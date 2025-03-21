from pydantic import BaseModel
from schemas.flowers import FlowerInfo

class PurchaseItemInfo(BaseModel):
    id: int
    flower: FlowerInfo
    quantity: int

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "flower": {
                    "id": 1,
                    "name": "Rose",
                    "price": 500,
                    "quantity": 10
                },
                "quantity": 2
            }
        }