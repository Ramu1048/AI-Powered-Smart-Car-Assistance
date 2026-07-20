from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

class CarBase(BaseModel):
    brand: str
    model: str
    variant: str
    price: float = Field(..., description="Price in INR")
    mileage: Optional[float] = Field(None, description="Mileage in kmpl")
    fuel_type: str = Field(..., description="Petrol, Diesel, Electric, Hybrid, CNG")
    transmission: str = Field(..., description="Manual or Automatic")
    engine_specs: Optional[str] = Field(None, description="Engine specs description")
    safety_features: Optional[List[str]] = Field(default=[], description="List of safety features")
    tech_features: Optional[List[str]] = Field(default=[], description="List of technology features")
    images: Optional[List[str]] = Field(default=[], description="List of image URLs")

class CarCreate(CarBase):
    model_config = {
        "json_schema_extra": {
            "example": {
                "brand": "Hyundai",
                "model": "Creta",
                "variant": "SX Opt",
                "price": 1850000.0,
                "mileage": 16.8,
                "fuel_type": "Petrol",
                "transmission": "Automatic",
                "engine_specs": "1.5L Turbo GDi",
                "safety_features": ["6 Airbags", "ABS with EBD", "ESC", "ADAS Level 2"],
                "tech_features": ["10.25 inch Infotainment", "Bose Premium Sound", "Ventilated Seats"],
                "images": ["https://example.com/creta1.jpg"]
            }
        }
    }

class CarUpdate(BaseModel):
    brand: Optional[str] = None
    model: Optional[str] = None
    variant: Optional[str] = None
    price: Optional[float] = None
    mileage: Optional[float] = None
    fuel_type: Optional[str] = None
    transmission: Optional[str] = None
    engine_specs: Optional[str] = None
    safety_features: Optional[List[str]] = None
    tech_features: Optional[List[str]] = None
    images: Optional[List[str]] = None

class CarResponse(CarBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class CompareRequest(BaseModel):
    car_ids: List[int]

    model_config = {
        "json_schema_extra": {
            "example": {
                "car_ids": [1, 2]
            }
        }
    }
