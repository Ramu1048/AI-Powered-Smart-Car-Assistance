import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Default to memory-based database on Vercel to prevent read-only filesystem crashes
    DATABASE_URL: str = "sqlite:///:memory:" if os.getenv("VERCEL") else "sqlite:///./smart_car_db.db"
    JWT_SECRET_KEY: str = "supersecretkeychangeinproduction"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
