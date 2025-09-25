"""
Tests for configuration management.
"""

import pytest
from unittest.mock import patch
from multi_agent_decision_system.config.settings import Settings, SecurityConfig


class TestSettings:
    """Test cases for Settings class."""

    def test_default_settings(self):
        """Test that default settings are loaded correctly."""
        settings = Settings()
        
        assert settings.vector_db_path == "./data/vector_store"
        assert settings.embedding_model == "all-MiniLM-L6-v2"
        assert settings.max_file_size_mb == 50
        assert settings.supported_file_types == ["csv", "json", "txt"]
        assert settings.max_options_returned == 5
        assert settings.similarity_threshold == 0.7
        assert settings.llm_temperature == 0.1
        assert settings.max_tokens == 1000
        assert settings.streamlit_port == 8501
        assert settings.debug_mode is False

    @patch.dict('os.environ', {'GOOGLE_API_KEY': 'test_key'})
    def test_api_key_from_env(self):
        """Test that API keys are loaded from environment variables."""
        settings = Settings()
        assert settings.google_api_key == 'test_key'

    @patch.dict('os.environ', {'MAX_FILE_SIZE_MB': '100'})
    def test_env_override(self):
        """Test that environment variables override defaults."""
        settings = Settings()
        assert settings.max_file_size_mb == 100


class TestSecurityConfig:
    """Test cases for SecurityConfig class."""

    def test_validate_api_keys_all_none(self):
        """Test API key validation when no keys are present."""
        settings = Settings()
        result = SecurityConfig.validate_api_keys(settings)
        
        expected = {
            "google_api_key": False,
            "groq_api_key": False,
            "huggingface_api_key": False
        }
        assert result == expected

    @patch.dict('os.environ', {'GOOGLE_API_KEY': 'test_key'})
    def test_validate_api_keys_with_google(self):
        """Test API key validation with Google key present."""
        settings = Settings()
        result = SecurityConfig.validate_api_keys(settings)
        
        assert result["google_api_key"] is True
        assert result["groq_api_key"] is False
        assert result["huggingface_api_key"] is False

    def test_get_available_llm_providers_default(self):
        """Test available LLM providers with no API keys."""
        settings = Settings()
        providers = SecurityConfig.get_available_llm_providers(settings)
        
        assert "local_transformers" in providers
        assert len(providers) == 1

    @patch.dict('os.environ', {
        'GOOGLE_API_KEY': 'test_key',
        'GROQ_API_KEY': 'test_key'
    })
    def test_get_available_llm_providers_with_keys(self):
        """Test available LLM providers with API keys present."""
        settings = Settings()
        providers = SecurityConfig.get_available_llm_providers(settings)
        
        assert "google_gemini" in providers
        assert "groq_llama" in providers
        assert "local_transformers" in providers
        assert len(providers) == 3