import os
import hashlib
from langchain_core.embeddings import Embeddings
from langchain_core.documents import Document
from app.config import settings
from app.database.postgres import SessionLocal

class FallbackMockEmbeddings(Embeddings):
    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return [self._embed(t) for t in texts]
    
    def embed_query(self, text: str) -> list[float]:
        return self._embed(text)
        
    def _embed(self, text: str) -> list[float]:
        h = hashlib.sha256(text.encode('utf-8')).digest()
        vec = []
        for i in range(384):
            byte_idx = (i + sum(h)) % len(h)
            val = (h[byte_idx] / 255.0) * 2.0 - 1.0
            val += ((i * 17) % 100) / 1000.0
            vec.append(val)
        norm = sum(x**2 for x in vec) ** 0.5
        if norm > 0:
            vec = [x / norm for x in vec]
        return vec

class InMemoryMockVectorStore:
    def __init__(self, embeddings):
        self.embeddings = embeddings

    def similarity_search(self, query: str, k: int = 3, **kwargs) -> list[Document]:
        db = SessionLocal()
        try:
            from app.models.sql_models import Car
            # Fallback keyword matching on SQL to mimic search retrieval
            query_words = [w.lower() for w in query.split() if len(w) > 2]
            cars_query = db.query(Car)
            
            matched_cars = []
            if query_words:
                filters = []
                for word in query_words:
                    from sqlalchemy import or_
                    filters.append(Car.brand.ilike(f"%{word}%"))
                    filters.append(Car.model.ilike(f"%{word}%"))
                    filters.append(Car.fuel_type.ilike(f"%{word}%"))
                cars_query = cars_query.filter(or_(*filters))
            
            cars = cars_query.limit(k).all()
            if not cars:
                cars = db.query(Car).limit(k).all()
                
            docs = []
            for car in cars:
                text = (
                    f"Car details: {car.brand} {car.model} {car.variant}. Price: {car.price} INR. "
                    f"Fuel: {car.fuel_type}. Transmission: {car.transmission}. Specs: {car.engine_specs}. "
                    f"Safety: {', '.join(car.safety_features or [])}. Features: {', '.join(car.tech_features or [])}."
                )
                docs.append(Document(page_content=text, metadata={"car_id": car.id}))
            return docs
        except Exception as e:
            print(f"Mock vector store query failed: {e}")
            return [Document(page_content="Mock car details: Tata Nexon is a compact SUV with 5-star safety rating and 17.5 kmpl mileage.", metadata={})]
        finally:
            db.close()

def get_embeddings():
    if os.getenv("GEMINI_API_KEY"):
        try:
            from langchain_google_genai import GoogleGenerativeAIEmbeddings
            return GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        except Exception as e:
            print(f"Failed to load Google Embeddings: {e}. Trying local fallback...")
            
    try:
        from langchain_community.embeddings import HuggingFaceEmbeddings
        return HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    except Exception as e:
        print(f"Failed to load HuggingFace Embeddings: {e}. Using deterministic mock embeddings.")
        return FallbackMockEmbeddings()

def get_vector_store(collection_name: str = "car_specifications"):
    embeddings = get_embeddings()
    
    if settings.DATABASE_URL.startswith("postgresql"):
        try:
            from langchain_community.vectorstores import PGVector
            return PGVector(
                connection_string=settings.DATABASE_URL,
                embedding_function=embeddings,
                collection_name=collection_name
            )
        except Exception as e:
            print(f"Failed to initialize PGVector: {e}. Falling back to default store.")
            
    # Try Chroma
    try:
        from langchain_community.vectorstores import Chroma
        return Chroma(
            persist_directory="./chroma_db",
            embedding_function=embeddings,
            collection_name=collection_name
        )
    except Exception as e:
        print(f"Chroma load failed: {e}. Using lightweight in-memory SQL mock vector store.")
        return InMemoryMockVectorStore(embeddings)
