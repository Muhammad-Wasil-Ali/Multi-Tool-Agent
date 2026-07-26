
import requests
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field

from app.configs.keys_config import settings
from app.exception.custome_exceptions import CityNotFoundError, WeatherAPIError
from app.logger.custom_logger import get_logger

WEATHER_API_KEY = settings.WEATHER_API_KEY
logger=get_logger(__name__)

class WeatherToolSchema(BaseModel):
    city_name: str = Field(
        description="Name of the city to get the weather forecast for."
    )
    days: int = Field(
        default=1,
        ge=1,
        le=7,
        description="Number of forecast days (1-7).",
    )


class SearchWeatherTool(BaseTool):
    name: str = "search_weather"
    description: str = (
        "Use this tool whenever the user asks about the weather "
        "or weather forecast for a city."
    )

    args_schema: type[WeatherToolSchema] = WeatherToolSchema
    def _run(self, city_name: str, days: int):
        """
        Fetch weather forecast from OpenWeatherMap API.
        """

        cnt = days * 8  # OpenWeatherMap provides data every 3 hours

        url = (
            f"https://api.openweathermap.org/data/2.5/forecast?q={city_name}&appid={WEATHER_API_KEY}&units=metric&cnt={cnt}")
        logger.info(f"Fetching weather for {city_name}")

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()

        except requests.exceptions.HTTPError as e:
            if response.status_code == 404:
                logger.error(f"City not found: {city_name}")
                raise CityNotFoundError(f"City '{city_name}' not found.")
            else:
                logger.error(f"Weather API HTTP error: {e}")
                raise WeatherAPIError(f"Weather API error: {e}")

        except requests.exceptions.Timeout:
            logger.error("Weather API request timed out")
            raise WeatherAPIError("Weather API request timed out.")

        except requests.exceptions.ConnectionError:
            logger.error("Could not connect to weather API")
            raise WeatherAPIError("Could not connect to weather API.")
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Weather API request failed: {e}")
            raise WeatherAPIError(f"Weather API request failed: {e}")
        logger.info("Weather Fetched Successfully")
        return clean_weather_data(response.json())



def clean_weather_data(data):
    """
    Convert OpenWeatherMap response into a simplified format.
    """

    forecast = []

    for item in data["list"]:
        forecast.append(
            {
                "date_time": item["dt_txt"],
                "temperature_c": item["main"]["temp"],
                "feels_like_c": item["main"]["feels_like"],
                "humidity": item["main"]["humidity"],
                "pressure": item["main"]["pressure"],
                "condition": item["weather"][0]["description"],
                "cloud_percent": item["clouds"]["all"],
                "wind_speed": item["wind"]["speed"],
                "rain_chance_percent": item["pop"] * 100,
                "rain_volume_mm": item.get("rain", {}).get("3h", 0),
            }
        )

    return {
        "success": True,
        "city": data["city"]["name"],
        "country": data["city"]["country"],
        "forecast": forecast,
    }


search_weather = SearchWeatherTool()


if __name__ == "__main__":
    result = search_weather.invoke(
        {
            "city_name": "Attock",
            "days": 1,
        }
    )

    print(result)