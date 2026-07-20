import os
import hashlib
from sqlalchemy.orm import Session
from app.database.postgres import SessionLocal
from app.models.sql_models import Car, YoutubeReviewSummary, CustomerSentiment

# Try importing chromadb and sentence_transformers
try:
    import chromadb
    CHROMA_AVAILABLE = True
except ImportError:
    CHROMA_AVAILABLE = False

try:
    from sentence_transformers import SentenceTransformer
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False

def get_fallback_embedding(text: str, dimension: int = 384) -> list:
    """Generates a deterministic 384-dimensional unit vector from a text string."""
    h = hashlib.sha256(text.encode('utf-8')).digest()
    vec = []
    for i in range(dimension):
        byte_idx = (i + sum(h)) % len(h)
        val = (h[byte_idx] / 255.0) * 2.0 - 1.0
        val += ((i * 17) % 100) / 1000.0  # Add structural variance
        vec.append(float(val))
    # Normalize to unit length
    norm = sum(x**2 for x in vec) ** 0.5
    if norm > 0:
        vec = [x / norm for x in vec]
    return vec

class EmbeddingGenerator:
    def __init__(self):
        self.model = None
        if TRANSFORMERS_AVAILABLE:
            try:
                print("Loading SentenceTransformer model ('all-MiniLM-L6-v2')...")
                self.model = SentenceTransformer("all-MiniLM-L6-v2")
                print("Model loaded successfully.")
            except Exception as e:
                print(f"Error loading sentence-transformers model: {e}. Falling back to deterministic embeddings.")
                self.model = None

    def get_embedding(self, text: str) -> list:
        if self.model:
            try:
                return self.model.encode(text).tolist()
            except Exception as e:
                print(f"Embedding failed: {e}. Falling back to deterministic.")
        return get_fallback_embedding(text)

def ingest_data_to_chromadb():
    if not CHROMA_AVAILABLE:
        print("ChromaDB is not installed or available. Skipping vector ingestion.")
        return

    print("Connecting to persistent ChromaDB client...")
    chroma_client = chromadb.PersistentClient(path="./chroma_db")
    
    # Create or get collections
    spec_collection = chroma_client.get_or_create_collection(name="car_specifications")
    review_collection = chroma_client.get_or_create_collection(name="car_reviews")
    
    embedder = EmbeddingGenerator()
    db: Session = SessionLocal()
    
    cars = db.query(Car).all()
    if not cars:
        print("No cars found in database. Seed PostgreSQL first before running Chroma ingestion.")
        db.close()
        return

    print(f"\nProcessing {len(cars)} cars for vector indexing...")
    
    for car in cars:
        car_name = f"{car.brand} {car.model}"
        print(f"Indexing vector embeddings for: {car_name}...")
        
        # 1. Index specifications
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
        
        spec_embedding = embedder.get_embedding(spec_text)
        spec_metadata = {
            "car_id": car.id,
            "brand": car.brand,
            "model": car.model,
            "price": car.price,
            "fuel_type": car.fuel_type
        }
        
        # Add to spec collection
        spec_collection.upsert(
            ids=[f"spec_{car.id}"],
            embeddings=[spec_embedding],
            metadatas=[spec_metadata],
            documents=[spec_text]
        )
        
        # 2. Index YouTube summaries and sentiment analysis
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
        
        review_embedding = embedder.get_embedding(review_text)
        review_metadata = {
            "car_id": car.id,
            "brand": car.brand,
            "model": car.model
        }
        
        # Add to review collection
        review_collection.upsert(
            ids=[f"review_{car.id}"],
            embeddings=[review_embedding],
            metadatas=[review_metadata],
            documents=[review_text]
        )
        
    db.close()
    print("\nChromaDB vector ingestion pipeline completed successfully!")

if __name__ == "__main__":
    ingest_data_to_chromadb()
