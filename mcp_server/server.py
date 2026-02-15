import mcp.server.fastmcp as fastmcp
import random

# Create the MCP server
mcp_server = fastmcp.FastMCP("Weather MCP Server")


@mcp_server.tool()
def get_weather(city: str) -> dict:
    """
    Get the current weather for a city.

    Args:
        city: The name of the city to get weather for

    Returns:
        A dictionary containing weather information
    """
    # Simulate weather data (in a real app, you'd call a weather API)
    temperatures = list(range(10, 35))
    conditions = ["Sunny", "Cloudy", "Rainy", "Partly Cloudy", "Windy"]

    weather_data = {
        "city": city,
        "temperature": random.choice(temperatures),
        "condition": random.choice(conditions),
        "humidity": random.randint(30, 90),
        "wind_speed": random.randint(0, 30),
    }

    return weather_data


if __name__ == "__main__":
    mcp_server.run(transport="streamable-http")
