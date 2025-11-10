import os
from pydantic_settings import BaseSettings
from .logger import logger

class Settings(BaseSettings):
    EMBEDDINGS_MODEL: str = "BAAI/bge-m3"
    CHROMA_DB_PATH: str = "app/data/vectorstores/medicacoes_db"
    PPLX_API_KEY: str = os.getenv("PPLX_API_KEY", "")
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
    
    class Config:
        env_file = ".env"

settings = Settings()
