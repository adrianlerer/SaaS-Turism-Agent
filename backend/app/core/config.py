"""
Core configuration for TravelAgent Pro
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional
import secrets


class Settings(BaseSettings):
    """Application settings"""
    
    # API Settings
    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "TravelAgent Pro"
    VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # Security
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    ALGORITHM: str = "HS256"
    
    # Database
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/travelagent"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    CACHE_TTL: int = 3600
    
    # External APIs
    OPENAI_API_KEY: Optional[str] = None
    GOOGLE_MAPS_API_KEY: Optional[str] = None
    AMADEUS_API_KEY: Optional[str] = None
    AMADEUS_API_SECRET: Optional[str] = None
    OPENWEATHER_API_KEY: Optional[str] = None
    
    # Agent Configuration
    AGENT_MODEL: str = "gpt-4-turbo-preview"
    AGENT_TEMPERATURE: float = 0.7
    MAX_ITERATIONS: int = 10
    MAX_EXECUTION_TIME: int = 300  # seconds
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    
    # CORS
    ALLOWED_ORIGINS: list = ["http://localhost:3000", "http://localhost:5173"]
    
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)


settings = Settings()
