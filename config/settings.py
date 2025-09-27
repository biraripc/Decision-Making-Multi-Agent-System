"""Configuration management for the multi-agent decision system."""

import os
from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings with environment variable support."""
    
    # Google AI API configuration
    google_api_key: Optional[str] = Field(default=None, env="GOOGLE_API_KEY")
    
    # FAISS configuration
    faiss_index_path: str = Field(default="./data/faiss_index", env="FAISS_INDEX_PATH")
    
    # Embedding model configuration
    embedding_model: str = Field(default="all-MiniLM-L6-v2", env="EMBEDDING_MODEL")
    
    # LLM configuration
    llm_temperature: float = Field(default=0.7, env="LLM_TEMPERATURE")
    llm_max_tokens: int = Field(default=1000, env="LLM_MAX_TOKENS")
    
    # Search configuration
    search_top_k: int = Field(default=5, env="SEARCH_TOP_K")
    relevance_threshold: float = Field(default=0.7, env="RELEVANCE_THRESHOLD")
    
    # Retry configuration
    max_retries: int = Field(default=3, env="MAX_RETRIES")
    retry_delay: float = Field(default=1.0, env="RETRY_DELAY")
    max_retry_delay: float = Field(default=60.0, env="MAX_RETRY_DELAY")
    
    # UI configuration
    streamlit_port: int = Field(default=8501, env="STREAMLIT_PORT")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
    
    def validate_api_key(self) -> None:
        """Validate that the Google API key is configured."""
        if not self.google_api_key:
            raise ValueError(
                "Google API key is required. Please set GOOGLE_API_KEY environment variable."
            )


# Global settings instance
settings = Settings()