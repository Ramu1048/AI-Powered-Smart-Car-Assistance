# AI-Powered Smart Car Assistance API - Contract Specification

All endpoints in this API follow a consistent JSON envelope structure:

### Successful Response Format
```json
{
  "success": true,
  "data": { ... },
  "message": "Optional message details"
}
```

### Error Response Format
```json
{
  "success": false,
  "data": null,
  "message": "Detailed error explanation"
}
```

---

## 1. Authentication Endpoints

### Register User
* **URL**: `/auth/register`
* **Method**: `POST`
* **Request Body**:
  ```json
  {
    "email": "user@example.com",
    "password": "securepassword123",
    "name": "John Doe",
    "phone": "+919876543210"
  }
  ```
* **Response Data**:
  ```json
  {
    "id": 1,
    "email": "user@example.com",
    "name": "John Doe",
    "phone": "+919876543210",
    "is_admin": false,
    "created_at": "2026-07-20T10:52:00Z"
  }
  ```

### Login User
* **URL**: `/auth/login`
* **Method**: `POST`
* **Request Body**:
  ```json
  {
    "email": "user@example.com",
    "password": "securepassword123"
  }
  ```
* **Response Data**:
  ```json
  {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer",
    "user": {
      "id": 1,
      "email": "user@example.com",
      "name": "John Doe",
      "phone": "+919876543210",
      "is_admin": false,
      "created_at": "2026-07-20T10:52:00Z"
    }
  }
  ```

---

## 2. Car Discovery & Search Endpoints

### List Cars
* **URL**: `/cars`
* **Method**: `GET`
* **Query Parameters**:
  * `brand` (string, optional)
  * `min_price` (float, optional)
  * `max_price` (float, optional)
  * `fuel_type` (string, optional)
  * `transmission` (string, optional)
  * `min_mileage` (float, optional)
  * `skip` (integer, default `0`)
  * `limit` (integer, default `10`)
* **Response Data**:
  ```json
  [
    {
      "id": 1,
      "brand": "Hyundai",
      "model": "Creta",
      "variant": "SX Tech",
      "price": 1680000.0,
      "mileage": 16.8,
      "fuel_type": "Petrol",
      "transmission": "Automatic",
      "engine_specs": "1.5L MPi Petrol",
      "safety_features": ["6 Airbags", "ADAS Level 2"],
      "tech_features": ["Panoramic Sunroof", "Ventilated Seats"],
      "images": ["https://images.unsplash.com/..."],
      "created_at": "2026-07-20T10:52:00Z"
    }
  ]
  ```

### Get Single Car Details
* **URL**: `/cars/{id}`
* **Method**: `GET`
* **Response Data**: Returns the matching single Car object.

### Fetch Similar Cars
* **URL**: `/cars/{id}/similar`
* **Method**: `GET`
* **Query Parameters**:
  * `limit` (integer, default `4`)
* **Response Data**: List of similar Car objects based on price range segment fallback.

---

## 3. Comparison Endpoints

### Compare Cars
* **URL**: `/compare`
* **Method**: `POST`
* **Request Body**:
  ```json
  {
    "car_ids": [1, 2]
  }
  ```
* **Response Data**: List of full spec objects for comparison in requested order.

---

## 4. Showroom & Booking Endpoints

### Find Nearby Showrooms
* **URL**: `/showrooms/nearby`
* **Method**: `GET`
* **Query Parameters**:
  * `latitude` (float, required)
  * `longitude` (float, required)
  * `radius_km` (float, default `50.0`)
* **Response Data**:
  ```json
  [
    {
      "id": 1,
      "name": "Bangalore Central Showroom",
      "address": "100 Feet Rd, Indiranagar, Indiranagar, Indiranagar",
      "latitude": 12.9716,
      "longitude": 77.5946,
      "contact_number": "+918049999999",
      "available_car_ids": [1, 2, 3],
      "distance_km": 1.2
    }
  ]
  ```

### Showroom Available Cars
* **URL**: `/showrooms/{id}/availability`
* **Method**: `GET`
* **Response Data**: List of Car objects currently available in this showroom.

### Book a Test Drive or Purchase
* **URL**: `/bookings`
* **Method**: `POST`
* **Headers**: `Authorization: Bearer <token>`
* **Request Body**:
  ```json
  {
    "car_id": 1,
    "showroom_id": 1,
    "booking_type": "test_drive",
    "scheduled_date": "2026-07-25T10:30:00Z"
  }
  ```
* **Response Data**: Returns created Booking object with nested `car` and `showroom` structures.

### View User Booking History
* **URL**: `/bookings/{user_id}`
* **Method**: `GET`
* **Headers**: `Authorization: Bearer <token>`
* **Response Data**: List of Bookings made by this user.

---

## 5. Review & Sentiment Endpoints (PostgreSQL backed)

### Get Car Reviews
* **URL**: `/cars/{id}/reviews`
* **Method**: `GET`
* **Response Data**:
  ```json
  [
    {
      "car_id": 1,
      "user_name": "Aarav Mehta",
      "rating": 4.5,
      "comment": "Build quality is top notch. Safety is 5-star.",
      "sentiment": "Positive",
      "created_at": "2026-07-20T10:52:00Z"
    }
  ]
  ```

### Submit Car Review
* **URL**: `/cars/{id}/reviews`
* **Method**: `POST`
* **Headers**: `Authorization: Bearer <token>`
* **Request Body**:
  ```json
  {
    "rating": 4.5,
    "comment": "Excellent vehicle, very spacious"
  }
  ```
* **Response Data**: Returns saved review object containing calculated `sentiment`.

### Fetch YouTube Review Summaries
* **URL**: `/cars/{id}/youtube-summary`
* **Method**: `GET`
* **Response Data**:
  ```json
  {
    "car_id": 1,
    "video_url": "https://www.youtube.com/watch?v=...",
    "summary_text": "Summarized from top expert automotive channels...",
    "pros": ["Safety Rating", "Comfort"],
    "cons": ["Sluggish gearbox"],
    "created_at": "2026-07-20T10:52:00Z"
  }
  ```

---

## 6. Wishlist Endpoints

### Save Car to Wishlist
* **URL**: `/wishlist`
* **Method**: `POST`
* **Headers**: `Authorization: Bearer <token>`
* **Request Body**:
  ```json
  {
    "car_id": 1
  }
  ```
* **Response Data**: Returns created wishlist item.

### View Saved Wishlist
* **URL**: `/wishlist/{user_id}`
* **Method**: `GET`
* **Headers**: `Authorization: Bearer <token>`
* **Response Data**: List of wishlisted items with detailed nested car data.

### Remove Car from Wishlist
* **URL**: `/wishlist/{id}`
* **Method**: `DELETE`
* **Headers**: `Authorization: Bearer <token>`
* **Response Data**: Null structure indicating removal success.

---

## 7. Admin Endpoints

All admin endpoints require an active Bearer Token of a user with `is_admin` set to `true`.

* `GET /admin/cars` - Fetch all cars in administrative detail.
* `POST /admin/cars` - Add a new car configuration.
* `PUT /admin/cars/{id}` - Modify existing car specification.
* `DELETE /admin/cars/{id}` - Purge a car listing.
* `GET /admin/bookings` - Retrieve all bookings made globally in the system.

---

## 8. AI & RAG Assistant Endpoints

### Conversational RAG Chat
* **URL**: `/api/ai/chat`
* **Method**: `POST`
* **Request Body**:
  ```json
  {
    "message": "Is the Tata Nexon a safe car?",
    "history": [
      { "role": "user", "content": "Hi" },
      { "role": "assistant", "content": "Hello! How can I assist you today?" }
    ]
  }
  ```
* **Response Data**:
  ```json
  {
    "response": "Yes, the Tata Nexon is highly regarded for safety. It holds a 5-star safety rating from Global NCAP...",
    "sources": [
      "Car details: Tata Nexon Creative Plus... Safety: 6 Airbags, ESP..."
    ]
  }
  ```

### Personalized Smart Recommendations
* **URL**: `/api/ai/recommend`
* **Method**: `POST`
* **Request Body**:
  ```json
  {
    "budget": 1500000.0,
    "family_size": 4,
    "commute_distance": 25.0,
    "fuel_preference": "Petrol",
    "priorities": ["Safety", "Mileage"]
  }
  ```
* **Response Data**:
  ```json
  [
    {
      "car_id": 1,
      "brand": "Tata",
      "model": "Nexon",
      "variant": "Creative Plus",
      "match_score": 95.0,
      "explanation": "The Tata Nexon is an excellent match...",
      "pros": ["5-star GNCAP safety rating", "208mm ground clearance"],
      "cons": ["Slow AMT shifts"]
    }
  ]
  ```

### Side-by-Side Car Specifications Comparison
* **URL**: `/api/ai/compare`
* **Method**: `POST`
* **Request Body**:
  ```json
  {
    "car_ids": [1, 2],
    "aspect": "safety"
  }
  ```
* **Response Data**:
  ```json
  {
    "comparison_summary": "Comparing Tata Nexon and Hyundai Creta safety configurations...",
    "specs_table": {
      "Tata Nexon": {
        "variant": "Creative Plus",
        "price": 1150000.0,
        "mileage": 17.5,
        "fuel_type": "Petrol",
        "transmission": "Manual",
        "engine": "1.2L Turbocharged Revotron",
        "safety": ["6 Airbags", "ESP", "ABS with EBD", "5-Star GNCAP Rating"],
        "tech": ["10.25-inch Touchscreen", "Wireless CarPlay"],
        "positive_sentiment_pct": 50.0
      },
      "Hyundai Creta": {
        "variant": "SX Tech",
        "price": 1680000.0,
        "mileage": 16.8,
        "fuel_type": "Petrol",
        "transmission": "Automatic",
        "engine": "1.5L MPi Petrol",
        "safety": ["6 Airbags", "ADAS Level 2", "ESC"],
        "tech": ["Panoramic Sunroof", "Ventilated Seats"],
        "positive_sentiment_pct": 66.67
      }
    }
  }
  ```
