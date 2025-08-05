from pydantic_settings import BaseSettings
from pydantic import Field
from dotenv import load_dotenv


load_dotenv(dotenv_path=".env", override=True)


class Settings(BaseSettings):
    
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    SUPABASE_URL: str
    SUPABASE_KEY: str
    OPENAI_API_KEY: str
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    LIVEKIT_API_KEY: str
    LIVEKIT_API_SECRET: str
    LIVEKIT_URL: str
    DEEPGRAM_API_KEY: str
    CARTESIA_API_KEY: str
    
    
    class Config:
        env_file = "../.env"
        env_file_encoding = "utf-8"
        
settings = Settings()