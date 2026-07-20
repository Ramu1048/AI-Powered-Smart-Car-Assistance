from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.postgres import get_db
from app.models.sql_models import WishlistItem, User, Car
from app.schemas.wishlist import WishlistCreate, WishlistItemResponse
from app.schemas.common import ApiResponse
from app.routers.auth import get_current_user

router = APIRouter(prefix="/wishlist", tags=["wishlist"])

@router.post("", response_model=ApiResponse[WishlistItemResponse])
def add_to_wishlist(
    wishlist_in: WishlistCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Verify car exists
    car = db.query(Car).filter(Car.id == wishlist_in.car_id).first()
    if not car:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Car with ID {wishlist_in.car_id} not found"
        )
        
    # Check if duplicate
    existing = db.query(WishlistItem).filter(
        WishlistItem.user_id == current_user.id,
        WishlistItem.car_id == wishlist_in.car_id
    ).first()
    
    if existing:
        existing.car = car
        return ApiResponse(
            success=True,
            data=WishlistItemResponse.model_validate(existing),
            message="Car is already in your wishlist"
        )
        
    item = WishlistItem(
        user_id=current_user.id,
        car_id=wishlist_in.car_id
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    item.car = car
    
    return ApiResponse(
        success=True,
        data=WishlistItemResponse.model_validate(item),
        message="Car added to wishlist successfully"
    )

@router.get("/{user_id}", response_model=ApiResponse[List[WishlistItemResponse]])
def get_user_wishlist(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.id != user_id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to view this wishlist"
        )
        
    items = db.query(WishlistItem).filter(WishlistItem.user_id == user_id).all()
    
    for item in items:
        item.car = db.query(Car).filter(Car.id == item.car_id).first()
        
    return ApiResponse(
        success=True,
        data=[WishlistItemResponse.model_validate(item) for item in items],
        message=f"Retrieved {len(items)} wishlist items"
    )

@router.delete("/{id}", response_model=ApiResponse[None])
def delete_wishlist_item(
    id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    item = db.query(WishlistItem).filter(WishlistItem.id == id).first()
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Wishlist item with ID {id} not found"
        )
        
    if item.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to delete this wishlist item"
        )
        
    db.delete(item)
    db.commit()
    
    return ApiResponse(
        success=True,
        data=None,
        message="Wishlist item removed successfully"
    )
