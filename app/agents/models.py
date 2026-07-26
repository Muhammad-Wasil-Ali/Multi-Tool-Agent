from langchain_openrouter import ChatOpenRouter

from app.configs.keys_config import settings
from app.logger.custom_logger import get_logger

logger=get_logger(__name__)
def get_model():
    logger.info("Initializing model")
    return ChatOpenRouter(model=settings.OPENROUTER_MODEL,api_key=settings.OPENROUTER_API_KEY)

model=get_model()


if __name__=="__main__":
    result=model.invoke("How are you")
    print(result)
    print(result.content)