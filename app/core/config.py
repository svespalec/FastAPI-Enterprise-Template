from typing import List
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI Advanced Template"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "Advanced FastAPI application with modern best practices"
    API_V1_STR: str = "/api/v1"
    
    # Security
    SECRET_KEY: str = "your-secret-key-here"  # Change in production
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Database
    DATABASE_URL: str = "postgresql://postgres:postgres@db:5432/fastapi_db"
    
    # Redis
    REDIS_URL: str = "redis://redis:6379/0"
    
    # CORS
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost",
        "http://localhost:8000",
        "http://localhost:3000",
    ]

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings() 