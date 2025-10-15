from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
    
    model_config = SettingsConfigDict(
        env_file='.env',
        extra='ignore' 
    )
    SECRET_KEY: str = Field(..., description="Clé secrète pour les jetons JWT et les sessions.")
    SERPAPI_API_KEY: str = Field(..., description="Clé de l'API SerpApi pour la collecte de données.")
    OPENAI_API_KEY: str = Field(..., description="Clé pour l'analyse de CV par l'IA.") 
    DATABASE_URL: str = "sqlite:///users.db" 
    GOOGLE_CLIENT_ID: str = Field(..., description="ID client Google pour OAuth.")
    GOOGLE_CLIENT_SECRET: str = Field(..., description="Secret client Google pour OAuth.")
    GOOGLE_REDIRECT_URI: str = Field(...,description="uri redirction")
   
settings = None
def initialize_settings():
    global settings
    if settings is None:
        settings = Settings()
    return settings

