import requests

from typing import TypedDict
from datasets import load_dataset
from pydantic import BaseModel, Field

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Geolocation MCP Example")


# Using Pydantic models for rich structured data
class WeatherData(BaseModel):
    """Weather information structure."""

    temperature: float = Field(description="Temperature in Celsius")
    humidity: float = Field(description="Humidity percentage")
    condition: str
    wind_speed: float


@mcp.tool()
def get_weather(city: str) -> WeatherData:
    """Get weather for a city - returns structured data."""
    # Simulated weather data
    return WeatherData(
        temperature=22.5,
        humidity=45.0,
        condition="sunny",
        wind_speed=5.2,
    )


# Loading dataset from huggingface (jamescalam/world-cities-geo)
dataset = load_dataset("jamescalam/world-cities-geo")["train"]

# Using TypedDict for simpler structures
class LocationInfo(TypedDict):
    city: str
    country: str
    region: str
    continent: str
    latitude: float
    longitude: float

@mcp.tool()
def get_location(city_name: str) -> LocationInfo:
    """Get geographic location info"""
    city_data = next(
        (item for item in dataset if item["city"].lower() == city_name.lower()), None
    )
    if not city_data:
        raise ValueError(f"City '{city_name}' does not exist in the dataset.")

    return LocationInfo(
        city=city_data["city"],
        country=city_data["country"],
        region=city_data["region"],
        continent=city_data["continent"],
        latitude=city_data["latitude"],
        longitude=city_data["longitude"],
    )

# Using dict[str, Any] for flexible schemas
@mcp.tool()
def get_statistics(data_type: str) -> dict[str, float]:
    """Get various statistics"""
    return {"mean": 42.5, "median": 40.0, "std_dev": 5.2}


# Ordinary classes with type hints work for structured output
class UserProfile:
    name: str
    age: int
    email: str | None = None

    def __init__(self, name: str, age: int, email: str | None = None):
        self.name = name
        self.age = age
        self.email = email


@mcp.tool()
def get_user(user_id: str) -> UserProfile:
    """Get user profile - returns structured data"""
    return UserProfile(name="Alice", age=30, email="alice@example.com")


# Classes WITHOUT type hints cannot be used for structured output
class UntypedConfig:
    def __init__(self, setting1, setting2):  # type: ignore[reportMissingParameterType]
        self.setting1 = setting1
        self.setting2 = setting2


@mcp.tool()
def get_config() -> UntypedConfig:
    """This returns unstructured output - no schema generated"""
    return UntypedConfig("value1", "value2")


# Lists and other types are wrapped automatically
@mcp.tool()
def list_cities() -> list[str]:
    """Get a list of cities"""
    return ["London", "Paris", "Tokyo"]
    # Returns: {"result": ["London", "Paris", "Tokyo"]}


@mcp.tool()
def get_temperature(city: str) -> float:
    """Get temperature as a simple float"""
    return 22.5
    # Returns: {"result": 22.5}

if __name__ == "__main__":
    mcp.run()