import os
import hashlib
from langchain_core.embeddings import Embeddings
from app.config import settings

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

def get_embeddings():
    if os.getenv("GEMINI_API_KEY"):
        try:
            from langchain_google_genai import GoogleGenerativeAIEmbeddings
            return GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        except Exception as e:
            print(f"Failed to load Google Embeddings: {e}. Trying SentenceTransformer...")
            
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
            print(f"Failed to initialize PGVector: {e}. Falling back to SQLite/Chroma local store.")
            
    # SQLite Fallback to Chroma
    try:
        from langchain_community.vectorstores import Chroma
        return Chroma(
            persist_directory="./chroma_db",
            embedding_function=embeddings,
            collection_name=collection_name
        )
    except Exception as e:
        print(f"Chroma load failed: {e}. Fallback to local memory vector store.")
        from langchain_community.vectorstores import DocArrayInMemorySearch
        return DocArrayInMemorySearch.from_texts(
            ["Mock car details: Tata Nexon is a compact SUV with 5-star safety rating and 17.5 kmpl mileage."],
            embeddings
        )
