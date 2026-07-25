# app/api/schemas.py

from pydantic import BaseModel, Field
from typing import List


class ChatRequest(BaseModel):
    message: str = Field(description="User's natural language query, e.g. 'What's the weather in Lahore and convert 10 USD to PKR'")


class ChatResponse(BaseModel):
    reply: str = Field(description="Agent's final natural language answer")
    tool_calls_made: List[str] = Field(default=[], description="Names of tools the agent called while answering, in order")