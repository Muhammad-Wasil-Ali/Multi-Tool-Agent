from unittest.mock import MagicMock, patch


def get_weather_data(city):
    import requests
    
    response=requests.get(f"https://fakeapi.com/weather?city={city}")
    return response.json()

def test_get_weather_data_mocked():
    with patch("requests.get") as mock_get:
        mock_response=MagicMock()
        mock_response.json.return_value = {"temp": 30, "city": "Attock"}
        mock_get.return_value=mock_response
        
        result=get_weather_data("attock")
        
        assert result['temp']==30
        assert result['city']=="Attock"
        
test_get_weather_data_mocked()