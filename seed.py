from datetime import datetime
from sqlalchemy.orm import Session
from app.database.postgres import SessionLocal, Base, engine
from app.models.sql_models import User, Car, Showroom, Booking, WishlistItem, Review, YoutubeSummary, YoutubeReview, YoutubeReviewSummary, CustomerSentiment
from app.services.auth_service import get_password_hash

def seed_postgres():
<<<<<<< HEAD
    print("=== HARD RESET: Dropping all tables and re-creating from scratch ===")
    Base.metadata.drop_all(bind=engine)
=======
    print("Seeding PostgreSQL database...")
    # Make sure tables exist
>>>>>>> f82fe05c622b74763ace4d5a0d3f5b82c5a95241
    Base.metadata.create_all(bind=engine)
    
    db: Session = SessionLocal()
    
<<<<<<< HEAD
=======
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
    
>>>>>>> f82fe05c622b74763ace4d5a0d3f5b82c5a95241
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
<<<<<<< HEAD
    print("[OK] Users seeded.")
    
    # 2. Seed Cars
    # IMPORTANT: Images are served from frontend/public/cars/ via the same origin.
    # These are AI-generated brand-specific images, NOT random stock photos.
    cars = [
        Car(
            brand="Maruti Suzuki", model="Dzire", variant="ZXi", price=850000.0, mileage=22.4,
            fuel_type="Petrol", transmission="Manual", engine_specs="1.2L DualJet Petrol",
            safety_features=["2 Airbags", "ESP", "Hill Hold Assist", "ABS with EBD", "Reverse Parking Sensors"],
            tech_features=["7-inch SmartPlay Studio", "Automatic Climate Control", "Steering Mounted Controls", "Keyless Entry"],
            images=["/cars/maruti_suzuki_dzire.png"]
        ),
        Car(
            brand="Volkswagen", model="Virtus", variant="GT Plus", price=1900000.0, mileage=18.2,
            fuel_type="Petrol", transmission="Automatic", engine_specs="1.5L TSI EVO Petrol",
            safety_features=["6 Airbags", "5-Star GNCAP Rating", "Electronic Stability Control", "Multi-Collision Brakes"],
            tech_features=["10-inch Infotainment Screen", "Digital Cockpit Console", "Wireless Charging", "Sunroof", "Ventilated Seats"],
            images=["/cars/volkswagen_virtus.png"]
=======
    print("Users seeded.")
    
    # 2. Seed Cars
    cars = [
        Car(
            brand="Tata", model="Nexon", variant="Creative Plus", price=1150000.0, mileage=17.5,
            fuel_type="Petrol", transmission="Manual", engine_specs="1.2L Turbocharged Revotron",
            safety_features=["6 Airbags", "ESP", "ABS with EBD", "5-Star GNCAP Rating"],
            tech_features=["10.25-inch Touchscreen", "Wireless Apple CarPlay/Android Auto", "Digital Console"],
            images=["https://images.unsplash.com/photo-1549399542-7e3f8b79c341?q=80&w=600"]
>>>>>>> f82fe05c622b74763ace4d5a0d3f5b82c5a95241
        ),
        Car(
            brand="Hyundai", model="Creta", variant="SX Tech", price=1680000.0, mileage=16.8,
            fuel_type="Petrol", transmission="Automatic", engine_specs="1.5L MPi Petrol",
<<<<<<< HEAD
            safety_features=["6 Airbags", "ADAS Level 2", "Electronic Stability Control", "All 4 Disc Brakes", "TPMS"],
            tech_features=["Panoramic Sunroof", "Ventilated Seats", "Bose Sound System", "BlueLink Connected Car", "Wireless Charger"],
            images=["/cars/hyundai_creta.png"]
        ),
        Car(
            brand="Tata", model="Nexon", variant="Fearless", price=1450000.0, mileage=17.0,
            fuel_type="Petrol", transmission="Automatic", engine_specs="1.2L Turbocharged Revotron",
            safety_features=["6 Airbags", "360 Degree Camera", "ESP", "ABS with EBD", "5-Star GNCAP Rating"],
            tech_features=["10.25-inch Touchscreen", "Wireless Apple CarPlay/Android Auto", "JBL Sound System", "Voice Assisted Sunroof"],
            images=["/cars/tata_nexon.png"]
        ),
=======
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
>>>>>>> f82fe05c622b74763ace4d5a0d3f5b82c5a95241
    ]
    
    db.add_all(cars)
    db.commit()
    
    for car in cars:
        db.refresh(car)
        
    car_ids = [car.id for car in cars]
<<<<<<< HEAD
    print(f"[OK] {len(cars)} Cars seeded with brand-specific local images.")
    
    # Print verification table immediately
    print("\n--- SEED VERIFICATION TABLE ---")
    print(f"{'ID':<4} {'Brand':<18} {'Model':<12} {'Variant':<12} {'Image Path'}")
    print("-" * 80)
    for car in cars:
        img = car.images[0] if car.images else "MISSING"
        print(f"{car.id:<4} {car.brand:<18} {car.model:<12} {car.variant:<12} {img}")
    print("-" * 80 + "\n")
    
    # 3. Seed Localized Nearby Showrooms (3 cities)
    showrooms = [
        # Bangalore
        Showroom(
            name="Bangalore Indiranagar Showroom", address="100 Feet Rd, Indiranagar, Bengaluru, Karnataka 560038",
            latitude=12.97189, longitude=77.64115, contact_number="+918049999901",
            available_car_ids=car_ids
        ),
        Showroom(
            name="Bangalore Central Showroom", address="Residency Rd, Ashok Nagar, Bengaluru, Karnataka 560025",
            latitude=12.9716, longitude=77.5946, contact_number="+918049999902",
            available_car_ids=car_ids
        ),
        Showroom(
            name="Bangalore Whitefield Showroom", address="ITPL Main Rd, Whitefield, Bengaluru, Karnataka 560066",
            latitude=12.9868, longitude=77.7500, contact_number="+918049999903",
            available_car_ids=car_ids
        ),
        # Mumbai
        Showroom(
            name="Mumbai Colaba Showroom", address="Colaba Causeway, Apollo Bandar, Colaba, Mumbai, Maharashtra 400001",
            latitude=18.9220, longitude=72.8347, contact_number="+912249999901",
            available_car_ids=car_ids
        ),
        Showroom(
            name="Mumbai Bandra Showroom", address="Linking Rd, Bandra West, Mumbai, Maharashtra 400050",
            latitude=19.0596, longitude=72.8295, contact_number="+912249999902",
            available_car_ids=car_ids
        ),
        # Delhi
        Showroom(
            name="Delhi Connaught Place Showroom", address="Connaught Place, New Delhi, Delhi 110001",
            latitude=28.6139, longitude=77.2090, contact_number="+911149999901",
            available_car_ids=car_ids
        ),
        Showroom(
            name="Delhi Gurugram Showroom", address="Sector 29, Gurugram, Haryana 122001",
            latitude=28.4595, longitude=77.0266, contact_number="+911149999903",
            available_car_ids=car_ids
        ),
    ]
    db.add_all(showrooms)
    db.commit()
    print(f"[OK] {len(showrooms)} Showrooms seeded.")
    
    # 4. Seed Bookings
    user_id = test_user.id
    bookings = [
        Booking(user_id=user_id, car_id=car_ids[0], showroom_id=1, booking_type="test_drive", status="confirmed", scheduled_date=datetime(2026, 7, 25, 10, 30, 0)),
=======
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
>>>>>>> f82fe05c622b74763ace4d5a0d3f5b82c5a95241
    ]
    db.add_all(bookings)
    
    # 5. Seed Wishlist
<<<<<<< HEAD
    wishlist = [WishlistItem(user_id=user_id, car_id=car_ids[0])]
    db.add_all(wishlist)
    db.commit()
    print("[OK] Bookings and Wishlist seeded.")

    # 6. Seed Reviews
    reviews = [
        Review(car_id=car_ids[0], user_name="Aarav Mehta", rating=4.5, comment="Dzire cabin is very comfortable for daily city commute. The mileage is outstanding.", sentiment="Positive"),
        Review(car_id=car_ids[1], user_name="Rajesh Kumar", rating=5.0, comment="Virtus GT high speed stability and performance is absolute premium. Build quality is solid.", sentiment="Positive"),
        Review(car_id=car_ids[2], user_name="Priya Nair", rating=4.0, comment="Creta ADAS features and panoramic sunroof are the highlights. Very comfortable on highways.", sentiment="Positive"),
        Review(car_id=car_ids[3], user_name="Vikram Singh", rating=4.5, comment="Nexon 5-star safety rating gives immense peace of mind. Love the build quality.", sentiment="Positive"),
    ]
    db.add_all(reviews)
    db.commit()
    print("[OK] Reviews seeded.")

    # 7. Seed YouTube Reviews
    yt_reviews = [
        YoutubeReview(car_id=car_ids[0], video_id="dzire_2024", title="Maruti Suzuki Dzire 2024 Real World Mileage Test", thumbnail="", view_count=150000, description=""),
        YoutubeReview(car_id=car_ids[1], video_id="virtus_gt_2024", title="Volkswagen Virtus GT - The Driver's Sedan!", thumbnail="", view_count=210000, description=""),
        YoutubeReview(car_id=car_ids[2], video_id="creta_2024", title="Hyundai Creta Facelift - Is it still King?", thumbnail="", view_count=230000, description=""),
        YoutubeReview(car_id=car_ids[3], video_id="nexon_2024", title="Tata Nexon Fearless - Safe, Techy, Modern!", thumbnail="", view_count=185000, description=""),
    ]
    db.add_all(yt_reviews)
    db.commit()
    print("[OK] YouTube review metadata seeded.")
=======
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
>>>>>>> f82fe05c622b74763ace4d5a0d3f5b82c5a95241

    # 8. Seed YouTube Review Summaries
    yt_summaries = [
        YoutubeReviewSummary(
<<<<<<< HEAD
            car_id=car_ids[0], video_url="https://youtube.com/watch?v=dzire_2024",
            summary_text="Maruti Suzuki Dzire delivers class-leading city mileage and a soft, comfortable ride, though high-speed highway stability is average.",
            pros=["Excellent fuel economy", "Light and easy steering", "Spacious cabin rear legroom"],
            cons=["Average build sheet metal", "Bumpy ride at high speeds"],
            mileage_observed="18.5 kmpl (City), 22.1 kmpl (Highway)",
            ride_quality="Soft suspension, highly suited for city traffic.",
            common_complaints=["Engine noise above 3000 RPM", "Light build quality"]
        ),
        YoutubeReviewSummary(
            car_id=car_ids[1], video_url="https://youtube.com/watch?v=virtus_gt_2024",
            summary_text="Volkswagen Virtus GT delivers outstanding highway stability, sharp cornering, and premium cabin, though pricing is high.",
            pros=["High speed stability", "Punchy TSI performance", "5-star crash safety"],
            cons=["Premium price tag", "Stiff low-speed suspension"],
            mileage_observed="12.5 kmpl (City), 17.8 kmpl (Highway)",
            ride_quality="Stiff suspension, excellent high speed dynamics.",
            common_complaints=["Stiff low-speed ride", "High maintenance cost"]
        ),
        YoutubeReviewSummary(
            car_id=car_ids[2], video_url="https://youtube.com/watch?v=creta_2024",
            summary_text="Hyundai Creta provides an incredibly plush ride, high interior refinement, and feature loaded cabin, though top-end pricing is high.",
            pros=["Refined engine", "Panoramic sunroof", "Plush comfort"],
            cons=["Styling is subjective", "High pricing for top specs"],
            mileage_observed="12.8 kmpl (City), 16.5 kmpl (Highway)",
            ride_quality="Soft and comfortable suspension, digests potholes well.",
            common_complaints=["Infotainment lag", "Premium pricing"]
        ),
        YoutubeReviewSummary(
            car_id=car_ids[3], video_url="https://youtube.com/watch?v=nexon_2024",
            summary_text="Tata Nexon provides class-leading 5-star safety and ground clearance, though AMT can be slow and engine noise is high.",
            pros=["5-star GNCAP safety", "208mm ground clearance", "Modern LED design"],
            cons=["Slow AMT shifts", "Engine noise at high RPMs"],
            mileage_observed="14.5 kmpl (City), 17.2 kmpl (Highway)",
            ride_quality="Stiff suspension, excellent high-speed stability.",
            common_complaints=["AMT shift delay", "Cabin idle vibrations"]
        ),
    ]
    db.add_all(yt_summaries)
    db.commit()
    print("[OK] YouTube review summaries seeded.")

    # 9. Seed Customer Sentiments
    sentiments = [
        CustomerSentiment(car_id=car_ids[0], positive_percentage=80.0, negative_percentage=10.0, neutral_percentage=10.0, total_comments_analyzed=10, sentiment_summary="Highly positive feedback focused on low ownership costs and fuel efficiency."),
        CustomerSentiment(car_id=car_ids[1], positive_percentage=90.0, negative_percentage=10.0, neutral_percentage=0.0, total_comments_analyzed=10, sentiment_summary="Extremely positive for German driving dynamics, stability, and aesthetics."),
        CustomerSentiment(car_id=car_ids[2], positive_percentage=83.0, negative_percentage=10.0, neutral_percentage=7.0, total_comments_analyzed=10, sentiment_summary="Highly positive for comfort, features, and brand trust."),
        CustomerSentiment(car_id=car_ids[3], positive_percentage=75.0, negative_percentage=15.0, neutral_percentage=10.0, total_comments_analyzed=10, sentiment_summary="Positive for safety and build quality. Minor complaints on transmission."),
    ]
    db.add_all(sentiments)
    db.commit()
    print("[OK] Customer sentiments seeded.")
    
    db.close()
    print("\n=== DATABASE SEEDED SUCCESSFULLY ===")
    return car_ids

def main():
    try:
        seed_postgres()
    except Exception as e:
        print(f"[ERROR] Seeding failed: {e}")
        import traceback
        traceback.print_exc()
=======
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
>>>>>>> f82fe05c622b74763ace4d5a0d3f5b82c5a95241

if __name__ == "__main__":
    main()
