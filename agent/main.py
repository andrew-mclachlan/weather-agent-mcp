from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI
from openai.types.chat import (
    ChatCompletionMessageParam,
    ChatCompletionToolMessageParam,
    ChatCompletionToolParam,
)
from dotenv import load_dotenv
import os
import json

load_dotenv()

app = FastAPI(title="Weather Expert Agent")

MODEL = "gpt-5.2"

client = OpenAI(
    api_key=os.environ["OPENAI_API_KEY"],
)


class QueryRequest(BaseModel):
    question: str


def call_weather_tool(city: str) -> dict:
    """Call the MCP server's weather tool"""
    try:
        import sys
        from pathlib import Path

        sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "mcp_server"))
        from server import get_weather  # type: ignore[import-not-found]

        return get_weather(city)
    except Exception as e:
        return {"error": f"Failed to get weather: {str(e)}"}


# Define the tool for OpenAI
tools: list[ChatCompletionToolParam] = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get the current weather for a city",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "The name of the city to get weather for",
                    }
                },
                "required": ["city"],
            },
        },
    }
]


@app.post("/ask")
async def ask_agent(request: QueryRequest):
    """
    Ask the weather expert agent a question.
    The agent can use the weather tool to answer questions.
    """
    try:
        messages: list[ChatCompletionMessageParam] = [
            {
                "role": "system",
                "content": "You are a helpful weather expert assistant. Use the get_weather tool to answer questions about weather in different cities.",
            },
            {"role": "user", "content": request.question},
        ]

        # First call to OpenAI
        response = client.chat.completions.create(
            model=MODEL, messages=messages, tools=tools, tool_choice="auto"
        )

        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls

        # If the model wants to call a tool
        if tool_calls:
            messages.append(response_message.to_dict())  # type: ignore[arg-type]

            # Process each tool call
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)

                if function_name == "get_weather":
                    function_response = call_weather_tool(function_args["city"])
                else:
                    function_response = {"error": "Unknown function"}

                tool_message: ChatCompletionToolMessageParam = {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "content": json.dumps(function_response),
                }
                messages.append(tool_message)

            # Second call to get the final response
            second_response = client.chat.completions.create(
                model=MODEL, messages=messages, tools=tools
            )

            return {
                "response": second_response.choices[0].message.content,
                "tool_used": True,
            }
        else:
            return {"response": response_message.content, "tool_used": False}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
async def root():
    return {
        "message": "Weather Expert Agent API",
        "endpoints": {
            "/ask": "POST - Ask the weather agent a question",
            "/docs": "GET - Interactive API documentation",
        },
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
