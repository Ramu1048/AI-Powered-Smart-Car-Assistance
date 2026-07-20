from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.postgres import get_db
from app.models.sql_models import User, Car, Booking, Showroom
from app.schemas.car import CarCreate, CarUpdate, CarResponse
from app.schemas.booking import BookingResponse
from app.schemas.common import ApiResponse
from app.routers.auth import get_admin_user

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/cars", response_model=ApiResponse[List[CarResponse]])
def admin_list_cars(
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_admin_user)
):
    cars = db.query(Car).all()
    return ApiResponse(
        success=True,
        data=[CarResponse.model_validate(car) for car in cars],
        message=f"Fetched {len(cars)} cars for admin panel"
    )

@router.post("/cars", response_model=ApiResponse[CarResponse])
def admin_create_car(
    car_in: CarCreate,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_admin_user)
):
    new_car = Car(
        brand=car_in.brand,
        model=car_in.model,
        variant=car_in.variant,
        price=car_in.price,
        mileage=car_in.mileage,
        fuel_type=car_in.fuel_type,
        transmission=car_in.transmission,
        engine_specs=car_in.engine_specs,
        safety_features=car_in.safety_features,
        tech_features=car_in.tech_features,
        images=car_in.images
    )
    db.add(new_car)
    db.commit()
    db.refresh(new_car)
    
    return ApiResponse(
        success=True,
        data=CarResponse.model_validate(new_car),
        message="Car created successfully"
    )

@router.put("/cars/{id}", response_model=ApiResponse[CarResponse])
def admin_update_car(
    id: int,
    car_in: CarUpdate,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_admin_user)
):
    car = db.query(Car).filter(Car.id == id).first()
    if not car:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Car with ID {id} not found"
        )
        
    update_data = car_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(car, key, value)
        
    db.commit()
    db.refresh(car)
    
    return ApiResponse(
        success=True,
        data=CarResponse.model_validate(car),
        message="Car details updated successfully"
    )

@router.delete("/cars/{id}", response_model=ApiResponse[None])
def admin_delete_car(
    id: int,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_admin_user)
):
    car = db.query(Car).filter(Car.id == id).first()
    if not car:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Car with ID {id} not found"
        )
        
    db.delete(car)
    db.commit()
    
    return ApiResponse(
        success=True,
        data=None,
        message="Car deleted successfully"
    )

@router.get("/bookings", response_model=ApiResponse[List[BookingResponse]])
def admin_get_bookings(
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_admin_user)
):
    bookings = db.query(Booking).order_by(Booking.created_at.desc()).all()
    
    for b in bookings:
        b.car = db.query(Car).filter(Car.id == b.car_id).first()
        b.showroom = db.query(Showroom).filter(Showroom.id == b.showroom_id).first()
        
    return ApiResponse(
        success=True,
        data=[BookingResponse.model_validate(b) for b in bookings],
        message=f"Retrieved all {len(bookings)} bookings globally"
    )
