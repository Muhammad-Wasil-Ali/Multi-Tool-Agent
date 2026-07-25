from fastapi import APIRouter,HTTPException
from app.agents.agent_setup import agent
from app.logger.custom_logger import get_logger
from app.exception.custome_exceptions import CityNotFoundError,InvalidCurrencyCodeError,WeatherAPIError,CurrencyAPIError
from app.api.schemas.agent_schemas import ChatRequest,ChatResponse


router=APIRouter()

logger=get_logger(__name__)

@router.post("/chat",response_model=ChatResponse)
def chat_with_agent(request:ChatRequest):
    logger.info(f"Chat Request Received : {request.message}")
    
    try:
        response=agent.invoke({"messages":[{"role":"user","content":request.message}]})
        final_result=response['messages'][-1].content
        tool_names = [
            tc["name"]
            for msg in response["messages"]
            if hasattr(msg, "tool_calls")
            for tc in msg.tool_calls
        ]
        
        logger.info(f"Agent responded successfully. Tool Used : {tool_names}")
        return ChatResponse(reply=final_result,tool_calls_made=tool_names)
    except (CityNotFoundError, InvalidCurrencyCodeError) as e:
        logger.error(f"Bad request: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except (WeatherAPIError, CurrencyAPIError) as e:
        logger.error(f"External API failure: {e}")
        raise HTTPException(status_code=502, detail=str(e))
    
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Something went wrong. Please try again.")