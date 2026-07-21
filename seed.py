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
<<<<<<< HEAD
    print("=== HARD RESET: Dropping all tables and re-creating from scratch ===")
    Base.metadata.drop_all(bind=engine)
=======
    print("Seeding PostgreSQL database...")
    # Make sure tables exist
>>>>>>> f82fe05c622b74763ace4d5a0d3f5b82c5a95241
>>>>>>> 839ba178d4aeef05cb4c560f62ca954700b89f58
    Base.metadata.create_all(bind=engine)
    
    db: Session = SessionLocal()
    
<<<<<<< HEAD
=======
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
>>>>>>> 839ba178d4aeef05cb4c560f62ca954700b89f58
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
    
    # 2. Seed 30 Cars representing all major Indian brands and models
    cars_data = [
        # --- Maruti Suzuki ---
        {
            "brand": "Maruti Suzuki", "model": "Swift", "variant": "VXi", "price": 720000.0, "mileage": 22.38,
            "fuel_type": "Petrol", "transmission": "Manual", "engine_specs": "1.2L Z-Series Petrol",
            "safety_features": ["6 Airbags", "ABS with EBD", "Hill Hold Assist", "ESP"],
            "tech_features": ["7-inch Touchscreen", "Steering Mounted Controls", "Keyless Entry"],
            "images": ["/cars/maruti_suzuki_swift.png"], "body_type": "Hatchback", "seating_capacity": 5, "ncap_rating": 3.0,
            "dimensions": {"length_mm": 3860, "width_mm": 1735, "height_mm": 1520, "wheelbase_mm": 2450, "ground_clearance_mm": 163, "boot_space_litres": 265},
            "engine_details": {"capacity_cc": 1197, "max_power_bhp": 82, "max_torque_nm": 112, "cylinders": 3, "transmission_type": "5MT"},
            "adas_features": [],
            "comfort_features": {"sunroof_type": "None", "ventilated_seats": False, "drive_modes": ["Normal"], "touchscreen_size_inches": 7.0, "digital_cluster": False}
        },
        {
            "brand": "Maruti Suzuki", "model": "Dzire", "variant": "ZXi Plus", "price": 850000.0, "mileage": 22.41,
            "fuel_type": "Petrol", "transmission": "Manual", "engine_specs": "1.2L DualJet Petrol",
            "safety_features": ["2 Airbags", "ABS with EBD", "Reverse Parking Sensors", "ESP"],
            "tech_features": ["7-inch SmartPlay Studio", "Automatic Climate Control", "Steering Controls"],
            "images": ["https://imgd.aeplcdn.com/664x374/n/cw/ec/170173/dzire-exterior-right-front-three-quarter.jpeg"], "body_type": "Sedan", "seating_capacity": 5, "ncap_rating": 2.0,
            "dimensions": {"length_mm": 3995, "width_mm": 1735, "height_mm": 1515, "wheelbase_mm": 2450, "ground_clearance_mm": 163, "boot_space_litres": 378},
            "engine_details": {"capacity_cc": 1197, "max_power_bhp": 89, "max_torque_nm": 113, "cylinders": 4, "transmission_type": "5MT"},
            "adas_features": [],
            "comfort_features": {"sunroof_type": "None", "ventilated_seats": False, "drive_modes": ["Normal"], "touchscreen_size_inches": 7.0, "digital_cluster": False}
        },
        {
            "brand": "Maruti Suzuki", "model": "Baleno", "variant": "Zeta", "price": 880000.0, "mileage": 22.35,
            "fuel_type": "Petrol", "transmission": "Manual", "engine_specs": "1.2L DualJet Petrol",
            "safety_features": ["6 Airbags", "Rear Camera", "ABS with EBD", "ESP"],
            "tech_features": ["9-inch Touchscreen", "OTA Updates", "SmartPlay Pro+"],
            "images": ["/cars/maruti_suzuki_baleno.png"], "body_type": "Hatchback", "seating_capacity": 5, "ncap_rating": 3.0,
            "dimensions": {"length_mm": 3990, "width_mm": 1745, "height_mm": 1500, "wheelbase_mm": 2520, "ground_clearance_mm": 170, "boot_space_litres": 318},
            "engine_details": {"capacity_cc": 1197, "max_power_bhp": 89, "max_torque_nm": 113, "cylinders": 4, "transmission_type": "5MT"},
            "adas_features": [],
            "comfort_features": {"sunroof_type": "None", "ventilated_seats": False, "drive_modes": ["Normal"], "touchscreen_size_inches": 9.0, "digital_cluster": False}
        },
        {
            "brand": "Maruti Suzuki", "model": "Brezza", "variant": "ZXi", "price": 1100000.0, "mileage": 19.8,
            "fuel_type": "Petrol", "transmission": "Manual", "engine_specs": "1.5L Smart Hybrid Petrol",
            "safety_features": ["6 Airbags", "360 Camera", "ESP", "Hill Hold Assist"],
            "tech_features": ["Wireless Apple CarPlay", "SmartPlay Pro+", "Arkamys Sound"],
            "images": ["/cars/maruti_suzuki_brezza.png"], "body_type": "SUV", "seating_capacity": 5, "ncap_rating": 4.0,
            "dimensions": {"length_mm": 3995, "width_mm": 1790, "height_mm": 1685, "wheelbase_mm": 2500, "ground_clearance_mm": 200, "boot_space_litres": 328},
            "engine_details": {"capacity_cc": 1462, "max_power_bhp": 102, "max_torque_nm": 136.8, "cylinders": 4, "transmission_type": "5MT"},
            "adas_features": [],
            "comfort_features": {"sunroof_type": "Single", "ventilated_seats": False, "drive_modes": ["Eco", "Normal"], "touchscreen_size_inches": 9.0, "digital_cluster": False}
        },
        {
            "brand": "Maruti Suzuki", "model": "Grand Vitara", "variant": "Zeta", "price": 1450000.0, "mileage": 21.11,
            "fuel_type": "Petrol", "transmission": "Manual", "engine_specs": "1.5L K15C Petrol Mild-Hybrid",
            "safety_features": ["6 Airbags", "ABS with EBD", "ESP", "Hill Descent Control"],
            "tech_features": ["9-inch Infotainment", "Connected Car Tech", "Ambient Lighting"],
            "images": ["/cars/maruti_suzuki_grand_vitara.png"], "body_type": "SUV", "seating_capacity": 5, "ncap_rating": 4.0,
            "dimensions": {"length_mm": 4345, "width_mm": 1795, "height_mm": 1645, "wheelbase_mm": 2600, "ground_clearance_mm": 210, "boot_space_litres": 373},
            "engine_details": {"capacity_cc": 1462, "max_power_bhp": 102, "max_torque_nm": 136.8, "cylinders": 4, "transmission_type": "5MT"},
            "adas_features": [],
            "comfort_features": {"sunroof_type": "Panoramic", "ventilated_seats": False, "drive_modes": ["Eco", "Normal", "Sport"], "touchscreen_size_inches": 9.0, "digital_cluster": True}
        },

        # --- Hyundai ---
        {
            "brand": "Hyundai", "model": "i20", "variant": "Asta Opt", "price": 980000.0, "mileage": 19.65,
            "fuel_type": "Petrol", "transmission": "Manual", "engine_specs": "1.2L Kappa Petrol",
            "safety_features": ["6 Airbags", "ESC", "HAC", "TPMS", "ABS with EBD"],
            "tech_features": ["10.25-inch Touchscreen", "Bose Audio", "BlueLink Connected"],
            "images": ["/cars/hyundai_i20.png"], "body_type": "Hatchback", "seating_capacity": 5, "ncap_rating": 3.0,
            "dimensions": {"length_mm": 3995, "width_mm": 1775, "height_mm": 1505, "wheelbase_mm": 2580, "ground_clearance_mm": 170, "boot_space_litres": 311},
            "engine_details": {"capacity_cc": 1197, "max_power_bhp": 82, "max_torque_nm": 114.7, "cylinders": 4, "transmission_type": "5MT"},
            "adas_features": [],
            "comfort_features": {"sunroof_type": "Single", "ventilated_seats": False, "drive_modes": ["Normal"], "touchscreen_size_inches": 10.25, "digital_cluster": True}
        },
        {
            "brand": "Hyundai", "model": "Creta", "variant": "SX (O)", "price": 1680000.0, "mileage": 16.8,
            "fuel_type": "Petrol", "transmission": "Automatic", "engine_specs": "1.5L MPi Petrol",
            "safety_features": ["6 Airbags", "ADAS Level 2", "Electronic Stability Control", "All 4 Disc Brakes", "TPMS"],
            "tech_features": ["Panoramic Sunroof", "Ventilated Seats", "Bose Sound System", "BlueLink Connected Car"],
            "images": ["https://imgd.aeplcdn.com/664x374/n/cw/ec/141115/creta-exterior-right-front-three-quarter.jpeg"], "body_type": "SUV", "seating_capacity": 5, "ncap_rating": 5.0,
            "dimensions": {"length_mm": 4330, "width_mm": 1790, "height_mm": 1635, "wheelbase_mm": 2610, "ground_clearance_mm": 190, "boot_space_litres": 433},
            "engine_details": {"capacity_cc": 1497, "max_power_bhp": 115, "max_torque_nm": 144, "cylinders": 4, "transmission_type": "IVT"},
            "adas_features": ["Lane Keep Assist", "Adaptive Cruise Control", "Forward Collision Avoidance Assist"],
            "comfort_features": {"sunroof_type": "Panoramic", "ventilated_seats": True, "drive_modes": ["Eco", "Normal", "Sport"], "touchscreen_size_inches": 10.25, "digital_cluster": True}
        },
        {
            "brand": "Hyundai", "model": "Venue", "variant": "SX", "price": 1200000.0, "mileage": 17.5,
            "fuel_type": "Petrol", "transmission": "Manual", "engine_specs": "1.2L Kappa Petrol",
            "safety_features": ["6 Airbags", "Rear Sensors", "ABS with EBD", "ESC"],
            "tech_features": ["8-inch Infotainment", "Ambient Lighting", "Wireless Charger"],
            "images": ["/cars/hyundai_venue.png"], "body_type": "SUV", "seating_capacity": 5, "ncap_rating": 4.0,
            "dimensions": {"length_mm": 3995, "width_mm": 1770, "height_mm": 1617, "wheelbase_mm": 2500, "ground_clearance_mm": 195, "boot_space_litres": 350},
            "engine_details": {"capacity_cc": 1197, "max_power_bhp": 82, "max_torque_nm": 114, "cylinders": 4, "transmission_type": "5MT"},
            "adas_features": [],
            "comfort_features": {"sunroof_type": "Single", "ventilated_seats": False, "drive_modes": ["Eco", "Normal"], "touchscreen_size_inches": 8.0, "digital_cluster": True}
        },
        {
            "brand": "Hyundai", "model": "Verna", "variant": "SX Opt", "price": 1750000.0, "mileage": 18.6,
            "fuel_type": "Petrol", "transmission": "Automatic", "engine_specs": "1.5L Turbo GDi",
            "safety_features": ["6 Airbags", "ADAS Level 2", "ESC", "All 4 Disc Brakes"],
            "tech_features": ["10.25-inch Dual Screen", "Bose Speakers", "Heated Seats"],
            "images": ["/cars/hyundai_verna.png"], "body_type": "Sedan", "seating_capacity": 5, "ncap_rating": 5.0,
            "dimensions": {"length_mm": 4535, "width_mm": 1765, "height_mm": 1475, "wheelbase_mm": 2670, "ground_clearance_mm": 165, "boot_space_litres": 528},
            "engine_details": {"capacity_cc": 1482, "max_power_bhp": 158, "max_torque_nm": 253, "cylinders": 4, "transmission_type": "7DCT"},
            "adas_features": ["Lane Departure Warning", "Adaptive Cruise", "Blind Spot Assist"],
            "comfort_features": {"sunroof_type": "Single", "ventilated_seats": True, "drive_modes": ["Eco", "Normal", "Sport"], "touchscreen_size_inches": 10.25, "digital_cluster": True}
        },

        # --- Tata ---
        {
            "brand": "Tata", "model": "Nexon", "variant": "Fearless Plus", "price": 1450000.0, "mileage": 17.0,
            "fuel_type": "Petrol", "transmission": "Automatic", "engine_specs": "1.2L Turbocharged Revotron",
            "safety_features": ["6 Airbags", "360 Degree Camera", "ESP", "5-Star GNCAP Rating"],
            "tech_features": ["10.25-inch Touchscreen", "Wireless Apple CarPlay", "JBL Sound System"],
            "images": ["https://imgd.aeplcdn.com/664x374/n/cw/ec/141867/nexon-exterior-right-front-three-quarter-3.jpeg"], "body_type": "SUV", "seating_capacity": 5, "ncap_rating": 5.0,
            "dimensions": {"length_mm": 3995, "width_mm": 1804, "height_mm": 1620, "wheelbase_mm": 2498, "ground_clearance_mm": 208, "boot_space_litres": 382},
            "engine_details": {"capacity_cc": 1199, "max_power_bhp": 118, "max_torque_nm": 170, "cylinders": 3, "transmission_type": "7DCA"},
            "adas_features": [],
            "comfort_features": {"sunroof_type": "Single", "ventilated_seats": True, "drive_modes": ["Eco", "City", "Sport"], "touchscreen_size_inches": 10.25, "digital_cluster": True}
        },
        {
            "brand": "Tata", "model": "Punch", "variant": "Creative", "price": 850000.0, "mileage": 20.09,
            "fuel_type": "Petrol", "transmission": "Manual", "engine_specs": "1.2L Revotron Engine",
            "safety_features": ["2 Airbags", "5-Star GNCAP Rating", "ABS with EBD", "Rear Camera"],
            "tech_features": ["7-inch Touchscreen", "Harman Sound System", "Connected Tech"],
            "images": ["/cars/tata_punch.png"], "body_type": "SUV", "seating_capacity": 5, "ncap_rating": 5.0,
            "dimensions": {"length_mm": 3827, "width_mm": 1742, "height_mm": 1615, "wheelbase_mm": 2445, "ground_clearance_mm": 187, "boot_space_litres": 366},
            "engine_details": {"capacity_cc": 1199, "max_power_bhp": 87, "max_torque_nm": 115, "cylinders": 3, "transmission_type": "5MT"},
            "adas_features": [],
            "comfort_features": {"sunroof_type": "None", "ventilated_seats": False, "drive_modes": ["Eco", "City"], "touchscreen_size_inches": 7.0, "digital_cluster": False}
        },
        {
            "brand": "Tata", "model": "Harrier", "variant": "Fearless Plus", "price": 2200000.0, "mileage": 16.8,
            "fuel_type": "Diesel", "transmission": "Automatic", "engine_specs": "2.0L Kryotec Diesel",
            "safety_features": ["7 Airbags", "ADAS Level 2", "ESP", "Traction Control"],
            "tech_features": ["12.3-inch Touchscreen", "10-Speaker JBL System", "Voice Assisted Sunroof"],
            "images": ["/cars/tata_harrier.png"], "body_type": "SUV", "seating_capacity": 5, "ncap_rating": 5.0,
            "dimensions": {"length_mm": 4605, "width_mm": 1922, "height_mm": 1718, "wheelbase_mm": 2741, "ground_clearance_mm": 205, "boot_space_litres": 445},
            "engine_details": {"capacity_cc": 1956, "max_power_bhp": 168, "max_torque_nm": 350, "cylinders": 4, "transmission_type": "6AT"},
            "adas_features": ["Autonomous Emergency Braking", "Lane Keep Assist", "Traffic Sign Recognition"],
            "comfort_features": {"sunroof_type": "Panoramic", "ventilated_seats": True, "drive_modes": ["Eco", "City", "Sport"], "touchscreen_size_inches": 12.3, "digital_cluster": True}
        },
        {
            "brand": "Tata", "model": "Safari", "variant": "Accomplished+", "price": 2500000.0, "mileage": 16.14,
            "fuel_type": "Diesel", "transmission": "Automatic", "engine_specs": "2.0L Kryotec Diesel",
            "safety_features": ["7 Airbags", "360 3D Camera", "ADAS Level 2", "ESC"],
            "tech_features": ["12.3-inch Infotainment", "Dual Zone Climate Control", "Gesture Tailgate"],
            "images": ["/cars/tata_safari.png"], "body_type": "SUV", "seating_capacity": 7, "ncap_rating": 5.0,
            "dimensions": {"length_mm": 4668, "width_mm": 1922, "height_mm": 1795, "wheelbase_mm": 2741, "ground_clearance_mm": 205, "boot_space_litres": 420},
            "engine_details": {"capacity_cc": 1956, "max_power_bhp": 168, "max_torque_nm": 350, "cylinders": 4, "transmission_type": "6AT"},
            "adas_features": ["Adaptive Cruise Control", "Lane Keep Assist", "Rear Cross Traffic Alert"],
            "comfort_features": {"sunroof_type": "Panoramic", "ventilated_seats": True, "drive_modes": ["Eco", "City", "Sport"], "touchscreen_size_inches": 12.3, "digital_cluster": True}
        },

        # --- Kia ---
        {
            "brand": "Kia", "model": "Seltos", "variant": "HTX Petrol", "price": 1650000.0, "mileage": 17.7,
            "fuel_type": "Petrol", "transmission": "Automatic", "engine_specs": "1.5L Turbo GDi Petrol",
            "safety_features": ["6 Airbags", "ESC", "HAC", "All Disc Brakes", "TPMS"],
            "tech_features": ["10.25-inch Touchscreen", "Bose Premium 8 Speakers", "Connected Car"],
            "images": ["https://imgd.aeplcdn.com/664x374/n/cw/ec/144159/seltos-exterior-right-front-three-quarter.jpeg"], "body_type": "SUV", "seating_capacity": 5, "ncap_rating": 3.0,
            "dimensions": {"length_mm": 4365, "width_mm": 1800, "height_mm": 1645, "wheelbase_mm": 2610, "ground_clearance_mm": 190, "boot_space_litres": 433},
            "engine_details": {"capacity_cc": 1497, "max_power_bhp": 158, "max_torque_nm": 253, "cylinders": 4, "transmission_type": "7DCT"},
            "adas_features": ["Forward Collision Assist", "Lane Follow Assist"],
            "comfort_features": {"sunroof_type": "Panoramic", "ventilated_seats": True, "drive_modes": ["Eco", "Normal", "Sport"], "touchscreen_size_inches": 10.25, "digital_cluster": True}
        },
        {
            "brand": "Kia", "model": "Sonet", "variant": "HTX", "price": 1250000.0, "mileage": 18.2,
            "fuel_type": "Petrol", "transmission": "Automatic", "engine_specs": "1.0L Turbo GDi",
            "safety_features": ["6 Airbags", "Rear Sensors", "ABS with EBD", "ESC"],
            "tech_features": ["10.25-inch Infotainment", "Wireless Charging", "LED Mood Lamps"],
            "images": ["/cars/kia_sonet.png"], "body_type": "SUV", "seating_capacity": 5, "ncap_rating": 3.0,
            "dimensions": {"length_mm": 3995, "width_mm": 1790, "height_mm": 1642, "wheelbase_mm": 2500, "ground_clearance_mm": 205, "boot_space_litres": 385},
            "engine_details": {"capacity_cc": 998, "max_power_bhp": 118, "max_torque_nm": 172, "cylinders": 3, "transmission_type": "7DCT"},
            "adas_features": [],
            "comfort_features": {"sunroof_type": "Single", "ventilated_seats": True, "drive_modes": ["Eco", "Normal", "Sport"], "touchscreen_size_inches": 10.25, "digital_cluster": True}
        },
        {
            "brand": "Kia", "model": "Carens", "variant": "Luxury Plus", "price": 1800000.0, "mileage": 16.5,
            "fuel_type": "Diesel", "transmission": "Automatic", "engine_specs": "1.5L CRDi VGT",
            "safety_features": ["6 Airbags", "ESC", "All Wheel Disc Brakes", "TPMS"],
            "tech_features": ["10.25-inch Audio", "Cabin Air Purifier", "One Touch Tumble Seats"],
            "images": ["/cars/kia_carens.png"], "body_type": "MPV", "seating_capacity": 7, "ncap_rating": 3.0,
            "dimensions": {"length_mm": 4540, "width_mm": 1800, "height_mm": 1708, "wheelbase_mm": 2780, "ground_clearance_mm": 195, "boot_space_litres": 216},
            "engine_details": {"capacity_cc": 1493, "max_power_bhp": 113, "max_torque_nm": 250, "cylinders": 4, "transmission_type": "6AT"},
            "adas_features": [],
            "comfort_features": {"sunroof_type": "Single", "ventilated_seats": True, "drive_modes": ["Eco", "Normal", "Sport"], "touchscreen_size_inches": 10.25, "digital_cluster": True}
        },

        # --- Mahindra ---
        {
            "brand": "Mahindra", "model": "XUV700", "variant": "AX7 L", "price": 2350000.0, "mileage": 15.0,
            "fuel_type": "Petrol", "transmission": "Automatic", "engine_specs": "2.0L mStallion Turbo Petrol",
            "safety_features": ["7 Airbags", "ADAS Level 2", "ESP", "5-Star GNCAP Rating"],
            "tech_features": ["Dual 10.25-inch Screens", "Sony 3D Sound System", "Smart Door Handles"],
            "images": ["/cars/mahindra_xuv700.png"], "body_type": "SUV", "seating_capacity": 7, "ncap_rating": 5.0,
            "dimensions": {"length_mm": 4695, "width_mm": 1890, "height_mm": 1755, "wheelbase_mm": 2750, "ground_clearance_mm": 200, "boot_space_litres": 240},
            "engine_details": {"capacity_cc": 1997, "max_power_bhp": 197, "max_torque_nm": 380, "cylinders": 4, "transmission_type": "6AT"},
            "adas_features": ["Adaptive Cruise Control", "Smart Pilot Assist", "High Beam Assist"],
            "comfort_features": {"sunroof_type": "Panoramic", "ventilated_seats": True, "drive_modes": ["Zip", "Zap", "Zoom"], "touchscreen_size_inches": 10.25, "digital_cluster": True}
        },
        {
            "brand": "Mahindra", "model": "Thar", "variant": "LX 4WD", "price": 1600000.0, "mileage": 15.2,
            "fuel_type": "Diesel", "transmission": "Manual", "engine_specs": "2.2L mHawk Diesel",
            "safety_features": ["2 Airbags", "Roll Cage", "ESP", "Hill Hold Control", "4-Star NCAP"],
            "tech_features": ["7-inch Touchscreen", "Roof Mounted Speakers", "Adventure Connect Tech"],
            "images": ["/cars/mahindra_thar.png"], "body_type": "SUV", "seating_capacity": 4, "ncap_rating": 4.0,
            "dimensions": {"length_mm": 3985, "width_mm": 1820, "height_mm": 1844, "wheelbase_mm": 2450, "ground_clearance_mm": 226, "boot_space_litres": 150},
            "engine_details": {"capacity_cc": 2184, "max_power_bhp": 130, "max_torque_nm": 300, "cylinders": 4, "transmission_type": "6MT"},
            "adas_features": [],
            "comfort_features": {"sunroof_type": "None", "ventilated_seats": False, "drive_modes": ["Off-Road"], "touchscreen_size_inches": 7.0, "digital_cluster": False}
        },
        {
            "brand": "Mahindra", "model": "Scorpio-N", "variant": "Z8 L", "price": 2100000.0, "mileage": 14.0,
            "fuel_type": "Diesel", "transmission": "Automatic", "engine_specs": "2.2L mHawk Diesel",
            "safety_features": ["6 Airbags", "5-Star GNCAP", "ESP", "ISOFIX Mounts"],
            "tech_features": ["8-inch Infotainment", "What3Words Tech", "Sony Audio System"],
            "images": ["/cars/mahindra_scorpio_n.png"], "body_type": "SUV", "seating_capacity": 7, "ncap_rating": 5.0,
            "dimensions": {"length_mm": 4662, "width_mm": 1917, "height_mm": 1857, "wheelbase_mm": 2750, "ground_clearance_mm": 187, "boot_space_litres": 460},
            "engine_details": {"capacity_cc": 2198, "max_power_bhp": 172, "max_torque_nm": 400, "cylinders": 4, "transmission_type": "6AT"},
            "adas_features": [],
            "comfort_features": {"sunroof_type": "Single", "ventilated_seats": False, "drive_modes": ["Zip", "Zap", "Zoom"], "touchscreen_size_inches": 8.0, "digital_cluster": True}
        },

        # --- Toyota ---
        {
            "brand": "Toyota", "model": "Innova Hycross", "variant": "VX Hybrid", "price": 2600000.0, "mileage": 23.24,
            "fuel_type": "Hybrid", "transmission": "Automatic", "engine_specs": "2.0L Hybrid Engine",
            "safety_features": ["6 Airbags", "Vehicle Stability Control", "Hill Start Assist"],
            "tech_features": ["10-inch Display", "Dual Zone Auto AC", "Powered Ottoman Seats"],
            "images": ["/cars/toyota_innova.png"], "body_type": "MPV", "seating_capacity": 7, "ncap_rating": 5.0,
            "dimensions": {"length_mm": 4755, "width_mm": 1850, "height_mm": 1795, "wheelbase_mm": 2850, "ground_clearance_mm": 185, "boot_space_litres": 300},
            "engine_details": {"capacity_cc": 1987, "max_power_bhp": 184, "max_torque_nm": 206, "cylinders": 4, "transmission_type": "e-CVT"},
            "adas_features": [],
            "comfort_features": {"sunroof_type": "Panoramic", "ventilated_seats": True, "drive_modes": ["Eco", "Normal", "Power"], "touchscreen_size_inches": 10.1, "digital_cluster": True}
        },
        {
            "brand": "Toyota", "model": "Urban Cruiser Hyryder", "variant": "G Hybrid", "price": 1850000.0, "mileage": 27.97,
            "fuel_type": "Hybrid", "transmission": "Automatic", "engine_specs": "1.5L Self-Charging Hybrid",
            "safety_features": ["6 Airbags", "TPMS", "VSC", "Hill Hold Control"],
            "tech_features": ["9-inch Touchscreen", "Head-up Display", "Wireless Charging"],
            "images": ["/cars/toyota_hyryder.png"], "body_type": "SUV", "seating_capacity": 5, "ncap_rating": 4.0,
            "dimensions": {"length_mm": 4365, "width_mm": 1795, "height_mm": 1645, "wheelbase_mm": 2600, "ground_clearance_mm": 210, "boot_space_litres": 373},
            "engine_details": {"capacity_cc": 1490, "max_power_bhp": 114, "max_torque_nm": 141, "cylinders": 3, "transmission_type": "e-CVT"},
            "adas_features": [],
            "comfort_features": {"sunroof_type": "Panoramic", "ventilated_seats": True, "drive_modes": ["Eco", "Power", "EV"], "touchscreen_size_inches": 9.0, "digital_cluster": True}
        },

        # --- Volkswagen ---
        {
            "brand": "Volkswagen", "model": "Virtus", "variant": "Topline 1.0 TSI", "price": 1900000.0, "mileage": 18.2,
            "fuel_type": "Petrol", "transmission": "Automatic", "engine_specs": "1.5L TSI EVO Petrol",
            "safety_features": ["6 Airbags", "5-Star GNCAP Rating", "Electronic Stability Control", "Multi-Collision Brakes"],
            "tech_features": ["10-inch Infotainment Screen", "Digital Cockpit Console", "Wireless Charging", "Sunroof"],
            "images": ["https://imgd.aeplcdn.com/664x374/n/cw/ec/144681/virtus-exterior-right-front-three-quarter-7.jpeg"], "body_type": "Sedan", "seating_capacity": 5, "ncap_rating": 5.0,
            "dimensions": {"length_mm": 4561, "width_mm": 1752, "height_mm": 1507, "wheelbase_mm": 2651, "ground_clearance_mm": 179, "boot_space_litres": 521},
            "engine_details": {"capacity_cc": 1498, "max_power_bhp": 148, "max_torque_nm": 250, "cylinders": 4, "transmission_type": "7DSG"},
            "adas_features": [],
            "comfort_features": {"sunroof_type": "Single", "ventilated_seats": True, "drive_modes": ["Eco", "Normal", "Sport"], "touchscreen_size_inches": 10.1, "digital_cluster": True}
        },
        {
            "brand": "Volkswagen", "model": "Taigun", "variant": "GT Plus", "price": 1780000.0, "mileage": 18.0,
            "fuel_type": "Petrol", "transmission": "Automatic", "engine_specs": "1.5L TSI EVO Engine",
            "safety_features": ["6 Airbags", "5-Star GNCAP", "ESC", "Rear Camera"],
            "tech_features": ["10-inch Infotainment", "MyVW Connect", "Wireless Android Auto"],
            "images": ["/cars/volkswagen_taigun.png"], "body_type": "SUV", "seating_capacity": 5, "ncap_rating": 5.0,
            "dimensions": {"length_mm": 4221, "width_mm": 1760, "height_mm": 1612, "wheelbase_mm": 2651, "ground_clearance_mm": 188, "boot_space_litres": 385},
            "engine_details": {"capacity_cc": 1498, "max_power_bhp": 148, "max_torque_nm": 250, "cylinders": 4, "transmission_type": "7DSG"},
            "adas_features": [],
            "comfort_features": {"sunroof_type": "Single", "ventilated_seats": True, "drive_modes": ["Eco", "Sport"], "touchscreen_size_inches": 10.0, "digital_cluster": True}
        },

        # --- Honda ---
        {
            "brand": "Honda", "model": "City", "variant": "ZX", "price": 1580000.0, "mileage": 17.8,
            "fuel_type": "Petrol", "transmission": "Automatic", "engine_specs": "1.5L i-VTEC Petrol",
            "safety_features": ["6 Airbags", "Honda Sensing ADAS Level 1", "ESC", "LaneWatch Camera"],
            "tech_features": ["8-inch Infotainment", "Honda Connect Tech", "Wireless CarPlay"],
            "images": ["/cars/honda_city.png"], "body_type": "Sedan", "seating_capacity": 5, "ncap_rating": 5.0,
            "dimensions": {"length_mm": 4574, "width_mm": 1748, "height_mm": 1489, "wheelbase_mm": 2600, "ground_clearance_mm": 165, "boot_space_litres": 506},
            "engine_details": {"capacity_cc": 1498, "max_power_bhp": 119, "max_torque_nm": 145, "cylinders": 4, "transmission_type": "CVT"},
            "adas_features": ["Collision Mitigation Braking", "Lane Keeping Assist System", "Road Departure Mitigation"],
            "comfort_features": {"sunroof_type": "Single", "ventilated_seats": False, "drive_modes": ["Eco", "Normal"], "touchscreen_size_inches": 8.0, "digital_cluster": True}
        },
        {
            "brand": "Honda", "model": "Elevate", "variant": "ZX", "price": 1620000.0, "mileage": 16.92,
            "fuel_type": "Petrol", "transmission": "Automatic", "engine_specs": "1.5L i-VTEC Petrol",
            "safety_features": ["6 Airbags", "Honda Sensing ADAS", "VSA", "Hill Start Assist"],
            "tech_features": ["10.25-inch Touchscreen", "Wireless Charging", "8-speaker Premium Sound"],
            "images": ["/cars/honda_elevate.png"], "body_type": "SUV", "seating_capacity": 5, "ncap_rating": 5.0,
            "dimensions": {"length_mm": 4312, "width_mm": 1790, "height_mm": 1650, "wheelbase_mm": 2650, "ground_clearance_mm": 220, "boot_space_litres": 458},
            "engine_details": {"capacity_cc": 1498, "max_power_bhp": 119, "max_torque_nm": 145, "cylinders": 4, "transmission_type": "CVT"},
            "adas_features": ["Adaptive Cruise Control", "Lane Keeping Assist"],
            "comfort_features": {"sunroof_type": "Single", "ventilated_seats": False, "drive_modes": ["Normal"], "touchscreen_size_inches": 10.25, "digital_cluster": True}
        },

        # --- Skoda ---
        {
            "brand": "Skoda", "model": "Slavia", "variant": "Style", "price": 1600000.0, "mileage": 19.47,
            "fuel_type": "Petrol", "transmission": "Manual", "engine_specs": "1.0L TSI Petrol",
            "safety_features": ["6 Airbags", "5-Star GNCAP Rating", "ESC", "TPMS", "ABS"],
            "tech_features": ["10-inch Infotainment", "MySkoda Connect", "8 Speakers with Subwoofer"],
            "images": ["/cars/skoda_slavia.png"], "body_type": "Sedan", "seating_capacity": 5, "ncap_rating": 5.0,
            "dimensions": {"length_mm": 4541, "width_mm": 1752, "height_mm": 1507, "wheelbase_mm": 2651, "ground_clearance_mm": 179, "boot_space_litres": 521},
            "engine_details": {"capacity_cc": 999, "max_power_bhp": 114, "max_torque_nm": 178, "cylinders": 3, "transmission_type": "6MT"},
            "adas_features": [],
            "comfort_features": {"sunroof_type": "Single", "ventilated_seats": True, "drive_modes": ["Normal"], "touchscreen_size_inches": 10.0, "digital_cluster": True}
        },
        {
            "brand": "Skoda", "model": "Kushaq", "variant": "Style", "price": 1650000.0, "mileage": 18.09,
            "fuel_type": "Petrol", "transmission": "Manual", "engine_specs": "1.0L TSI Engine",
            "safety_features": ["6 Airbags", "5-Star GNCAP", "ESC", "Multi-Collision Braking"],
            "tech_features": ["10-inch Touchscreen", "Wireless charging", "Valet mode"],
            "images": ["/cars/skoda_kushaq.png"], "body_type": "SUV", "seating_capacity": 5, "ncap_rating": 5.0,
            "dimensions": {"length_mm": 4225, "width_mm": 1760, "height_mm": 1612, "wheelbase_mm": 2651, "ground_clearance_mm": 188, "boot_space_litres": 385},
            "engine_details": {"capacity_cc": 999, "max_power_bhp": 114, "max_torque_nm": 178, "cylinders": 3, "transmission_type": "6MT"},
            "adas_features": [],
            "comfort_features": {"sunroof_type": "Single", "ventilated_seats": True, "drive_modes": ["Normal"], "touchscreen_size_inches": 10.0, "digital_cluster": True}
        },

        # --- MG ---
        {
            "brand": "MG", "model": "Hector", "variant": "Sharp Pro", "price": 2000000.0, "mileage": 13.79,
            "fuel_type": "Petrol", "transmission": "Automatic", "engine_specs": "1.5L Turbo Petrol",
            "safety_features": ["6 Airbags", "360 Around View Camera", "ESP", "Cornering Lights"],
            "tech_features": ["14-inch HD Touchscreen", "Dual Pane Panoramic Sunroof", "Next Gen i-Smart Tech"],
            "images": ["/cars/mg_hector.png"], "body_type": "SUV", "seating_capacity": 5, "ncap_rating": 4.0,
            "dimensions": {"length_mm": 4699, "width_mm": 1835, "height_mm": 1760, "wheelbase_mm": 2750, "ground_clearance_mm": 192, "boot_space_litres": 587},
            "engine_details": {"capacity_cc": 1451, "max_power_bhp": 141, "max_torque_nm": 250, "cylinders": 4, "transmission_type": "CVT"},
            "adas_features": ["Traffic Jam Assist", "Lane Departure Warning"],
            "comfort_features": {"sunroof_type": "Panoramic", "ventilated_seats": True, "drive_modes": ["Eco", "Normal", "Sport"], "touchscreen_size_inches": 14.0, "digital_cluster": True}
        },

        # --- Renault ---
        {
            "brand": "Renault", "model": "Kiger", "variant": "RXZ Turbo", "price": 950000.0, "mileage": 20.5,
            "fuel_type": "Petrol", "transmission": "Automatic", "engine_specs": "1.0L Turbocharged Petrol",
            "safety_features": ["4 Airbags", "Rear Camera", "ABS with EBD", "Hill Start Assist"],
            "tech_features": ["8-inch Infotainment", "3D Sound by Arkamys", "Wireless Smart Link"],
            "images": ["/cars/renault_kiger.png"], "body_type": "SUV", "seating_capacity": 5, "ncap_rating": 4.0,
            "dimensions": {"length_mm": 3991, "width_mm": 1750, "height_mm": 1605, "wheelbase_mm": 2500, "ground_clearance_mm": 205, "boot_space_litres": 405},
            "engine_details": {"capacity_cc": 999, "max_power_bhp": 99, "max_torque_nm": 160, "cylinders": 3, "transmission_type": "CVT"},
            "adas_features": [],
            "comfort_features": {"sunroof_type": "None", "ventilated_seats": False, "drive_modes": ["Eco", "Normal", "Sport"], "touchscreen_size_inches": 8.0, "digital_cluster": True}
        },

        # --- Nissan ---
        {
            "brand": "Nissan", "model": "Magnite", "variant": "XV Premium", "price": 980000.0, "mileage": 20.0,
            "fuel_type": "Petrol", "transmission": "Automatic", "engine_specs": "1.0L HRA0 Turbo Petrol",
            "safety_features": ["2 Airbags", "Around View Monitor 360", "Vehicle Dynamic Control", "4-Star NCAP"],
            "tech_features": ["8-inch Display", "Nissan Connect", "6 Speaker Audio"],
            "images": ["/cars/nissan_magnite.png"], "body_type": "SUV", "seating_capacity": 5, "ncap_rating": 4.0,
            "dimensions": {"length_mm": 3994, "width_mm": 1758, "height_mm": 1572, "wheelbase_mm": 2500, "ground_clearance_mm": 205, "boot_space_litres": 336},
            "engine_details": {"capacity_cc": 999, "max_power_bhp": 99, "max_torque_nm": 152, "cylinders": 3, "transmission_type": "CVT"},
            "adas_features": [],
            "comfort_features": {"sunroof_type": "None", "ventilated_seats": False, "drive_modes": ["Eco", "Sport"], "touchscreen_size_inches": 8.0, "digital_cluster": True}
        }
=======
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
>>>>>>> 839ba178d4aeef05cb4c560f62ca954700b89f58
    ]
    
    cars = [Car(**c) for c in cars_data]
    db.add_all(cars)
    db.commit()
    
    for car in cars:
        db.refresh(car)
        
    car_ids = [car.id for car in cars]
<<<<<<< HEAD
    print(f"[OK] {len(cars)} Cars seeded with expanded Indian spec sheets.")
    
    # Print verification table
    print("\n--- SEED VERIFICATION TABLE ---")
    print(f"{'ID':<4} {'Brand':<18} {'Model':<12} {'Body Type':<10} {'NCAP':<6} {'Price (Lakh)':<12} {'Image Path'}")
    print("-" * 90)
    for car in cars:
        img = car.images[0] if car.images else "MISSING"
        print(f"{car.id:<4} {car.brand:<18} {car.model:<12} {car.body_type:<10} {car.ncap_rating:<6} {car.price/100000.0:<12.2f} {img}")
    print("-" * 90 + "\n")
=======
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
>>>>>>> 839ba178d4aeef05cb4c560f62ca954700b89f58
    
    # 3. Seed Showrooms
    showrooms = [
        Showroom(
            name="Bangalore Indiranagar Showroom", address="100 Feet Rd, Indiranagar, Bengaluru, Karnataka 560038",
            latitude=12.97189, longitude=77.64115, contact_number="+918049999901", available_car_ids=car_ids
        ),
        Showroom(
            name="Bangalore Whitefield Showroom", address="ITPL Main Rd, Whitefield, Bengaluru, Karnataka 560066",
            latitude=12.9868, longitude=77.7500, contact_number="+918049999903", available_car_ids=car_ids
        ),
        Showroom(
            name="Mumbai Bandra Showroom", address="Linking Rd, Bandra West, Mumbai, Maharashtra 400050",
            latitude=19.0596, longitude=72.8295, contact_number="+912249999902", available_car_ids=car_ids
        ),
        Showroom(
            name="Delhi Connaught Place Showroom", address="Connaught Place, New Delhi, Delhi 110001",
            latitude=28.6139, longitude=77.2090, contact_number="+911149999901", available_car_ids=car_ids
        ),
    ]
    db.add_all(showrooms)
    db.commit()
    print(f"[OK] {len(showrooms)} Showrooms seeded.")
    
<<<<<<< HEAD
    # 4. Seed Youtube Review Metadata (with channel, channel_url, video_url)
    # We will seed 1 dedicated review metadata per car
    yt_reviews = []
    channels = [
        {"name": "MotorOctane", "url": "https://www.youtube.com/@MotorOctane"},
        {"name": "FasBeam", "url": "https://www.youtube.com/@FasBeam"},
        {"name": "Prasad Tech In Telugu", "url": "https://www.youtube.com/@PrasadTechInTelugu"},
        {"name": "Gagan Choudhary", "url": "https://www.youtube.com/@GaganChoudhary"},
        {"name": "Autocar India", "url": "https://www.youtube.com/@AutocarIndia1"}
=======
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
>>>>>>> 839ba178d4aeef05cb4c560f62ca954700b89f58
    ]
    
<<<<<<< HEAD
    for idx, car in enumerate(cars):
        # Rotate channels
        ch = channels[idx % len(channels)]
        video_id = f"video_review_{car.brand.lower().replace(' ', '_')}_{car.model.lower()}"
        yt_reviews.append(YoutubeReview(
            car_id=car.id,
            video_id=video_id,
            title=f"{car.brand} {car.model} Detailed In-Depth Review and Test Drive",
            thumbnail=f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg",
            view_count=250000 + (car.id * 15000),
            description=f"Detailed Hindi and English review of {car.brand} {car.model} {car.variant} variant. Check specifications, ride, mileage and safety ratings.",
            channel_name=ch["name"],
            channel_url=ch["url"],
            video_url=f"https://www.youtube.com/watch?v={video_id}"
        ))
    db.add_all(yt_reviews)
    db.commit()
    print("[OK] YouTube review redirection metadata seeded.")

    # 5. Seed Reviews, YouTube Summaries, Customer Sentiments
    reviews = []
    yt_summaries = []
    sentiments = []
    
    for car in cars:
        reviews.append(Review(
            car_id=car.id,
            user_name="Aman Verma",
            rating=4.5 if car.ncap_rating and car.ncap_rating >= 4.0 else 4.0,
            comment=f"Highly satisfied with the {car.model} {car.variant}. The tech specs and feature set are great for this budget.",
            sentiment="Positive"
        ))
        yt_summaries.append(YoutubeReviewSummary(
            car_id=car.id,
            video_url=f"https://www.youtube.com/watch?v=video_review_{car.brand.lower().replace(' ', '_')}_{car.model.lower()}",
            summary_text=f"The {car.brand} {car.model} review indicates robust build quality and easy drivability. Engine refinement is decent.",
            pros=["Comfortable suspension", "Smart dashboard layout", "Affordable price package"],
            cons=["Bumpy low speed ride" if car.body_type == "SUV" else "Low sheet metal quality"],
            mileage_observed=f"{car.mileage - 2:.1f} kmpl (City), {car.mileage + 1:.1f} kmpl (Highway)",
            ride_quality="Suspension feels tuned for Indian speed bumps.",
            common_complaints=["Rear seat legroom could be slightly better"]
        ))
        sentiments.append(CustomerSentiment(
            car_id=car.id,
            positive_percentage=82.0,
            negative_percentage=10.0,
            neutral_percentage=8.0,
            total_comments_analyzed=15,
            sentiment_summary=f"Positive customer feedback highlighting cabin comfort, tech dashboard, and mileage of {car.mileage} kmpl."
        ))
        
    db.add_all(reviews)
=======
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
>>>>>>> 839ba178d4aeef05cb4c560f62ca954700b89f58
    db.add_all(yt_summaries)
    db.add_all(sentiments)
    db.commit()
    print("[OK] Reviews, Summaries, and Sentiments seeded.")
    
    db.close()
    print("\n=== DATABASE SEEDED SUCCESSFULLY ===")
    return car_ids

def main():
    try:
        seed_postgres()
    except Exception as e:
<<<<<<< HEAD
        print(f"[ERROR] Seeding failed: {e}")
        import traceback
        traceback.print_exc()
=======
        print(f"Error seeding: {e}")
>>>>>>> f82fe05c622b74763ace4d5a0d3f5b82c5a95241
>>>>>>> 839ba178d4aeef05cb4c560f62ca954700b89f58

if __name__ == "__main__":
    main()
