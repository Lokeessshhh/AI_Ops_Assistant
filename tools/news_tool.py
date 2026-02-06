"""
News Tool for AI Operations Assistant.
Fetches latest news articles using NewsAPI.
"""

import requests
from typing import Dict, Any
from config import Config


class NewsTool:
    """Tool for fetching news articles."""
    
    def __init__(self):
        """Initialize news tool."""
        self.api_url = Config.NEWS_API_URL
        self.api_key = Config.NEWS_API_KEY
    
    def get_news(self, query: str, max_results: int = 5) -> Dict[str, Any]:
        """
        Get latest news articles for a given query.
        
        Args:
            query: Search query for news
            max_results: Maximum number of articles to return
            
        Returns:
            Dictionary containing news articles
            
        Raises:
            RuntimeError: If API call fails
        """
        params = {
            "q": query,
            "apiKey": self.api_key,
            "pageSize": max_results,
            "language": "en"
        }
        
        try:
            response = requests.get(self.api_url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get("status") != "ok":
                raise RuntimeError(f"News API error: {data.get('message', 'Unknown error')}")
            
            articles = []
            for article in data.get("articles", [])[:max_results]:
                articles.append({
                    "title": article.get("title", ""),
                    "description": article.get("description", ""),
                    "url": article.get("url", ""),
                    "source": article.get("source", {}).get("name", ""),
                    "published_at": article.get("publishedAt", "")
                })
            
            return {
                "query": query,
                "total_results": len(articles),
                "articles": articles
            }
            
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"News API request failed: {e}")
