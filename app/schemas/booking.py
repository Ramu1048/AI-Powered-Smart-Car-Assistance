from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from app.schemas.car import CarResponse
from app.schemas.showroom import ShowroomResponse

class BookingCreate(BaseModel):
    car_id: int
    showroom_id: int
    booking_type: str = Field(..., description="test_drive or purchase")
    scheduled_date: datetime

    model_config = {
        "json_schema_extra": {
            "example": {
                "car_id": 1,
                "showroom_id": 1,
                "booking_type": "test_drive",
                "scheduled_date": "2026-07-25T14:30:00"
            }
        }
    }

class BookingResponse(BaseModel):
    id: int
    user_id: int
    car_id: int
    showroom_id: int
    booking_type: str
    status: str
    scheduled_date: datetime
    created_at: datetime
    
    car: Optional[CarResponse] = None
    showroom: Optional[ShowroomResponse] = None

    class Config:
        from_attributes = True
