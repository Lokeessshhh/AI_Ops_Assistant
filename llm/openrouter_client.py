"""
NVIDIA LLM client for AI Operations Assistant.
Handles chat completions using NVIDIA's API with retry logic and error handling.
"""

import time
import json
from typing import List, Dict, Any, Optional
from openai import OpenAI
from config import Config


class OpenRouterClient:
    """Client for interacting with NVIDIA API using OpenAI SDK."""
    
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        """
        Initialize NVIDIA client.
        
        Args:
            api_key: NVIDIA API key (defaults to config)
            model: Model name (defaults to config)
        """
        self.api_key = api_key or Config.NVIDIA_API_KEY
        self.model = model or Config.NVIDIA_MODEL
        self.base_url = Config.NVIDIA_BASE_URL
        self.max_retries = Config.MAX_RETRIES
        self.retry_delay = Config.RETRY_DELAY
        
        self.client = OpenAI(
            base_url=self.base_url,
            api_key=self.api_key
        )
    
    def call_llm(
        self,
        messages: List[Dict[str, str]],
        temperature: float = Config.DEFAULT_TEMPERATURE,
        max_tokens: int = Config.DEFAULT_MAX_TOKENS,
        json_mode: bool = False
    ) -> str:
        """
        Call the LLM with given messages.
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            json_mode: If True, request JSON response
            
        Returns:
            LLM response content as string
        """
        for attempt in range(self.max_retries):
            try:
                completion = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    stream=False
                )
                
                content = completion.choices[0].message.content
                return content
                
            except Exception as e:
                if attempt < self.max_retries - 1:
                    print(f"API call failed (attempt {attempt + 1}/{self.max_retries}): {e}")
                    print(f"Retrying in {self.retry_delay} seconds...")
                    time.sleep(self.retry_delay)
                else:
                    raise RuntimeError(f"Failed to call LLM after {self.max_retries} attempts: {e}")
    
    def call_llm_with_json(
        self,
        messages: List[Dict[str, str]],
        temperature: float = Config.DEFAULT_TEMPERATURE,
        max_tokens: int = Config.DEFAULT_MAX_TOKENS
    ) -> Dict[str, Any]:
        """
        Call LLM and parse JSON response safely.
        
        Args:
            messages: List of message dicts
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            
        Returns:
            Parsed JSON object
            
        Raises:
            ValueError: If response cannot be parsed as JSON
        """
        response = self.call_llm(messages, temperature, max_tokens, json_mode=True)
        
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            raise ValueError(f"LLM response is not valid JSON: {response}")
