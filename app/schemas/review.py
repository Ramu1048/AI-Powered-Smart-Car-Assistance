from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

class ReviewCreate(BaseModel):
    rating: float = Field(..., ge=1.0, le=5.0)
    comment: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "rating": 4.5,
                "comment": "Excellent family car with top notch safety and tech features."
            }
        }
    }

class ReviewResponse(BaseModel):
    car_id: int
    user_name: str
    rating: float
    comment: str
    sentiment: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

class YoutubeSummaryResponse(BaseModel):
    car_id: int
    video_url: str
    summary_text: str
    pros: List[str] = []
    cons: List[str] = []
    created_at: datetime

    class Config:
        from_attributes = True
