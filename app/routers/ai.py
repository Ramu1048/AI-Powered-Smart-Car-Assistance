from typing import List, Dict, Optional, Any
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from app.schemas.common import ApiResponse
from app.services.ai_service import AIService

<<<<<<< HEAD
router = APIRouter(prefix="/ai", tags=["ai"])
=======
<<<<<<< HEAD
router = APIRouter(prefix="/ai", tags=["ai"])
=======
router = APIRouter(prefix="/api/ai", tags=["ai"])
>>>>>>> f82fe05c622b74763ace4d5a0d3f5b82c5a95241
>>>>>>> 839ba178d4aeef05cb4c560f62ca954700b89f58
ai_service = AIService()

class ChatRequest(BaseModel):
    message: str
    history: List[Dict[str, str]] = []

    model_config = {
        "json_schema_extra": {
            "example": {
                "message": "Is the Tata Nexon a good family car?",
                "history": [
                    {"role": "user", "content": "Hi"},
                    {"role": "assistant", "content": "Hello! How can I assist you today?"}
                ]
            }
        }
    }

class RecommendRequest(BaseModel):
    budget: float = Field(..., description="Target budget in INR")
    family_size: int = Field(5, description="Number of passengers")
    commute_distance: float = Field(30.0, description="Daily travel distance in km")
    fuel_preference: str = Field("Petrol", description="Petrol, Diesel, Hybrid, CNG, Electric")
    priorities: List[str] = Field(["Safety", "Mileage"], description="List of priorities: Safety, Mileage, Features, Performance")

    model_config = {
        "json_schema_extra": {
            "example": {
                "budget": 1500000.0,
                "family_size": 4,
                "commute_distance": 25.0,
                "fuel_preference": "Petrol",
                "priorities": ["Safety", "Mileage"]
            }
        }
    }

class CompareRequest(BaseModel):
    car_ids: List[int] = Field(..., description="List of car IDs to compare")
    aspect: Optional[str] = Field(None, description="Aspect to focus: safety, mileage, performance, features")

    model_config = {
        "json_schema_extra": {
            "example": {
                "car_ids": [1, 2],
                "aspect": "safety"
            }
        }
    }

class VoiceRequest(BaseModel):
    message: str = Field(..., description="Speech-to-text input string")

class SmartCompareRequest(BaseModel):
    car_id: int = Field(..., description="Base car ID to compare against")
    budget_range: Optional[List[float]] = Field(None, description="Min and max budget bounds in INR")
    required_features: Optional[List[str]] = Field(default=[], description="Required tech or safety features")

@router.post("/chat", response_model=ApiResponse[Dict[str, Any]])
def ai_chat(payload: ChatRequest):
    try:
        data = ai_service.chat(payload.message, payload.history)
        return ApiResponse(
            success=True,
            data=data,
            message="Chat response generated successfully"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.post("/recommend", response_model=ApiResponse[List[Dict[str, Any]]])
def ai_recommend(payload: RecommendRequest):
    try:
        preferences = {
            "budget": payload.budget,
            "family_size": payload.family_size,
            "commute_distance": payload.commute_distance,
            "fuel_preference": payload.fuel_preference,
            "priorities": payload.priorities
        }
        data = ai_service.recommend(preferences)
        return ApiResponse(
            success=True,
            data=data,
            message="Recommendations computed successfully"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.post("/compare", response_model=ApiResponse[Dict[str, Any]])
def ai_compare(payload: CompareRequest):
    if len(payload.car_ids) < 1 or len(payload.car_ids) > 4:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Must provide between 1 and 4 car IDs to compare."
        )
    try:
        data = ai_service.compare(payload.car_ids, payload.aspect)
        return ApiResponse(
            success=True,
            data=data,
            message="Car comparison generated successfully"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.post("/voice", response_model=ApiResponse[Dict[str, Any]])
def ai_voice(payload: VoiceRequest):
    try:
        data = ai_service.voice_chat(payload.message)
        return ApiResponse(
            success=True,
            data=data,
            message="Voice assistant response computed successfully"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.post("/smart-compare", response_model=ApiResponse[Dict[str, Any]])
def ai_smart_compare(payload: SmartCompareRequest):
    try:
        data = ai_service.smart_compare(
            car_id=payload.car_id,
            budget_range=payload.budget_range,
            required_features=payload.required_features
        )
        return ApiResponse(
            success=True,
            data=data,
            message="Smart budget comparison generated successfully"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
