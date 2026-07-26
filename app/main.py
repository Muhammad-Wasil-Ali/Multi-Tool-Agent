from fastapi import FastAPI

from app.api.routes.chat_route import router
from app.logger.custom_logger import get_logger

app=FastAPI(title="Weather & Currency API",description="This agent is used to search weather and updated currecny conversion using langchain adn tools",version="1.0.0")



logger=get_logger(__name__)

app.include_router(router)

@app.get("/")
def health_check():
    logger.info("Health check pinged")
    return {"status":"ok","message":"Weather & Currency API is running"}