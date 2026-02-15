# Weather Expert Agent with MCP Server

A simple weather expert agent built with FastAPI and OpenAI SDK, using an MCP server with fast-mcp for weather data.

## Project Structure

```plaintext
weather-agent-mcp/
├── .github/
│   └── workflows/
│       └── code-quality.yml  # CI checks (ruff, black, pyright)
├── agent/
│   └── main.py               # FastAPI agent with OpenAI SDK
├── mcp_server/
│   └── server.py             # MCP server with weather tool
├── .env                      # Environment variables (not committed)
├── .gitignore
├── pyproject.toml             # Project config and dependencies
└── test.sh                    # Manual test script
```

## Setup

Requires Python 3.10+ and [uv](https://docs.astral.sh/uv/).

1. Install dependencies:

   ```bash
   uv sync --all-groups
   ```

2. Create a `.env` file with your OpenAI API key:

   ```bash
   echo 'OPENAI_API_KEY=your-api-key-here' > .env
   ```

## Running the Agent

Start the FastAPI agent:

```bash
uv run python agent/main.py
```

The agent will be available at `http://localhost:8000`

## Using the Agent

### Interactive API Docs

Visit `http://localhost:8000/docs` for interactive API documentation.

### Example Request

```bash
curl -X POST "http://localhost:8000/ask" \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the weather like in London?"}'
```

### Example with Python

```python
import requests

response = requests.post(
    "http://localhost:8000/ask",
    json={"question": "What is the weather like in Paris?"}
)
print(response.json())
```

## How It Works

1. **MCP Server** (`mcp_server/server.py`): Provides a `get_weather` tool that returns weather data for a city
2. **FastAPI Agent** (`agent/main.py`):
   - Receives questions from users
   - Uses OpenAI SDK to process the question
   - Calls the weather tool when needed
   - Returns a natural language response

## Code Quality

CI runs ruff, black, and pyright on pull requests. Run locally:

```bash
uv run ruff check .
uv run black --check .
uv run pyright agent/ mcp_server/ --pythonversion 3.13
```

## Example Questions

- "What's the weather in Tokyo?"
- "Is it raining in Seattle?"
- "Tell me about the weather in New York"
- "What's the temperature in Sydney?"
