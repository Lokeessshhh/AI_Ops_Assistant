"""
Executor Agent for AI Operations Assistant.
Executes plans by calling appropriate tools and handling errors.
"""

from typing import Dict, Any, List
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.github_tool import GitHubTool
from tools.weather_tool import WeatherTool
from tools.news_tool import NewsTool


class ExecutorAgent:
    """Agent that executes plans by calling tools."""
    
    def __init__(self):
        """Initialize executor agent with tools."""
        self.tools = {
            "github_search": GitHubTool(),
            "weather_fetch": WeatherTool(),
            "news_fetch": NewsTool()
        }
    
    def execute_plan(self, plan: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Execute a plan by calling tools for each step.
        
        Args:
            plan: Dictionary containing execution plan with steps
            
        Returns:
            List of results from each step execution
        """
        results = []
        
        for i, step in enumerate(plan["steps"]):
            tool_name = step["tool"]
            tool_input = step["input"]
            
            print(f"\n[Executor] Step {i + 1}/{len(plan['steps'])}")
            print(f"  Tool: {tool_name}")
            print(f"  Input: {tool_input}")
            
            try:
                if tool_name not in self.tools:
                    raise ValueError(f"Unknown tool: {tool_name}")
                
                tool = self.tools[tool_name]
                
                if tool_name == "github_search":
                    result = tool.search_repositories(tool_input)
                elif tool_name == "weather_fetch":
                    result = tool.get_weather(tool_input)
                elif tool_name == "news_fetch":
                    result = tool.get_news(tool_input)
                else:
                    raise ValueError(f"Tool not implemented: {tool_name}")
                
                results.append({
                    "step": i + 1,
                    "tool": tool_name,
                    "input": tool_input,
                    "status": "success",
                    "result": result
                })
                
                print("  Status: Success")
                
            except Exception as e:
                error_result = {
                    "step": i + 1,
                    "tool": tool_name,
                    "input": tool_input,
                    "status": "error",
                    "error": str(e)
                }
                results.append(error_result)
                print(f"  Status: Error - {e}")
        
        return results
