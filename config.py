import os
from typing import Optional
from pydantic import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Solution IDs for fallback tools
    expedite_solution_id: str = "default_expedite_001"
    manual_solution_id: str = "default_manual_002"
    
    # Environment identifier
    environment: str = "local"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


def get_settings() -> Settings:
    """Get application settings instance."""
    return Settings()


# Global settings instance
settings = get_settings()