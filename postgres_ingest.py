import os
from sqlalchemy.orm import Session
from app.database.postgres import SessionLocal
from app.models.sql_models import Car, YoutubeReviewSummary, CustomerSentiment
from app.database.vector_store import get_embeddings, get_vector_store
from app.config import settings

def ingest_data_to_pgvector():
    print(f"Connecting to vector database via connection string...")
    
    # Initialize the PGVector stores (one for specs, one for reviews)
    spec_store = get_vector_store("car_specifications")
    review_store = get_vector_store("car_reviews")
    
    db: Session = SessionLocal()
    
    cars = db.query(Car).all()
    if not cars:
        print("No cars found in database. Seed PostgreSQL first before running vector ingestion.")
        db.close()
        return

    print(f"\nProcessing {len(cars)} cars for PGVector indexing...")
    
    for car in cars:
        car_name = f"{car.brand} {car.model}"
        print(f"Indexing vector embeddings for: {car_name}...")
        
        # 1. Spec Text Ingestion
        safety_str = ", ".join(car.safety_features or [])
        tech_str = ", ".join(car.tech_features or [])
        spec_text = (
            f"Car details: {car.brand} {car.model} {car.variant}. "
            f"Price: {car.price} INR. Mileage: {car.mileage} kmpl. "
            f"Fuel Type: {car.fuel_type}. Transmission: {car.transmission}. "
            f"Engine Specs: {car.engine_specs or 'N/A'}. "
            f"Safety Features: {safety_str or 'None'}. "
            f"Tech Features: {tech_str or 'None'}."
        )
        
        spec_metadata = {
            "car_id": car.id,
            "brand": car.brand,
            "model": car.model,
            "price": car.price,
            "fuel_type": car.fuel_type
        }
        
        # Add specs to PGVector / local store fallback
        spec_store.add_texts(
            texts=[spec_text],
            metadatas=[spec_metadata],
            ids=[f"spec_{car.id}"]
        )
        
        # 2. YouTube Summaries & Sentiment Ingestion
        summary = db.query(YoutubeReviewSummary).filter(YoutubeReviewSummary.car_id == car.id).first()
        sentiment = db.query(CustomerSentiment).filter(CustomerSentiment.car_id == car.id).first()
        
        review_parts = [f"Reviews for {car_name}:"]
        if summary:
            pros_str = ", ".join(summary.pros or [])
            cons_str = ", ".join(summary.cons or [])
            complaints_str = ", ".join(summary.common_complaints or [])
            review_parts.append(
                f"Expert Summary: {summary.summary_text} "
                f"Pros: {pros_str}. Cons: {cons_str}. "
                f"Observed Mileage: {summary.mileage_observed or 'N/A'}. "
                f"Ride Quality: {summary.ride_quality or 'N/A'}. "
                f"Complaints: {complaints_str}."
            )
        if sentiment:
            review_parts.append(
                f"Customer Sentiment: Positive={sentiment.positive_percentage}%, "
                f"Negative={sentiment.negative_percentage}%, Neutral={sentiment.neutral_percentage}%. "
                f"Summary: {sentiment.sentiment_summary}"
            )
            
        review_text = " ".join(review_parts)
        review_metadata = {
            "car_id": car.id,
            "brand": car.brand,
            "model": car.model
        }
        
        review_store.add_texts(
            texts=[review_text],
            metadatas=[review_metadata],
            ids=[f"review_{car.id}"]
        )
        
    db.close()
    print("\nVector ingestion pipeline completed successfully!")

if __name__ == "__main__":
    ingest_data_to_pgvector()
