from datetime import datetime
from sqlalchemy.orm import Session
from app.database.postgres import SessionLocal, Base, engine
from app.models.sql_models import User, Car, Showroom, Booking, WishlistItem, Review, YoutubeSummary, YoutubeReview, YoutubeReviewSummary, CustomerSentiment
from app.services.auth_service import get_password_hash

def seed_postgres():
    print("Seeding PostgreSQL database...")
    # Make sure tables exist
    Base.metadata.create_all(bind=engine)
    
    db: Session = SessionLocal()
    
    # Clear existing tables in correct order
    db.query(Booking).delete()
    db.query(WishlistItem).delete()
    db.query(Showroom).delete()
    db.query(YoutubeReviewSummary).delete()
    db.query(YoutubeReview).delete()
    db.query(CustomerSentiment).delete()
    db.query(YoutubeSummary).delete()
    db.query(Review).delete()
    db.query(Car).delete()
    db.query(User).delete()
    db.commit()
    
    # 1. Seed Users
    admin_user = User(
        name="Admin Assistant",
        email="admin@example.com",
        password_hash=get_password_hash("adminpassword"),
        phone="+919999999999",
        is_admin=True
    )
    test_user = User(
        name="Rohan Sharma",
        email="user@example.com",
        password_hash=get_password_hash("userpassword"),
        phone="+918888888888",
        is_admin=False
    )
    db.add(admin_user)
    db.add(test_user)
    db.commit()
    print("Users seeded.")
    
    # 2. Seed Cars
    cars = [
        Car(
            brand="Tata", model="Nexon", variant="Creative Plus", price=1150000.0, mileage=17.5,
            fuel_type="Petrol", transmission="Manual", engine_specs="1.2L Turbocharged Revotron",
            safety_features=["6 Airbags", "ESP", "ABS with EBD", "5-Star GNCAP Rating"],
            tech_features=["10.25-inch Touchscreen", "Wireless Apple CarPlay/Android Auto", "Digital Console"],
            images=["https://images.unsplash.com/photo-1549399542-7e3f8b79c341?q=80&w=600"]
        ),
        Car(
            brand="Hyundai", model="Creta", variant="SX Tech", price=1680000.0, mileage=16.8,
            fuel_type="Petrol", transmission="Automatic", engine_specs="1.5L MPi Petrol",
            safety_features=["6 Airbags", "ADAS Level 2", "Electronic Stability Control", "All 4 Disc Brakes"],
            tech_features=["Panoramic Sunroof", "Ventilated Seats", "Bose Sound System", "BlueLink Connected Car"],
            images=["https://images.unsplash.com/photo-1533473359331-0135ef1b58bf?q=80&w=600"]
        ),
        Car(
            brand="Maruti Suzuki", model="Swift", variant="ZXI Plus", price=829000.0, mileage=22.4,
            fuel_type="Petrol", transmission="Manual", engine_specs="1.2L Z-Series Petrol",
            safety_features=["6 Airbags", "Hill Hold Assist", "ABS with EBD", "Reverse Parking Camera"],
            tech_features=["9-inch SmartPlay Pro+ Touchscreen", "Wireless Charger", "Suzuki Connect Tech"],
            images=["https://images.unsplash.com/photo-1563720223185-11003d516935?q=80&w=600"]
        ),
        Car(
            brand="Mahindra", model="XUV700", variant="AX7 Luxury", price=2399000.0, mileage=14.2,
            fuel_type="Diesel", transmission="Automatic", engine_specs="2.2L mHawk Diesel",
            safety_features=["7 Airbags", "ADAS Level 2", "360 Degree Camera", "Electronic Park Brake"],
            tech_features=["Dual 10.25-inch Screens", "Amazon Alexa Built-in", "Sony 3D Audio", "Skyroof"],
            images=["https://images.unsplash.com/photo-1617788138017-80ad40651399?q=80&w=600"]
        ),
        Car(
            brand="Toyota", model="Innova Hycross", variant="VX Hybrid", price=2590000.0, mileage=23.2,
            fuel_type="Hybrid", transmission="Automatic", engine_specs="2.0L 5th Gen Hybrid",
            safety_features=["6 Airbags", "Vehicle Stability Control", "Hill Start Assist", "Traction Control"],
            tech_features=["8-inch Display", "Dual-zone AC", "Paddle Shifters", "Panoramic Roof"],
            images=["https://images.unsplash.com/photo-1503376780353-7e6692767b70?q=80&w=600"]
        )
    ]
    
    db.add_all(cars)
    db.commit()
    
    for car in cars:
        db.refresh(car)
        
    car_ids = [car.id for car in cars]
    print(f"{len(cars)} Cars seeded.")
    
    # 3. Seed Showrooms
    showrooms = [
        Showroom(
            name="Bangalore Central Showroom", address="100 Feet Rd, Indiranagar, Bengaluru, Karnataka 560038",
            latitude=12.9716, longitude=77.5946, contact_number="+918049999999",
            available_car_ids=car_ids[0:3]
        ),
        Showroom(
            name="Mumbai South Showroom", address="Colaba Causeway, Apollo Bandar, Colaba, Mumbai, Maharashtra 400001",
            latitude=18.9220, longitude=72.8347, contact_number="+912249999999",
            available_car_ids=car_ids[1:4]
        ),
        Showroom(
            name="Delhi NCR Showroom", address="Connaught Place, New Delhi, Delhi 110001",
            latitude=28.6139, longitude=77.2090, contact_number="+911149999999",
            available_car_ids=car_ids[2:5]
        )
    ]
    db.add_all(showrooms)
    db.commit()
    print("Showrooms seeded.")
    
    # 4. Seed basic Bookings for Rohan
    user_id = test_user.id
    bookings = [
        Booking(
            user_id=user_id, car_id=car_ids[0], showroom_id=1,
            booking_type="test_drive", status="confirmed",
            scheduled_date=datetime(2026, 7, 25, 10, 30, 0)
        ),
        Booking(
            user_id=user_id, car_id=car_ids[1], showroom_id=1,
            booking_type="purchase", status="pending",
            scheduled_date=datetime(2026, 8, 1, 12, 0, 0)
        )
    ]
    db.add_all(bookings)
    
    # 5. Seed Wishlist
    wishlist = [
        WishlistItem(user_id=user_id, car_id=car_ids[0]),
        WishlistItem(user_id=user_id, car_id=car_ids[3])
    ]
    db.add_all(wishlist)
    db.commit()
    print("Bookings and Wishlist seeded.")

    # 6. Seed Reviews (Standard Customer Reviews)
    reviews = [
        Review(
            car_id=car_ids[0],
            user_name="Aarav Mehta",
            rating=4.5,
            comment="Build quality is top notch. Safety is 5-star, which gives me absolute peace of mind.",
            sentiment="Positive"
        ),
        Review(
            car_id=car_ids[1],
            user_name="Rajesh Kumar",
            rating=4.0,
            comment="Very spacious cabin and panoramic sunroof is a hit with family. Soft suspension is great.",
            sentiment="Positive"
        )
    ]
    db.add_all(reviews)
    db.commit()
    print("Standard reviews seeded.")

    # 7. Seed YouTube Reviews (Metadata)
    yt_reviews = [
        YoutubeReview(
            car_id=car_ids[0],  # Tata Nexon
            video_id="mock_vid_1",
            title="Tata Nexon Facelift 2024 - Safe, Techy and Modern Review!",
            thumbnail="https://example.com/nexon_thumb.jpg",
            view_count=185000,
            description="Comprehensive road test and detail specifications of Tata Nexon."
        ),
        YoutubeReview(
            car_id=car_ids[1],  # Hyundai Creta
            video_id="mock_vid_2",
            title="Hyundai Creta Facelift 2024 Review - Is it still the SUV King?",
            thumbnail="https://example.com/creta_thumb.jpg",
            view_count=230000,
            description="Detailed drive review of the new Creta variants and features."
        )
    ]
    db.add_all(yt_reviews)
    db.commit()
    print("YouTube review metadata seeded.")

    # 8. Seed YouTube Review Summaries
    yt_summaries = [
        YoutubeReviewSummary(
            car_id=car_ids[0],  # Tata Nexon
            video_url="https://www.youtube.com/watch?v=mock_vid_1",
            summary_text="Tata Nexon provides class-leading 5-star safety ratings and ground clearance, though AMT can be slow and engine noise is high.",
            pros=["5-star GNCAP safety rating", "208mm ground clearance", "Modern LED layout"],
            cons=["Slow AMT shifts", "Engine noise at high RPMs"],
            mileage_observed="14.5 kmpl (City), 17.2 kmpl (Highway)",
            ride_quality="Stiff suspension setup, high-speed stability is excellent.",
            common_complaints=["AMT shift delay", "Cabin idle vibrations"]
        ),
        YoutubeReviewSummary(
            car_id=car_ids[1],  # Hyundai Creta
            video_url="https://www.youtube.com/watch?v=mock_vid_2",
            summary_text="Hyundai Creta provides an incredibly plush ride quality, high interior refinement, and feature loaded cabin, although top end pricing is high.",
            pros=["Refined motor", "Panoramic sunroof and ventilation", "Plush comfort"],
            cons=["Styling is subjective", "High pricing for top specs"],
            mileage_observed="12.8 kmpl (City), 16.5 kmpl (Highway)",
            ride_quality="Soft and comfortable suspension, digests potholes very well.",
            common_complaints=["Infotainment software lag", "Premium pricing"]
        )
    ]
    db.add_all(yt_summaries)
    db.commit()
    print("YouTube review summaries seeded.")

    # 9. Seed Customer Sentiments
    sentiments = [
        CustomerSentiment(
            car_id=car_ids[0],  # Tata Nexon
            positive_percentage=66.67,
            negative_percentage=16.67,
            neutral_percentage=16.66,
            total_comments_analyzed=6,
            sentiment_summary="Overall customer sentiment for Nexon is positive, highly praising the build quality and safety, with standard warnings regarding transmission shifts."
        ),
        CustomerSentiment(
            car_id=car_ids[1],  # Hyundai Creta
            positive_percentage=83.33,
            negative_percentage=16.67,
            neutral_percentage=0.00,
            total_comments_analyzed=6,
            sentiment_summary="Overall customer sentiment for Creta is highly positive, focused on smooth driving mechanics and premium cabin features, with negative outliers focused on pricing."
        )
    ]
    db.add_all(sentiments)
    db.commit()
    print("Customer sentiments seeded.")
    
    db.close()
    return car_ids

def main():
    print("Starting seeder script...")
    try:
        seed_postgres()
        print("Database seeded successfully!")
    except Exception as e:
        print(f"Error seeding: {e}")

if __name__ == "__main__":
    main()
