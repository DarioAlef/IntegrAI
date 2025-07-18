from pydantic import BaseSettings
from dotenv import load_dotenv

load_dotenv()  # Para compatibilidade com outras partes do código

class Settings(BaseSettings):
    GROQ_API_KEY: str
    UNREAL_SPEECH_API_KEY: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()