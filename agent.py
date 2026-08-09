import os
from openai import OpenAI
import dotenv
from agents import Agent, Runner, function_tool, set_tracing_disabled
import requests
# Initialize the client. It automatically pulls your key from the OPENAI_API_KEY environment variable.
#Open environment variables from .env file

set_tracing_disabled(True)


dotenv.load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
base_url = os.getenv("OPENAI_BASE_URL")
client = OpenAI(
    api_key=api_key,
    base_url=base_url
)


@function_tool
def get_weather(location: str, country: str) -> str:
    """
    Get the current weather.

    Args:
        location: City name.
        country: Country name.
    """

    weather_api_key = os.getenv("WEATHER_API_KEY")

    response = requests.get(
        "https://api.weatherapi.com/v1/current.json",
        params={
            "key": weather_api_key,
            "q": f"{location}, {country}",
        },
        timeout=10,
    )

    response.raise_for_status()

    data = response.json()

    return (
        f"Location: {data['location']['name']}, "
        f"{data['location']['country']}\n"
        f"Temperature: {data['current']['temp_c']}°C\n"
        f"Condition: {data['current']['condition']['text']}\n"
        f"Humidity: {data['current']['humidity']}%"
    )

user_input = input("Enter your prompt: ")

instructions = "You are a weather agent. You can provide weather information for any location and time."

agent = Agent(
    name="Weather Agent",
    instructions=instructions,
    tools=[get_weather]
)

result = Runner.run_sync(
    agent, 
    user_input
)

print(result.final_output)