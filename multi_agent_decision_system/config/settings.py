"""
Configuration management for the multi-agent decision system.
"""

import os
from typing import Dict, Optional
from pydantic import Field
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings(BaseSettings):
    """Application settings with environment variable support."""
    
    # API Keys for LLM providers
    google_api_key: Optional[str] = Field(default=None)
    groq_api_key: Optional[str] = Field(default=None)
    huggingface_api_key: Optional[str] = Field(default=None)
    
    # Vector database settings
    vector_db_path: str = Field(default="./data/vector_store")
    embedding_model: str = Field(default="all-MiniLM-L6-v2")
    
    # File processing settings
    max_file_size_mb: int = Field(default=50)
    supported_file_types: list = Field(default=["csv", "json", "txt"])
    
    # Agent settings
    max_options_returned: int = Field(default=5)
    similarity_threshold: float = Field(default=0.7)
    
    # LLM settings
    llm_temperature: float = Field(default=0.1)
    max_tokens: int = Field(default=1000)
    
    # Interface settings
    streamlit_port: int = Field(default=8501)
    debug_mode: bool = Field(default=False)
    
    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "env_prefix": "",
        "case_sensitive": False,
        "extra": "ignore"
    }


class SecurityConfig:
    """Security configuration and validation."""
    
    @staticmethod
    def validate_api_keys(settings: Settings) -> Dict[str, bool]:
        """Validate that required API keys are present."""
        return {
            "google_api_key": bool(settings.google_api_key),
            "groq_api_key": bool(settings.groq_api_key),
            "huggingface_api_key": bool(settings.huggingface_api_key)
        }
    
    @staticmethod
    def get_available_llm_providers(settings: Settings) -> list:
        """Get list of available LLM providers based on API keys."""
        providers = []
        if settings.google_api_key:
            providers.append("google_gemini")
        if settings.groq_api_key:
            providers.append("groq_llama")
        if settings.huggingface_api_key:
            providers.append("huggingface")
        
        # Always include local transformers as fallback
        providers.append("local_transformers")
        return providers


# Global settings instance
settings = Settings()
security_config = SecurityConfig()