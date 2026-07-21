from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_
from app.database.postgres import get_db
from app.models.sql_models import Car, YoutubeReview
from app.schemas.car import CarResponse, YoutubeReviewResponse
from app.schemas.common import ApiResponse

router = APIRouter(prefix="/cars", tags=["cars"])

def _car_to_response(car: Car) -> CarResponse:
    """Convert a Car ORM object to CarResponse, including YouTube review metadata."""
    yt_reviews = []
    for yt in (car.youtube_reviews or []):
        yt_reviews.append(YoutubeReviewResponse(
            channel_name=yt.channel_name,
            video_title=yt.title,
            video_url=yt.video_url or f"https://www.youtube.com/watch?v={yt.video_id}",
            channel_url=yt.channel_url,
            thumbnail_url=yt.thumbnail or f"https://img.youtube.com/vi/{yt.video_id}/hqdefault.jpg"
        ))
    
    car_dict = {
        "id": car.id,
        "brand": car.brand,
        "model": car.model,
        "variant": car.variant,
        "price": car.price,
        "mileage": car.mileage,
        "fuel_type": car.fuel_type,
        "transmission": car.transmission,
        "engine_specs": car.engine_specs,
        "safety_features": car.safety_features or [],
        "tech_features": car.tech_features or [],
        "images": car.images or [],
        "body_type": car.body_type,
        "seating_capacity": car.seating_capacity,
        "ncap_rating": car.ncap_rating,
        "dimensions": car.dimensions,
        "engine_details": car.engine_details,
        "adas_features": car.adas_features or [],
        "comfort_features": car.comfort_features,
        "created_at": car.created_at,
        "youtube_reviews": yt_reviews,
    }
    return CarResponse(**car_dict)

@router.get("", response_model=ApiResponse[List[CarResponse]])
def list_cars(
    brand: Optional[str] = Query(None, description="Filter by car brand"),
    body_type: Optional[str] = Query(None, description="Filter by body type (Hatchback, Sedan, SUV, MPV)"),
    min_price: Optional[float] = Query(None, description="Minimum price in INR"),
    max_price: Optional[float] = Query(None, description="Maximum price in INR"),
    fuel_type: Optional[str] = Query(None, description="Filter by fuel type (e.g. Petrol, Diesel, Electric)"),
    transmission: Optional[str] = Query(None, description="Filter by transmission (Manual, Automatic)"),
    min_mileage: Optional[float] = Query(None, description="Minimum mileage in kmpl"),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db)
):
    query = db.query(Car).options(joinedload(Car.youtube_reviews))
    
    if brand:
        query = query.filter(Car.brand.ilike(brand))
    if body_type:
        query = query.filter(Car.body_type.ilike(body_type))
    if min_price is not None:
        query = query.filter(Car.price >= min_price)
    if max_price is not None:
        query = query.filter(Car.price <= max_price)
    if fuel_type:
        query = query.filter(Car.fuel_type.ilike(fuel_type))
    if transmission:
        query = query.filter(Car.transmission.ilike(transmission))
    if min_mileage is not None:
        query = query.filter(Car.mileage >= min_mileage)
        
    # Use unique() due to joinedload causing duplicates with collection
    cars = query.offset(skip).limit(limit).all()
    unique_cars = list({car.id: car for car in cars}.values())
    total = db.query(Car).count()
    
    return ApiResponse(
        success=True,
        data=[_car_to_response(car) for car in unique_cars],
        message=f"Fetched {len(unique_cars)} cars out of {total} available matching filters"
    )

@router.get("/{id}", response_model=ApiResponse[CarResponse])
def get_car(id: int, db: Session = Depends(get_db)):
    car = db.query(Car).options(joinedload(Car.youtube_reviews)).filter(Car.id == id).first()
    if not car:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Car with ID {id} not found"
        )
    return ApiResponse(
        success=True,
        data=_car_to_response(car),
        message="Car details fetched successfully"
    )

@router.get("/{id}/similar", response_model=ApiResponse[List[CarResponse]])
def get_similar_cars(id: int, limit: int = Query(4, ge=1, le=10), db: Session = Depends(get_db)):
    car = db.query(Car).filter(Car.id == id).first()
    if not car:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Car with ID {id} not found"
        )
    
    # Rule-based similarity: price within +/- 30%, same fuel type or body type
    price_lower_bound = car.price * 0.7
    price_upper_bound = car.price * 1.3
    
    similar_query = db.query(Car).options(joinedload(Car.youtube_reviews)).filter(
        Car.id != id,
        Car.price >= price_lower_bound,
        Car.price <= price_upper_bound,
        or_(
            Car.fuel_type.ilike(car.fuel_type),
            Car.body_type.ilike(car.body_type) if car.body_type else Car.transmission.ilike(car.transmission)
        )
    ).limit(limit)
    
    similar_cars = similar_query.all()
    
    # Fallback: if fewer than 2 similar cars, expand price bounds to +/- 50%
    if len(similar_cars) < 2:
        price_lower_bound = car.price * 0.5
        price_upper_bound = car.price * 1.5
        similar_cars = db.query(Car).options(joinedload(Car.youtube_reviews)).filter(
            Car.id != id,
            Car.price >= price_lower_bound,
            Car.price <= price_upper_bound
        ).limit(limit).all()
        
    return ApiResponse(
        success=True,
        data=[_car_to_response(c) for c in similar_cars],
        message=f"Fetched {len(similar_cars)} similar cars"
    )
