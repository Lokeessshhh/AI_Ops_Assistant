"""
Planner Agent for AI Operations Assistant.
Converts natural language tasks into structured execution plans.
"""

from typing import Dict, Any
from llm.openrouter_client import OpenRouterClient


class PlannerAgent:
    """Agent that creates execution plans from natural language tasks."""
    
    def __init__(self, llm_client: OpenRouterClient):
        """
        Initialize planner agent.
        
        Args:
            llm_client: OpenRouter client instance
        """
        self.llm = llm_client
    
    def create_plan(self, task: str) -> Dict[str, Any]:
        """
        Create a structured execution plan from a natural language task.
        
        Args:
            task: Natural language description of the task
            
        Returns:
            Dictionary containing structured plan with steps
        """
        system_prompt = """You are a planning agent for an AI Operations Assistant. 
Your task is to convert natural language requests into structured execution plans.

You have access to these tools:
- github_search: Search GitHub repositories (use for finding repos, code, projects)
- weather_fetch: Get current weather information (use for weather queries)
- news_fetch: Get latest news articles (use for news, current events, topics)

Create a plan with steps. Each step must specify:
- tool: Either "github_search" or "weather_fetch"
- input: A clear description of what to search for or query

Output ONLY valid JSON in this exact format:
{
  "steps": [
    {
      "tool": "github_search",
      "input": "search query description"
    }
  ]
}

Rules:
1. Output ONLY JSON, no other text
2. Plan should be minimal but complete
3. Each step should be clear and actionable
4. Select the appropriate tool based on the task
5. If task involves multiple aspects, create multiple steps
"""
        
        user_message = f"Create an execution plan for this task: {task}"
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]
        
        try:
            plan = self.llm.call_llm_with_json(messages)
            
            if "steps" not in plan:
                raise ValueError("Plan must contain 'steps' key")
            
            if not isinstance(plan["steps"], list):
                raise ValueError("Steps must be a list")
            
            for step in plan["steps"]:
                if "tool" not in step or "input" not in step:
                    raise ValueError("Each step must have 'tool' and 'input' keys")
                
                if step["tool"] not in ["github_search", "weather_fetch", "news_fetch"]:
                    raise ValueError(f"Invalid tool: {step['tool']}")
            
            return plan
            
        except Exception as e:
            raise RuntimeError(f"Failed to create plan: {e}")
