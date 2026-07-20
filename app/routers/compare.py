from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.postgres import get_db
from app.models.sql_models import Car
from app.schemas.car import CarResponse, CompareRequest
from app.schemas.common import ApiResponse

router = APIRouter(prefix="/compare", tags=["compare"])

@router.post("", response_model=ApiResponse[List[CarResponse]])
def compare_cars(payload: CompareRequest, db: Session = Depends(get_db)):
    if not payload.car_ids:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="car_ids list cannot be empty"
        )
        
    cars = db.query(Car).filter(Car.id.in_(payload.car_ids)).all()
    
    id_to_car = {car.id: car for car in cars}
    sorted_cars = []
    missing_ids = []
    
    for car_id in payload.car_ids:
        if car_id in id_to_car:
            sorted_cars.append(id_to_car[car_id])
        else:
            missing_ids.append(car_id)
            
    if missing_ids:
        message = f"Compared {len(sorted_cars)} cars. Warning: Car IDs {missing_ids} not found."
    else:
        message = f"Compared {len(sorted_cars)} cars successfully"
        
    return ApiResponse(
        success=True,
        data=[CarResponse.model_validate(car) for car in sorted_cars],
        message=message
    )
