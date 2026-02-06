# AI Operations Assistant

A production-ready multi-agent system that accepts natural language tasks, creates execution plans, calls API tools, verifies results, and returns structured answers.

## Architecture

The system uses a three-agent architecture:

```
User Input → Planner → Executor → Verifier → Final Output
```

### Components

- **Planner Agent**: Converts natural language tasks into structured JSON execution plans
- **Executor Agent**: Executes plans by calling appropriate tools (GitHub, Weather)
- **Verifier Agent**: Validates results and creates final structured summaries

### Tools

- **GitHub Tool**: Searches GitHub repositories using the GitHub Search API
- **Weather Tool**: Fetches current weather information using WeatherAPI
- **News Tool**: Fetches latest news articles using NewsAPI

### LLM Provider

Uses **NVIDIA API** with OpenAI SDK for model inference.

Supported models include:
- `meta/llama-3.1-8b-instruct`
- `meta/llama-3.1-70b-instruct`
- `meta/llama-3.3-70b-instruct`

## Project Structure

```
ai_ops_assistant/
│
├── agents/
│   ├── planner.py      # Creates execution plans from tasks
│   ├── executor.py     # Executes plans by calling tools
│   └── verifier.py     # Validates results and creates summaries
│
├── tools/
│   ├── github_tool.py  # GitHub repository search
│   ├── weather_tool.py # Weather information fetch
│   └── news_tool.py    # News articles fetch
│
├── llm/
│   └── openrouter_client.py  # NVIDIA API client with OpenAI SDK with retry logic
│
├── main.py             # Main orchestrator and CLI
├── streamlit_app.py    # Streamlit web interface
├── config.py           # Configuration management
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variables template
└── README.md           # This file
```

## Setup

### Prerequisites

- Python 3.8+
- NVIDIA API key (get from https://build.nvidia.com/)
- WeatherAPI key (get from https://www.weatherapi.com/)
- NewsAPI key (get from https://newsapi.org/)

### Installation

1. Clone or navigate to the project directory:
```bash
cd ai_ops_assistant
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file from the example:
```bash
cp .env.example .env
```

4. Edit `.env` and add your API keys:
```env
NVIDIA_API_KEY=your_nvidia_api_key_here
NVIDIA_MODEL=meta/llama-3.1-8b-instruct
WEATHER_API_KEY=your_weather_api_key_here
NEWS_API_KEY=your_news_api_key_here
```

## Running

### Interactive Mode (CLI)

Run the main script to start the interactive CLI:

```bash
python main.py
```

### Web Interface (Streamlit)

Launch the Streamlit web interface:

**Windows:**
```bash
python -m streamlit run streamlit_app.py
```

**Linux/Mac:**
```bash
streamlit run streamlit_app.py
```

The web interface provides:
- Modern, user-friendly UI
- Task input with example suggestions
- Real-time execution progress
- Structured result display
- Expandable sections for details

You'll see a prompt where you can enter tasks:

```
AI Operations Assistant - Multi-Agent System
Enter a task or 'quit' to exit

Task> Find top AI GitHub repo and current weather in Mumbai
```

### Example Tasks

Try these example tasks:

1. **GitHub Search**: "Find the top repository for machine learning"
2. **Weather Query**: "Get current weather in London"
3. **News Query**: "Get latest news about AI technology"
4. **Combined Task**: "Find top AI GitHub repo and current weather in Mumbai"
5. **Specific Search**: "Search for Python web frameworks on GitHub"
6. **Weather Check**: "What's the weather like in New York?"
7. **News Check**: "What are the latest headlines about technology?"

### Example Output

```
============================================================
AI Operations Assistant
============================================================

Task: Find top AI GitHub repo and current weather in Mumbai

[Planner] Creating execution plan...
[Planner] Plan created with 2 step(s)
{
  "steps": [
    {
      "tool": "github_search",
      "input": "AI"
    },
    {
      "tool": "weather_fetch",
      "input": "Mumbai"
    }
  ]
}

[Executor] Executing plan...

[Executor] Step 1/2
  Tool: github_search
  Input: AI
  Status: Success

[Executor] Step 2/2
  Tool: weather_fetch
  Input: Mumbai
  Status: Success

[Verifier] Verifying results and creating summary...

============================================================
FINAL RESULT
============================================================

Status: SUCCESS

Summary:
Successfully retrieved top AI repository from GitHub and current weather for Mumbai.

Details:
  Total steps: 2
  Successful: 2
  Failed: 0

Key Findings:
  - Found top AI repository with detailed information
  - Retrieved current weather conditions for Mumbai

Final Answer:
{
  "github_result": {
    "name": "repository-name",
    "stars": "1000",
    "url": "https://github.com/...",
    "description": "..."
  },
  "weather_result": {
    "city": "Mumbai",
    "temperature_c": "32",
    "condition": "Sunny"
  }
}
```

## Features

- **Multi-Agent Architecture**: Planner → Executor → Verifier pipeline
- **Modular Architecture**: Clean separation between agents and tools
- **Type Hints**: Full type annotations for better IDE support
- **Error Handling**: Comprehensive error handling with retry logic
- **JSON Mode**: Structured JSON output from LLM when needed
- **CLI Interface**: Interactive command-line interface
- **Web Interface**: Modern Streamlit UI for easy access
- **Configurable**: Easy to modify models and API settings
- **Production Ready**: Robust error handling and logging

## Configuration

The system can be configured via environment variables in `.env`:

- `NVIDIA_API_KEY`: Required API key for NVIDIA
- `NVIDIA_MODEL`: LLM model to use (default: `meta/llama-3.1-8b-instruct`)
- `WEATHER_API_KEY`: Required API key for WeatherAPI
- `NEWS_API_KEY`: Required API key for NewsAPI

## Adding New Tools

To add a new tool:

1. Create a new file in `tools/` directory
2. Implement a class with methods that return structured data
3. Add the tool to `ExecutorAgent.__init__()` in `agents/executor.py`
4. Update the Planner agent's system prompt to include the new tool

Example:

```python
# tools/new_tool.py
class NewTool:
    def do_something(self, query: str) -> Dict[str, Any]:
        # Implementation
        return {"result": "data"}
```

## Error Handling

The system includes:

- **Retry Logic**: Automatic retries for failed API calls (3 attempts)
- **Graceful Degradation**: Continues execution even if one step fails
- **Detailed Logging**: Clear error messages for debugging
- **JSON Parsing Safety**: Safe JSON parsing with error handling

## Development

### Code Style

- PEP 8 compliant
- Type hints throughout
- Docstrings for all functions and classes
- Clear separation of concerns

### Testing

To test the system:

```bash
python main.py
```

Then enter a task to see the full workflow in action.

## License

This project is provided as-is for educational and production use.

## Support

For issues or questions, please refer to the code documentation or check the error messages in the CLI output.
