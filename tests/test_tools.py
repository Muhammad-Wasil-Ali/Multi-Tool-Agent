# tests/test_weather_tool.py

from unittest.mock import MagicMock, patch

# from app.tools.currency import currency_converter
from app.tools.search_weather import search_weather

# def test_search_weather_success():
#     with patch("app.tools.search_weather.requests.get") as mock_get:
#         mock_response = MagicMock()
#         mock_response.status_code = 200
#         mock_response.json.return_value = {
#             "cod": "200",
#             "list": [
#                 {"main": {"temp": 30}, "weather": [{"description": "clear sky"}], "dt_txt": "2026-07-23 12:00:00"}
#             ],
#             "city": {"name": "Attock"}
#         }
#         mock_response.raise_for_status.return_value = None
#         mock_get.return_value = mock_response

#         result = search_weather.invoke({"city_name": "Attock", "days": 1})

#         assert result["cod"] == "200"
#         assert result["city"]["name"] == "Attock"


def test_search_weather_success():
    with patch("app.tools.search_weather.requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "cod": "200",
            "list": [
                {
                    "dt_txt": "2026-07-23 12:00:00",
                    "main": {
                        "temp": 30,
                        "feels_like": 33,
                        "humidity": 50,
                        "pressure": 1000
                    },
                    "weather": [{"description": "clear sky"}],
                    "clouds": {"all": 10},
                    "wind": {"speed": 5},
                    "pop": 0.2,
                    "rain": {}
                }
            ],
            "city": {
                "name": "Attock",
                "country": "PK"
            }
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = search_weather.invoke({"city_name": "Attock", "days": 1})

        assert result["success"] is True
        assert result["city"] == "Attock"
        assert result["country"] == "PK"
        assert result["forecast"][0]["temperature_c"] == 30
        assert result["forecast"][0]["condition"] == "clear sky"