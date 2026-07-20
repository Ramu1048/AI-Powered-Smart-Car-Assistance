from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.database.postgres import get_db
from app.models.sql_models import Car
from app.schemas.car import CarResponse
from app.schemas.common import ApiResponse

router = APIRouter(prefix="/cars", tags=["cars"])

@router.get("", response_model=ApiResponse[List[CarResponse]])
def list_cars(
    brand: Optional[str] = Query(None, description="Filter by car brand"),
    min_price: Optional[float] = Query(None, description="Minimum price in INR"),
    max_price: Optional[float] = Query(None, description="Maximum price in INR"),
    fuel_type: Optional[str] = Query(None, description="Filter by fuel type (e.g. Petrol, Diesel, Electric)"),
    transmission: Optional[str] = Query(None, description="Filter by transmission (Manual, Automatic)"),
    min_mileage: Optional[float] = Query(None, description="Minimum mileage in kmpl"),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    query = db.query(Car)
    
    if brand:
        query = query.filter(Car.brand.ilike(brand))
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
        
    total = query.count()
    cars = query.offset(skip).limit(limit).all()
    
    return ApiResponse(
        success=True,
        data=[CarResponse.model_validate(car) for car in cars],
        message=f"Fetched {len(cars)} cars out of {total} available matching filters"
    )

@router.get("/{id}", response_model=ApiResponse[CarResponse])
def get_car(id: int, db: Session = Depends(get_db)):
    car = db.query(Car).filter(Car.id == id).first()
    if not car:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Car with ID {id} not found"
        )
    return ApiResponse(
        success=True,
        data=CarResponse.model_validate(car),
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
    
    # Simple rule-based similarity logic:
    # 1. Price within +/- 30% of the target car's price
    # 2. Same fuel type or transmission
    # 3. Exclude the car itself
    price_lower_bound = car.price * 0.7
    price_upper_bound = car.price * 1.3
    
    similar_cars = db.query(Car).filter(
        Car.id != id,
        Car.price >= price_lower_bound,
        Car.price <= price_upper_bound,
        or_(
            Car.fuel_type.ilike(car.fuel_type),
            Car.transmission.ilike(car.transmission)
        )
    ).limit(limit).all()
    
    # Fallback: if we find fewer than 2 similar cars, expand price bounds to +/- 50%
    if len(similar_cars) < 2:
        price_lower_bound = car.price * 0.5
        price_upper_bound = car.price * 1.5
        similar_cars = db.query(Car).filter(
            Car.id != id,
            Car.price >= price_lower_bound,
            Car.price <= price_upper_bound
        ).limit(limit).all()
        
    return ApiResponse(
        success=True,
        data=[CarResponse.model_validate(c) for c in similar_cars],
        message=f"Fetched {len(similar_cars)} similar cars"
    )
