"""
Weather Tool for AI Operations Assistant.
Fetches current weather information using WeatherAPI.
"""

import requests
from typing import Dict, Any
from config import Config


class WeatherTool:
    """Tool for fetching weather information."""
    
    def __init__(self):
        """Initialize weather tool."""
        self.api_url = Config.WEATHER_API_URL
        self.api_key = Config.WEATHER_API_KEY
    
    def get_weather(self, city: str) -> Dict[str, Any]:
        """
        Get current weather for a city.
        
        Args:
            city: City name
            
        Returns:
            Dictionary containing weather information
            
        Raises:
            RuntimeError: If API call fails
        """
        params = {"key": self.api_key, "q": city}
        
        try:
            response = requests.get(self.api_url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if "error" in data:
                raise RuntimeError(f"Weather API error: {data['error']['message']}")
            
            current = data.get("current", {})
            location = data.get("location", {})
            
            return {
                "city": location.get("name", city),
                "temperature_c": str(current.get("temp_c", "N/A")),
                "condition": current.get("condition", {}).get("text", "N/A")
            }
            
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Weather API request failed: {e}")
