"""
Configuration module for AI Operations Assistant.
Loads environment variables and provides configuration settings.
"""

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Configuration settings for the application."""
    
    # API Keys
    NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY")
    WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
    NEWS_API_KEY = os.getenv("NEWS_API_KEY")
    
    # NVIDIA API Settings
    NVIDIA_BASE_URL = "https://integrate.api.nvidia.com/v1"
    NVIDIA_MODEL = os.getenv("NVIDIA_MODEL", "meta/llama-3.1-8b-instruct")
    
    # API Endpoints
    GITHUB_API_URL = "https://api.github.com/search/repositories"
    WEATHER_API_URL = "http://api.weatherapi.com/v1/current.json"
    NEWS_API_URL = "https://newsapi.org/v2/everything"
    
    # Retry Settings
    MAX_RETRIES = 3
    RETRY_DELAY = 1
    
    # LLM Settings
    DEFAULT_TEMPERATURE = 0
    DEFAULT_MAX_TOKENS = 1000
    
    @classmethod
    def validate(cls) -> bool:
        """Validate required configuration is present."""
        if not cls.NVIDIA_API_KEY:
            raise ValueError("NVIDIA_API_KEY is required")
        if not cls.WEATHER_API_KEY:
            raise ValueError("WEATHER_API_KEY is required")
        if not cls.NEWS_API_KEY:
            raise ValueError("NEWS_API_KEY is required")
        return True
