"""
GitHub Tool for AI Operations Assistant.
Searches GitHub repositories using the GitHub Search API.
"""

import requests
from typing import Dict, Any
from config import Config


class GitHubTool:
    """Tool for searching GitHub repositories."""
    
    def __init__(self):
        """Initialize GitHub tool."""
        self.api_url = Config.GITHUB_API_URL
    
    def search_repositories(self, query: str) -> Dict[str, Any]:
        """
        Search GitHub repositories for a given query.
        
        Args:
            query: Search query string
            
        Returns:
            Dictionary containing top repository information
            
        Raises:
            RuntimeError: If API call fails
        """
        params = {"q": query, "sort": "stars", "per_page": 1}
        
        try:
            response = requests.get(self.api_url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if not data.get("items"):
                return {
                    "name": "No results",
                    "stars": "0",
                    "url": "",
                    "description": "No repositories found"
                }
            
            repo = data["items"][0]
            
            return {
                "name": repo.get("name", ""),
                "stars": str(repo.get("stargazers_count", 0)),
                "url": repo.get("html_url", ""),
                "description": repo.get("description", "")
            }
            
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"GitHub API request failed: {e}")
