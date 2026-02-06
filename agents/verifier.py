"""
Verifier Agent for AI Operations Assistant.
Validates execution results and creates final structured summary.
"""

from typing import Dict, Any, List
from llm.openrouter_client import OpenRouterClient


class VerifierAgent:
    """Agent that verifies results and creates final summaries."""
    
    def __init__(self, llm_client: OpenRouterClient):
        """
        Initialize verifier agent.
        
        Args:
            llm_client: OpenRouter client instance
        """
        self.llm = llm_client
    
    def verify_results(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Verify execution results and create final structured summary.
        
        Args:
            results: List of execution results from executor
            
        Returns:
            Dictionary containing verified summary and status
        """
        system_prompt = """You are a verification agent for an AI Operations Assistant.
Your task is to review execution results and create a final structured summary.

Analyze the results:
1. Check if all steps completed successfully
2. Verify data completeness and formatting
3. Identify any missing or incomplete information
4. Create a clear, structured final answer

Output ONLY valid JSON in this format:
{
  "status": "success|partial|failed",
  "summary": "Clear summary of what was accomplished",
  "details": {
    "total_steps": number,
    "successful_steps": number,
    "failed_steps": number,
    "findings": ["key findings from results"]
  },
  "final_answer": {
    "structured_data": {
      "key": "value"
    }
  }
}

Rules:
1. Output ONLY JSON, no other text
2. Be thorough in your analysis
3. If data is missing, note it in findings
4. Organize final_answer clearly by topic
"""
        
        results_str = self._format_results_for_llm(results)
        user_message = f"Review these execution results and create a final summary:\n\n{results_str}"
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]
        
        try:
            verification = self.llm.call_llm_with_json(messages)
            
            if "status" not in verification or "summary" not in verification:
                raise ValueError("Verification must contain 'status' and 'summary' keys")
            
            verification["raw_results"] = results
            return verification
            
        except Exception as e:
            return {
                "status": "failed",
                "summary": f"Failed to verify results: {str(e)}",
                "details": {
                    "total_steps": len(results),
                    "successful_steps": sum(1 for r in results if r.get("status") == "success"),
                    "failed_steps": sum(1 for r in results if r.get("status") == "error"),
                    "findings": ["Verification failed"]
                },
                "final_answer": {},
                "error": str(e)
            }
    
    def _format_results_for_llm(self, results: List[Dict[str, Any]]) -> str:
        """Format results for LLM consumption."""
        formatted = []
        for i, result in enumerate(results):
            formatted.append(f"Step {i + 1}:")
            formatted.append(f"  Tool: {result.get('tool', 'unknown')}")
            formatted.append(f"  Status: {result.get('status', 'unknown')}")
            
            if result.get("status") == "success":
                result_data = result.get('result', {})
                # Truncate long descriptions to avoid JSON parsing issues
                if isinstance(result_data, dict):
                    summary_data = {}
                    for key, value in result_data.items():
                        if isinstance(value, str) and len(value) > 200:
                            summary_data[key] = value[:200] + "... [truncated]"
                        else:
                            summary_data[key] = value
                    formatted.append(f"  Result: {summary_data}")
                else:
                    formatted.append(f"  Result: {result_data}")
            else:
                formatted.append(f"  Error: {result.get('error', 'Unknown error')}")
            
            formatted.append("")
        
        return "\n".join(formatted)
