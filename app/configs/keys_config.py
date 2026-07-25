from dotenv import load_dotenv
import os

load_dotenv()


class Settings:
    GEMINI_API_KEY:str=os.getenv("GEMINI_API_KEY")
    OPENROUTER_API_KEY:str=os.getenv("OPENROUTER_API_KEY")
    GROQ_API_KEY:str=os.getenv("GROQ_API_KEY")
    WEATHER_API_KEY:str=os.getenv("WEATHER_API_KEY")
    EXCHANGERATE_API_KEY:str=os.getenv("EXCHANGERATE_API_KEY")
    
    # GEMINI_MODEL=""
    OPENROUTER_MODEL="cohere/north-mini-code:free"
    
settings=Settings()


if __name__=="__main__":
    print(f"GEMINI KEY : {settings.GEMINI_API_KEY}")
    print(f"OPENROUTER KEY : {settings.OPENROUTER_API_KEY}")
    print(f"WEATHER KEY : {settings.WEATHER_API_KEY}")
    print(f"EXCHANGE KEY : {settings.EXCHANGERATE_API_KEY}")
    print(f"GROQ KEY : {settings.GROQ_API_KEY}")
    
    
    
    