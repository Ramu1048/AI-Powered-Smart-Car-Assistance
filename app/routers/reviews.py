from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.postgres import get_db
from app.models.sql_models import User, Review, YoutubeSummary
from app.schemas.review import ReviewCreate, ReviewResponse, YoutubeSummaryResponse
from app.schemas.common import ApiResponse
from app.routers.auth import get_current_user

router = APIRouter(prefix="/cars", tags=["reviews"])

@router.get("/{id}/reviews", response_model=ApiResponse[List[ReviewResponse]])
def get_car_reviews(id: int, db: Session = Depends(get_db)):
    reviews = db.query(Review).filter(Review.car_id == id).all()
    return ApiResponse(
        success=True,
        data=[ReviewResponse.model_validate(r) for r in reviews],
        message=f"Fetched {len(reviews)} reviews from PostgreSQL"
    )

@router.post("/{id}/reviews", response_model=ApiResponse[ReviewResponse])
def add_car_review(
    id: int,
    review_in: ReviewCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if review_in.rating >= 4.0:
        sentiment = "Positive"
    elif review_in.rating <= 2.5:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"
        
    new_review = Review(
        car_id=id,
        user_name=current_user.name,
        rating=review_in.rating,
        comment=review_in.comment,
        sentiment=sentiment
    )
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    
    return ApiResponse(
        success=True,
        data=ReviewResponse.model_validate(new_review),
        message="Review submitted and saved to PostgreSQL"
    )

@router.get("/{id}/youtube-summary", response_model=ApiResponse[YoutubeSummaryResponse])
def get_youtube_summary(id: int, db: Session = Depends(get_db)):
    doc = db.query(YoutubeSummary).filter(YoutubeSummary.car_id == id).first()
    if not doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"YouTube summary not found for car ID {id}"
        )
        
    return ApiResponse(
        success=True,
        data=YoutubeSummaryResponse.model_validate(doc),
        message="YouTube review summary fetched from PostgreSQL"
    )
