from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.postgres import get_db
from app.models.sql_models import Booking, User, Car, Showroom
from app.schemas.booking import BookingCreate, BookingResponse
from app.schemas.common import ApiResponse
from app.routers.auth import get_current_user

router = APIRouter(prefix="/bookings", tags=["bookings"])

@router.post("", response_model=ApiResponse[BookingResponse])
def create_booking(
    booking_in: BookingCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Verify car exists
    car = db.query(Car).filter(Car.id == booking_in.car_id).first()
    if not car:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Car with ID {booking_in.car_id} not found"
        )
        
    # Verify showroom exists
    showroom = db.query(Showroom).filter(Showroom.id == booking_in.showroom_id).first()
    if not showroom:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Showroom with ID {booking_in.showroom_id} not found"
        )

    new_booking = Booking(
        user_id=current_user.id,
        car_id=booking_in.car_id,
        showroom_id=booking_in.showroom_id,
        booking_type=booking_in.booking_type,
        status="pending",
        scheduled_date=booking_in.scheduled_date
    )
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    
    # Pre-populate relationships for schema mapping
    new_booking.car = car
    new_booking.showroom = showroom
    
    return ApiResponse(
        success=True,
        data=BookingResponse.model_validate(new_booking),
        message=f"Booking ({booking_in.booking_type}) submitted successfully"
    )

@router.get("/{user_id}", response_model=ApiResponse[List[BookingResponse]])
def get_user_bookings(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Check permissions
    if current_user.id != user_id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to view this booking history"
        )
        
    bookings = db.query(Booking).filter(Booking.user_id == user_id).order_by(Booking.created_at.desc()).all()
    
    return ApiResponse(
        success=True,
        data=[BookingResponse.model_validate(b) for b in bookings],
        message=f"Retrieved {len(bookings)} booking records"
    )
