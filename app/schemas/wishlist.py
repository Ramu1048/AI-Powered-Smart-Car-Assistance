from typing import Optional
from pydantic import BaseModel
from app.schemas.car import CarResponse

class WishlistCreate(BaseModel):
    car_id: int

    model_config = {
        "json_schema_extra": {
            "example": {
                "car_id": 1
            }
        }
    }

class WishlistItemResponse(BaseModel):
    id: int
    user_id: int
    car_id: int
    car: Optional[CarResponse] = None

    class Config:
        from_attributes = True
