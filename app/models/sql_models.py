from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.postgres import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    bookings = relationship("Booking", back_populates="user", cascade="all, delete-orphan")
    wishlist_items = relationship("WishlistItem", back_populates="user", cascade="all, delete-orphan")

class Car(Base):
    __tablename__ = "cars"

    id = Column(Integer, primary_key=True, index=True)
    brand = Column(String, nullable=False, index=True)
    model = Column(String, nullable=False, index=True)
    variant = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    mileage = Column(Float, nullable=True)
    fuel_type = Column(String, nullable=False)
    transmission = Column(String, nullable=False)
    engine_specs = Column(String, nullable=True)
    safety_features = Column(JSON, nullable=True)  # List of safety features
    tech_features = Column(JSON, nullable=True)    # List of technology features
    images = Column(JSON, nullable=True)           # List of image URLs

    # --- Expanded Specification Fields ---
    body_type = Column(String, nullable=True)      # Hatchback, Sedan, SUV, MPV, etc.
    seating_capacity = Column(Integer, nullable=True, default=5)
    ncap_rating = Column(Float, nullable=True)     # Global NCAP star rating (0-5)
    dimensions = Column(JSON, nullable=True)       # {length_mm, width_mm, height_mm, wheelbase_mm, ground_clearance_mm, boot_space_litres}
    engine_details = Column(JSON, nullable=True)   # {capacity_cc, max_power_bhp, max_torque_nm, cylinders, transmission_type}
    adas_features = Column(JSON, nullable=True)    # List of ADAS features
    comfort_features = Column(JSON, nullable=True) # {sunroof_type, ventilated_seats, drive_modes, touchscreen_size_inches, digital_cluster}

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    bookings = relationship("Booking", back_populates="car", cascade="all, delete-orphan")
    wishlist_items = relationship("WishlistItem", back_populates="car", cascade="all, delete-orphan")
    reviews = relationship("Review", back_populates="car", cascade="all, delete-orphan")
    youtube_summaries = relationship("YoutubeSummary", back_populates="car", cascade="all, delete-orphan")
    youtube_reviews = relationship("YoutubeReview", back_populates="car", cascade="all, delete-orphan")
    youtube_review_summaries = relationship("YoutubeReviewSummary", back_populates="car", cascade="all, delete-orphan")
    customer_sentiments = relationship("CustomerSentiment", back_populates="car", cascade="all, delete-orphan")

class Showroom(Base):
    __tablename__ = "showrooms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    contact_number = Column(String, nullable=True)
    available_car_ids = Column(JSON, nullable=True)  # List of integer car IDs available

    bookings = relationship("Booking", back_populates="showroom", cascade="all, delete-orphan")

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    car_id = Column(Integer, ForeignKey("cars.id", ondelete="CASCADE"), nullable=False)
    showroom_id = Column(Integer, ForeignKey("showrooms.id", ondelete="CASCADE"), nullable=False)
    booking_type = Column(String, nullable=False)  # test_drive or purchase
    status = Column(String, default="pending", nullable=False)  # pending, confirmed, cancelled
    scheduled_date = Column(DateTime, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="bookings")
    car = relationship("Car", back_populates="bookings")
    showroom = relationship("Showroom", back_populates="bookings")

class WishlistItem(Base):
    __tablename__ = "wishlists"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    car_id = Column(Integer, ForeignKey("cars.id", ondelete="CASCADE"), nullable=False)

    user = relationship("User", back_populates="wishlist_items")
    car = relationship("Car", back_populates="wishlist_items")

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    car_id = Column(Integer, ForeignKey("cars.id", ondelete="CASCADE"), nullable=False)
    user_name = Column(String, nullable=False)
    rating = Column(Float, nullable=False)
    comment = Column(String, nullable=False)
    sentiment = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    car = relationship("Car", back_populates="reviews")

class YoutubeSummary(Base):
    __tablename__ = "youtube_summaries"

    id = Column(Integer, primary_key=True, index=True)
    car_id = Column(Integer, ForeignKey("cars.id", ondelete="CASCADE"), nullable=False)
    video_url = Column(String, nullable=False)
    summary_text = Column(String, nullable=False)
    pros = Column(JSON, nullable=True)
    cons = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    car = relationship("Car", back_populates="youtube_summaries")

class YoutubeReview(Base):
    __tablename__ = "youtube_reviews"

    id = Column(Integer, primary_key=True, index=True)
    car_id = Column(Integer, ForeignKey("cars.id", ondelete="CASCADE"), nullable=False)
    video_id = Column(String, unique=True, index=True, nullable=False)
    title = Column(String, nullable=False)
    thumbnail = Column(String, nullable=True)
    view_count = Column(Integer, nullable=True)
    description = Column(String, nullable=True)
    # --- YouTube Channel & Video Redirection Fields ---
    channel_name = Column(String, nullable=True)
    channel_url = Column(String, nullable=True)
    video_url = Column(String, nullable=True)  # Full YouTube video URL
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    car = relationship("Car", back_populates="youtube_reviews")

class YoutubeReviewSummary(Base):
    __tablename__ = "youtube_review_summaries"

    id = Column(Integer, primary_key=True, index=True)
    car_id = Column(Integer, ForeignKey("cars.id", ondelete="CASCADE"), nullable=False)
    video_url = Column(String, nullable=False)
    summary_text = Column(String, nullable=False)
    pros = Column(JSON, nullable=True)
    cons = Column(JSON, nullable=True)
    mileage_observed = Column(String, nullable=True)
    ride_quality = Column(String, nullable=True)
    common_complaints = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    car = relationship("Car", back_populates="youtube_review_summaries")

class CustomerSentiment(Base):
    __tablename__ = "customer_sentiments"

    id = Column(Integer, primary_key=True, index=True)
    car_id = Column(Integer, ForeignKey("cars.id", ondelete="CASCADE"), nullable=False)
    positive_percentage = Column(Float, nullable=False)
    negative_percentage = Column(Float, nullable=False)
    neutral_percentage = Column(Float, nullable=False)
    total_comments_analyzed = Column(Integer, nullable=False)
    sentiment_summary = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    car = relationship("Car", back_populates="customer_sentiments")
