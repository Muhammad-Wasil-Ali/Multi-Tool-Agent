from langchain.agents import create_agent
from app.agents.models import model
from app.tools.search_weather import search_weather
from app.tools.currency import currency_converter,rate_conversion
from app.logger.custom_logger import get_logger


logger=get_logger(__name__)

SYSTEM_PROMPT="""
You are an AI help ful assistant and your name is 'M W A'.Always use the provided tools for calculations and data lookups never compute or guess values by yourself
"""

def get_agent():
    
    logger.info(f"Initializing agent... ")
    return create_agent(model=model,tools=[search_weather,rate_conversion,currency_converter],system_prompt=SYSTEM_PROMPT) 

agent=get_agent()

if __name__=="__main__":
    result=agent.invoke({
        "messages":[{"role":"user","content":"what is the weather in islamabad and convert the 10 usd into pkr"}]
    })
    
    print(result)
    print(result["messages"][-1].content)

