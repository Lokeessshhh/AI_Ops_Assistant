"""
Main orchestrator for AI Operations Assistant.
Coordinates planner, executor, and verifier agents to complete tasks.
"""

import json
import sys
from config import Config
from llm.openrouter_client import OpenRouterClient
from agents.planner import PlannerAgent
from agents.executor import ExecutorAgent
from agents.verifier import VerifierAgent


class AIOpsAssistant:
    """Main orchestrator for AI Operations Assistant."""
    
    def __init__(self):
        """Initialize the AI Operations Assistant."""
        try:
            Config.validate()
        except ValueError as e:
            print(f"Configuration error: {e}")
            print("Please ensure .env file is set up correctly.")
            sys.exit(1)
        
        self.llm = OpenRouterClient()
        self.planner = PlannerAgent(self.llm)
        self.executor = ExecutorAgent()
        self.verifier = VerifierAgent(self.llm)
    
    def process_task(self, task: str) -> dict:
        """
        Process a natural language task through the multi-agent pipeline.
        
        Args:
            task: Natural language description of the task
            
        Returns:
            Dictionary containing final results
        """
        print("=" * 60)
        print("AI Operations Assistant")
        print("=" * 60)
        print(f"\nTask: {task}\n")
        
        # Step 1: Planning
        print("[Planner] Creating execution plan...")
        try:
            plan = self.planner.create_plan(task)
            print(f"[Planner] Plan created with {len(plan['steps'])} step(s)")
            print(json.dumps(plan, indent=2))
        except Exception as e:
            print(f"[Planner] Error: {e}")
            return {"status": "failed", "error": str(e), "stage": "planning"}
        
        # Step 2: Execution
        print("\n[Executor] Executing plan...")
        results = self.executor.execute_plan(plan)
        
        # Step 3: Verification
        print("\n[Verifier] Verifying results and creating summary...")
        verification = self.verifier.verify_results(results)
        
        # Step 4: Final Output
        print("\n" + "=" * 60)
        print("FINAL RESULT")
        print("=" * 60)
        print(f"\nStatus: {verification['status'].upper()}")
        print(f"\nSummary:\n{verification['summary']}\n")
        
        print("Details:")
        print(f"  Total steps: {verification['details']['total_steps']}")
        print(f"  Successful: {verification['details']['successful_steps']}")
        print(f"  Failed: {verification['details']['failed_steps']}")
        
        if verification['details']['findings']:
            print("\nKey Findings:")
            for finding in verification['details']['findings']:
                print(f"  - {finding}")
        
        if verification.get('final_answer'):
            print("\nFinal Answer:")
            print(json.dumps(verification['final_answer'], indent=2))
        
        return verification


def main():
    """Main entry point for CLI usage."""
    print("\nAI Operations Assistant - Multi-Agent System")
    print("Enter a task or 'quit' to exit\n")
    
    assistant = AIOpsAssistant()
    
    while True:
        try:
            task = input("Task> ").strip()
            
            if not task:
                continue
            
            if task.lower() in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break
            
            assistant.process_task(task)
            print("\n")
            
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"\nError: {e}\n")


if __name__ == "__main__":
    main()
