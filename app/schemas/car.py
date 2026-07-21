from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

# --- YouTube Review Response Schema ---
class YoutubeReviewResponse(BaseModel):
    channel_name: Optional[str] = None
    video_title: str
    video_url: Optional[str] = None
    channel_url: Optional[str] = None
    thumbnail_url: Optional[str] = None

    class Config:
        from_attributes = True

# --- Car Schemas ---
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
    # --- Expanded Specification Fields ---
    body_type: Optional[str] = Field(None, description="Hatchback, Sedan, SUV, MPV, etc.")
    seating_capacity: Optional[int] = Field(5, description="Number of seats")
    ncap_rating: Optional[float] = Field(None, description="Global NCAP star rating (0-5)")
    dimensions: Optional[Dict[str, Any]] = Field(None, description="Length, Width, Height, Wheelbase, Ground Clearance, Boot Space")
    engine_details: Optional[Dict[str, Any]] = Field(None, description="Capacity cc, Max Power bhp, Max Torque Nm, Cylinders, Transmission Type")
    adas_features: Optional[List[str]] = Field(default=[], description="ADAS features list")
    comfort_features: Optional[Dict[str, Any]] = Field(None, description="Sunroof, Ventilated Seats, Drive Modes, Touchscreen, Digital Cluster")

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
                "images": ["https://example.com/creta1.jpg"],
                "body_type": "SUV",
                "seating_capacity": 5,
                "ncap_rating": 5.0,
                "dimensions": {"length_mm": 4330, "width_mm": 1790, "height_mm": 1635, "wheelbase_mm": 2610, "ground_clearance_mm": 190, "boot_space_litres": 433},
                "engine_details": {"capacity_cc": 1497, "max_power_bhp": 115, "max_torque_nm": 144, "cylinders": 4, "transmission_type": "IVT"},
                "adas_features": ["Lane Keep Assist", "Forward Collision Warning", "Adaptive Cruise Control"],
                "comfort_features": {"sunroof_type": "Panoramic", "ventilated_seats": True, "drive_modes": ["Eco", "Normal", "Sport"], "touchscreen_size_inches": 10.25, "digital_cluster": True}
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
    body_type: Optional[str] = None
    seating_capacity: Optional[int] = None
    ncap_rating: Optional[float] = None
    dimensions: Optional[Dict[str, Any]] = None
    engine_details: Optional[Dict[str, Any]] = None
    adas_features: Optional[List[str]] = None
    comfort_features: Optional[Dict[str, Any]] = None

class CarResponse(CarBase):
    id: int
    created_at: datetime
    youtube_reviews: Optional[List[YoutubeReviewResponse]] = []

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
