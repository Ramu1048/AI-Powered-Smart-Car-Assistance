from typing import List, Optional
from pydantic import BaseModel

class ShowroomBase(BaseModel):
    name: str
    address: str
    latitude: float
    longitude: float
    contact_number: Optional[str] = None
    available_car_ids: List[int] = []

class ShowroomResponse(ShowroomBase):
    id: int

    class Config:
        from_attributes = True

class ShowroomNearbyResponse(ShowroomResponse):
    distance_km: float
