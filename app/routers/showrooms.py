from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.database.postgres import get_db
from app.models.sql_models import Showroom, Car
from app.schemas.showroom import ShowroomNearbyResponse, ShowroomResponse
from app.schemas.car import CarResponse
from app.schemas.common import ApiResponse
from app.services.distance import calculate_haversine_distance

router = APIRouter(prefix="/showrooms", tags=["showrooms"])

@router.get("/nearby", response_model=ApiResponse[List[ShowroomNearbyResponse]])
def get_nearby_showrooms(
    latitude: float = Query(..., description="Latitude of user"),
    longitude: float = Query(..., description="Longitude of user"),
    radius_km: float = Query(50.0, description="Search radius in kilometers"),
    db: Session = Depends(get_db)
):
    showrooms = db.query(Showroom).all()
    nearby_showrooms = []
    
    for showroom in showrooms:
        distance = calculate_haversine_distance(
            latitude, longitude, showroom.latitude, showroom.longitude
        )
        if distance <= radius_km:
            showroom_data = ShowroomResponse.model_validate(showroom)
            nearby_data = ShowroomNearbyResponse(
                id=showroom_data.id,
                name=showroom_data.name,
                address=showroom_data.address,
                latitude=showroom_data.latitude,
                longitude=showroom_data.longitude,
                contact_number=showroom_data.contact_number,
                available_car_ids=showroom_data.available_car_ids or [],
                distance_km=round(distance, 2)
            )
            nearby_showrooms.append(nearby_data)
            
    # Sort by distance
    nearby_showrooms.sort(key=lambda x: x.distance_km)
    
    return ApiResponse(
        success=True,
        data=nearby_showrooms,
        message=f"Found {len(nearby_showrooms)} showrooms within {radius_km} km"
    )

@router.get("/{id}/availability", response_model=ApiResponse[List[CarResponse]])
def get_showroom_availability(id: int, db: Session = Depends(get_db)):
    showroom = db.query(Showroom).filter(Showroom.id == id).first()
    if not showroom:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Showroom with ID {id} not found"
        )
        
    car_ids = showroom.available_car_ids or []
    if not car_ids:
        return ApiResponse(
            success=True,
            data=[],
            message="No cars available at this showroom currently"
        )
        
    cars = db.query(Car).filter(Car.id.in_(car_ids)).all()
    return ApiResponse(
        success=True,
        data=[CarResponse.model_validate(car) for car in cars],
        message=f"Found {len(cars)} cars available at showroom '{showroom.name}'"
    )
