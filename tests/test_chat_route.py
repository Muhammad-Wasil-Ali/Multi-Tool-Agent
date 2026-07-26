from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

from app.main import app

client=TestClient(app)

def make_fake_message(content:str,tool_calls:list | None=None):
    fake_message=MagicMock()
    fake_message.content=content
    fake_message.tool_calls=tool_calls or []
    return fake_message


@patch("app.api.routes.chat_route.agent")
def test_chat_success(mock_agent):
    # Arrange the fake data
    
    fake_message=make_fake_message("Its a 30 degree C in lahore and 10 usd in pkr is approx 2800 Rs",[ {"name": "search_weather"},
        {"name": "rate_conversion"}])
    
    mock_agent.invoke.return_value={"messages":[fake_message]}
    
    response=client.post("/chat",json={"message":"Weather in lahore and convert 10 usd to pkr"})
    
    assert response.status_code==200
    
    data=response.json()
    
    assert  data["reply"]=="Its a 30 degree C in lahore and 10 usd in pkr is approx 2800 Rs"
    assert  data["tool_calls_made"]==["search_weather","rate_conversion"]
    

